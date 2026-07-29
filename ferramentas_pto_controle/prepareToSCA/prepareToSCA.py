# -*- coding: utf-8 -*-
"""P17: prepara a missão inteira para importação no Controle do Acervo (SCA).

Irmão do P10, e o contrário dele em quase tudo. O P10 monta o pacote MENOR, que
vai ao BPC da DSG: quatro arquivos por ponto, renomeados, só de ponto com órbita
final, sem ponto base. Aqui vai o pacote COMPLETO, que é o que o acervo guarda.

O que este passo entrega é um pacote pronto para as DUAS FASES do SCA:

    manifesto.json          o corpo de POST /api/ponto_controle/prepare-upload/missao
    <missao>.gpkg           a missão como ela foi validada em campo
    SC-HV-69/
        SC-HV-69_pacote.zip a pasta do ponto inteira, menos a monografia
        SC-HV-69.pdf        a monografia
    RS-HV-207/              ...

O manifesto traz, por ponto, os atributos lidos do GeoPackage e, por arquivo, o
tipo, o nome, o tamanho e o SHA-256. O servidor recalcula esse SHA-256 quando os
arquivos chegam ao volume: o daqui não é prova, é o que permite detectar a
transferência que corrompeu.

DOIS ARQUIVOS POR PONTO, e não um por arquivo (chefe, 2026-07-29; SCA a partir da
versão 1.7.0). O acervo oferece exatamente dois downloads, e o domínio de tipos
caiu de nove para dois. O zip guarda o caminho relativo, então a estrutura de
subpastas atravessa inteira, e nenhum arquivo precisa ser renomeado para caber
num nome só por ponto.
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
from .manifesto import (MONOGRAFIA, PACOTE, acha_monografia,
                        cod_ponto_invalido, entrada_de_arquivo, monta_pacote)

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
                destino_ponto = pasta_out / cod_ponto
                destino_ponto.mkdir(parents=True, exist_ok=True)

                # O PACOTE: a pasta do ponto inteira, menos a monografia. O zip
                # guarda o caminho relativo, então a estrutura de subpastas
                # atravessa. Nada precisa ser renomeado para caber, e arquivo
                # fora da estrutura conhecida entra junto em vez de sumir.
                zip_alvo = destino_ponto / f'{cod_ponto}_pacote.zip'
                incluidos, lixo = monta_pacote(pasta, zip_alvo)
                ignorados_geral.extend(lixo)

                if incluidos:
                    entrada = entrada_de_arquivo(zip_alvo, PACOTE)
                    arquivos.append(entrada)
                    total_arquivos += 1
                    total_mb += entrada['tamanho_mb']
                else:
                    zip_alvo.unlink()

                # A MONOGRAFIA viaja sozinha: é o documento que alguém procura
                # sem querer o resto.
                try:
                    monografia = acha_monografia(pasta)
                except ValueError as erro:
                    raise QgsProcessingException(str(erro))
                if monografia is not None:
                    alvo = destino_ponto / f'{cod_ponto}.pdf'
                    shutil.copyfile(monografia, alvo)
                    entrada = entrada_de_arquivo(alvo, MONOGRAFIA)
                    arquivos.append(entrada)
                    total_arquivos += 1
                    total_mb += entrada['tamanho_mb']

                feedback.pushInfo(
                    f'{cod_ponto}: pacote com {len(incluidos)} arquivo(s)'
                    + (', mais a monografia' if monografia is not None
                       else ', SEM monografia')
                    + (f', {len(lixo)} descartado(s)' if lixo else '')
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
                f'{len(ignorados_geral)} arquivo(s) de sistema descartado(s) do '
                'pacote:'
            )
            for caminho in ignorados_geral[:20]:
                feedback.pushWarning(f'  {caminho.name}')
            if len(ignorados_geral) > 20:
                feedback.pushWarning(f'  ... e mais {len(ignorados_geral) - 20}')

        sem_monografia = [
            p['cod_ponto'] for p in pontos
            if p['arquivos'] and not any(
                a['tipo_arquivo_id'] == MONOGRAFIA for a in p['arquivos'])
        ]
        if sem_monografia:
            feedback.pushWarning(
                f'{len(sem_monografia)} ponto(s) SEM monografia, entrando só com '
                f'o pacote: {", ".join(sem_monografia[:10])}'
                + (' ...' if len(sem_monografia) > 10 else '')
            )

        feedback.pushInfo(
            f'Pacote pronto em {pasta_out}: {len(pontos)} ponto(s), '
            f'{total_arquivos} arquivo(s) para o acervo, {total_mb:.1f} MB, '
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
            P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: o manifesto.json, o GeoPackage da missão e, por ponto, DOIS arquivos: o pacote zipado e a monografia.

            Antes: a missão toda validada, e o P03 já rodado. Peça ao Controle do Acervo o id do LOTE, que é como a missão é identificada lá.
            Depois: a importação no Controle do Acervo, em duas fases.

            Como importar, depois de rodar este passo:
            1. POST /api/ponto_controle/prepare-upload/missao com o conteúdo de manifesto.json. A resposta traz, por arquivo, o caminho de destino.
            2. Copie a pasta de cada ponto para o volume, nos caminhos que a resposta indicou.
            3. POST /api/ponto_controle/confirm-upload com o session_uuid. O servidor relê cada arquivo, recalcula o SHA-256 e grava.

            Por que dois arquivos por ponto:
            - o acervo oferece exatamente dois downloads, o pacote e a monografia;
            - o zip guarda o caminho relativo, então a estrutura de subpastas atravessa inteira;
            - nenhum arquivo precisa ser renomeado para caber num nome só por ponto.

            Diferença para o P10, que prepara o pacote do BPC:
            - o P10 leva quatro arquivos por ponto, renomeados, só de órbita FINAL e sem ponto base;
            - este leva a pasta inteira de cada ponto, sem filtro nenhum.

            Tamanho, medido na amostra do repositório (4 pontos):
            - pasta como o medidor entrega, antes do P03: cerca de 11 MB por ponto, dos quais 78% são as fotos de rastreio;
            - depois do P03, que recomprime essas fotos e substitui as originais: cerca de 3,6 MB por ponto.

            O zip quase não reduz o tamanho, porque JPEG já vem comprimido: medido em 5 pontos do acervo, o pacote fica em 92% da pasta. Ele é escolha de ORGANIZAÇÃO, e não de espaço.

            Atenção:
            - O passo PARA se algum código de ponto não servir ao acervo, ou se a pasta 8_Monografia tiver mais de um PDF.
            - Ponto sem monografia entra só com o pacote, e aparece na lista de avisos.
            - Só arquivo de sistema (Thumbs.db, .DS_Store) fica de fora do pacote. Todo o resto entra, inclusive o que estiver fora da estrutura de subpastas conhecida.
            - Rode depois do P03. Antes dele o pacote fica três vezes maior, com as fotos ainda no tamanho original.
            ''')

    def shortDescription(self):
        return self.tr(
            'P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: manifesto.json, o GeoPackage e, por ponto, o pacote zipado mais a monografia.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PrepareToSCA()
