# -*- coding: utf-8 -*-
"""P17: prepara a missão inteira para importação no Controle do Acervo (SCA).

Irmão do P10, e o contrário dele em quase tudo. O P10 monta o pacote MENOR, que
vai ao BPC da DSG: quatro arquivos por ponto, renomeados, só de ponto com órbita
final, sem ponto base. Aqui vai o pacote COMPLETO, que é o que o acervo guarda.

O que este passo entrega é um pacote pronto para as DUAS FASES do SCA:

    manifesto.json     o corpo de POST /api/ponto_controle/prepare-upload/missao
    <missao>.gpkg      a missão como ela foi validada em campo
    SC-HV-69/          os arquivos do ponto, achatados, prontos para copiar
    RS-HV-207/         ...

O manifesto traz, por ponto, os atributos lidos do GeoPackage e, por arquivo, o
tipo, o nome, o tamanho e o SHA-256. O servidor recalcula esse SHA-256 quando os
arquivos chegam ao volume: o daqui não é prova, é o que permite detectar a
transferência que corrompeu.

Deixou de gerar um zip por ponto (2026-07-28). O SCA registra arquivo a arquivo,
com tipo próprio e limite por ponto; um zip chegaria como um arquivo só, de tipo
nenhum, e o acervo perderia o que a estrutura de pastas carrega hoje.
"""
import json
import re
import shutil
from pathlib import Path

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterNumber)
from qgis.PyQt.QtCore import QCoreApplication

from ..utils.missao import conecta, colunas_da_tabela, lonlat_de
from .manifesto import (arquivos_do_ponto, cod_ponto_invalido,
                        entrada_de_arquivo)

# Mesma forma de código que o resto do plugin reconhece nas PASTAS. O manifesto
# usa o cod_ponto do GeoPackage, que é o registro; este padrão só serve para
# achar a pasta de cada ponto no disco.
RE_PONTO = re.compile(r"^([A-Z]{2})-(HV|Base|BASE)-[0-9]+$")

TABELA = "ponto_controle_p"

# Colunas que NÃO viajam no manifesto. As de posição saem da geometria, e as de
# endereço são caminho absoluto na máquina do medidor. O SCA descarta e relata o
# que não conhece, mas mandar lixo de propósito é outra coisa.
FORA_DO_MANIFESTO = {"id", "cod_ponto", "geom", "latitude", "longitude"}


class PrepareToSCA(QgsProcessingAlgorithm):

    OUTPUT = 'OUTPUT'
    FOLDERIN = 'FOLDERIN'
    FOLDEROUT = 'FOLDEROUT'
    MISSAO = 'MISSAO'
    LOTE = 'LOTE'
    SUBSTITUIR = 'SUBSTITUIR'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr('Selecione a pasta com a estrutura de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.MISSAO,
                self.tr('Arquivo da missão (GeoPackage), criado no P01'),
                extension='gpkg'
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.LOTE,
                self.tr('Id do lote no Controle do Acervo'),
                type=QgsProcessingParameterNumber.Integer,
                minValue=1
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SUBSTITUIR,
                self.tr('Substituir ponto que já exista no acervo'),
                defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.FOLDEROUT,
                self.tr('Pasta onde o pacote da missão será gerado')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        pasta_in = Path(self.parameterAsFile(parameters, self.FOLDERIN, context))
        missao = Path(self.parameterAsFile(parameters, self.MISSAO, context))
        lote_id = self.parameterAsInt(parameters, self.LOTE, context)
        substituir = self.parameterAsBoolean(parameters, self.SUBSTITUIR, context)
        pasta_out = Path(self.parameterAsString(parameters, self.FOLDEROUT, context))
        pasta_out.mkdir(parents=True, exist_ok=True)

        registros = self._le_missao(missao)
        if not registros:
            raise QgsProcessingException(
                f'O arquivo {missao.name} não tem ponto nenhum em {TABELA}.'
            )

        pastas = {
            p.name.upper(): p
            for p in pasta_in.rglob('*')
            if p.is_dir() and RE_PONTO.match(p.name)
        }

        # Recusa o pacote inteiro se algum código não serve ao SCA. Descobrir
        # isso na geração custa segundos; descobrir na importação custa a
        # transferência inteira.
        recusados = [
            m for m in (cod_ponto_invalido(r['cod_ponto']) for r in registros)
            if m
        ]
        if recusados:
            raise QgsProcessingException(
                'Códigos de ponto que o Controle do Acervo não aceita:\n  '
                + '\n  '.join(recusados)
            )

        pontos = []
        sem_pasta = []
        ignorados_geral = []
        total_arquivos = 0
        total_mb = 0.0

        for i, registro in enumerate(registros):
            if feedback.isCanceled():
                return {}
            feedback.setProgress(i * 100 / len(registros))

            cod_ponto = registro['cod_ponto']
            pasta = pastas.get(cod_ponto.upper())

            arquivos = []
            if pasta is None:
                # Ponto registrado e ainda sem pasta é caso legítimo: o ponto
                # planejado entra no acervo pela coordenada, e a documentação
                # chega numa importação depois.
                sem_pasta.append(cod_ponto)
            else:
                aceitos, ignorados = arquivos_do_ponto(pasta)
                ignorados_geral.extend(ignorados)

                destino_ponto = pasta_out / cod_ponto
                destino_ponto.mkdir(parents=True, exist_ok=True)

                for caminho, tipo in aceitos:
                    entrada = entrada_de_arquivo(caminho, tipo)
                    nome_fisico = (
                        f"{entrada['nome_arquivo']}.{entrada['extensao']}"
                        if entrada['extensao'] else entrada['nome_arquivo']
                    )
                    alvo = destino_ponto / nome_fisico

                    # A pasta de origem some no caminho: o que ela significava
                    # virou tipo_arquivo_id. Dois arquivos de subpastas
                    # diferentes com o MESMO nome colidiriam aqui, e é melhor
                    # parar do que sobrescrever um deles calado.
                    if alvo.exists():
                        raise QgsProcessingException(
                            f'{cod_ponto}: dois arquivos com o nome {nome_fisico} '
                            f'em subpastas diferentes. Renomeie um deles.'
                        )
                    shutil.copyfile(caminho, alvo)

                    arquivos.append(entrada)
                    total_arquivos += 1
                    total_mb += entrada['tamanho_mb']

                feedback.pushInfo(
                    f'{cod_ponto}: {len(arquivos)} arquivo(s)'
                    + (f', {len(ignorados)} fora da estrutura' if ignorados else '')
                )

            pontos.append({
                'cod_ponto': cod_ponto,
                'latitude': registro['latitude'],
                'longitude': registro['longitude'],
                'atributos': registro['atributos'],
                'arquivos': arquivos,
            })

        manifesto = {
            'lote_id': lote_id,
            'substituir': substituir,
            'pontos': pontos,
        }
        caminho_manifesto = pasta_out / 'manifesto.json'
        caminho_manifesto.write_text(
            json.dumps(manifesto, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        # O gpkg viaja junto: ele é a missão como ela foi validada em campo, e o
        # manifesto é só o recorte que o acervo grava.
        shutil.copyfile(missao, pasta_out / missao.name)

        feedback.pushInfo('')
        if sem_pasta:
            feedback.pushInfo(
                f'{len(sem_pasta)} ponto(s) sem pasta, entrando só com a '
                f'coordenada: {", ".join(sem_pasta[:10])}'
                + (' ...' if len(sem_pasta) > 10 else '')
            )
        if ignorados_geral:
            feedback.pushWarning(
                f'{len(ignorados_geral)} arquivo(s) FORA da estrutura conhecida '
                'não entraram no manifesto:'
            )
            for caminho in ignorados_geral[:20]:
                feedback.pushWarning(f'  {caminho.name}')
            if len(ignorados_geral) > 20:
                feedback.pushWarning(f'  ... e mais {len(ignorados_geral) - 20}')

        feedback.pushInfo(
            f'Pacote pronto em {pasta_out}: {len(pontos)} ponto(s), '
            f'{total_arquivos} arquivo(s), {total_mb:.1f} MB, '
            f'mais {missao.name} e manifesto.json.'
        )
        return {self.OUTPUT: str(pasta_out)}

    @staticmethod
    def _le_missao(caminho):
        """Pontos do GeoPackage, no formato que o manifesto usa.

        A posição sai da GEOMETRIA, e não das colunas `latitude`/`longitude`:
        elas são REAL no arquivo e perdem casa decimal, cerca de 1 cm no terreno
        na sétima. Ponto sem geometria não entra, porque o acervo exige a posição.
        """
        con = conecta(str(caminho))
        try:
            colunas = colunas_da_tabela(con, TABELA)
            linhas = con.execute(
                f'SELECT {", ".join(colunas)} FROM {TABELA} ORDER BY cod_ponto'
            ).fetchall()
        finally:
            con.close()

        registros = []
        for linha in linhas:
            dados = dict(zip(colunas, linha))
            lon, lat = lonlat_de(dados.get('geom'))
            if lon is None or lat is None:
                continue

            atributos = {
                chave: valor
                for chave, valor in dados.items()
                if chave not in FORA_DO_MANIFESTO
                and not chave.startswith('endereco_')
                and valor not in (None, '')
            }
            registros.append({
                'cod_ponto': dados.get('cod_ponto'),
                'latitude': lat,
                'longitude': lon,
                'atributos': atributos,
            })
        return registros

    def name(self):
        return 'prepararsca'

    def displayName(self):
        return self.tr('17 - Preparar a missão para o Controle do Acervo')

    def group(self):
        return self.tr('Pós-processamento')

    def groupId(self):
        return 'posprocessamento'

    def shortHelpString(self):
        return self.tr('''
            P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: o manifesto.json, o GeoPackage da missão e uma pasta por ponto com os arquivos prontos para copiar.

            Antes: a missão toda validada, e o P03 já rodado. Peça ao Controle do Acervo o id do LOTE, que é como a missão é identificada lá.
            Depois: a importação no Controle do Acervo, em duas fases.

            Como importar, depois de rodar este passo:
            1. POST /api/ponto_controle/prepare-upload/missao com o conteúdo de manifesto.json. A resposta traz, por arquivo, o caminho de destino.
            2. Copie a pasta de cada ponto para o volume, nos caminhos que a resposta indicou.
            3. POST /api/ponto_controle/confirm-upload com o session_uuid. O servidor relê cada arquivo, recalcula o SHA-256 e grava.

            Diferença para o P10, que prepara o pacote do BPC:
            - o P10 leva quatro arquivos por ponto, renomeados, só de órbita FINAL e sem ponto base;
            - este leva todos os arquivos de cada ponto, sem filtro nenhum.

            Tamanho, medido na amostra do repositório (4 pontos):
            - pasta como o medidor entrega, antes do P03: cerca de 11 MB por ponto, dos quais 78% são as fotos de rastreio;
            - depois do P03, que recomprime essas fotos e substitui as originais: cerca de 3,6 MB por ponto.

            Ou seja, uma missão de 100 pontos que passou pelo P03 dá cerca de 360 MB. O pacote do BPC, para comparar, custa cerca de 1,4 MB por ponto.

            Atenção:
            - Não gera mais um zip por ponto. O acervo registra arquivo a arquivo, com tipo próprio; um zip chegaria como um arquivo só, de tipo nenhum.
            - O passo PARA se algum código de ponto não servir ao acervo, ou se dois arquivos do mesmo ponto tiverem o mesmo nome em subpastas diferentes.
            - Arquivo fora da estrutura de subpastas conhecida não entra no manifesto, e aparece na lista de avisos.
            - Rode depois do P03. Antes dele o pacote fica três vezes maior, com as fotos ainda no tamanho original.
            ''')

    def shortDescription(self):
        return self.tr(
            'P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: manifesto.json, o GeoPackage e uma pasta por ponto com os arquivos.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PrepareToSCA()
