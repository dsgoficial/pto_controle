# -*- coding: utf-8 -*-
"""P17: prepara a missão inteira para importacao no Controle do Acervo (SCA).

Irmao do P10, e o contrario dele em quase tudo. O P10 monta o pacote MENOR, que
vai ao BPC da DSG: quatro arquivos por ponto, renomeados, só de ponto com órbita
final, sem ponto base. Aqui vai o pacote COMPLETO, que é o que o acervo guarda:
a pasta inteira de cada ponto, com as oito subpastas, sem filtro nenhum.

Medido na amostra do repositorio: o pacote do BPC custa cerca de 1,4 MB por ponto
e a missão completa cerca de 13,7 MB, dos quais 78% são as fotos de rastreio.
"""
import re
import shutil
import zipfile
from pathlib import Path

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination)
from qgis.PyQt.QtCore import QCoreApplication

# Mesma forma de código que o resto do plugin reconhece: UF-HV-1234, e as bases.
RE_PONTO = re.compile(r"^([A-Z]{2})-(HV|Base|BASE)-[0-9]+$")


class PrepareToSCA(QgsProcessingAlgorithm):

    OUTPUT = 'OUTPUT'
    FOLDERIN = 'FOLDERIN'
    FOLDEROUT = 'FOLDEROUT'
    MISSAO = 'MISSAO'

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
            QgsProcessingParameterFolderDestination(
                self.FOLDEROUT,
                self.tr('Pasta onde o pacote da missão será gerado')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        pasta_in = Path(self.parameterAsFile(parameters, self.FOLDERIN, context))
        missao = Path(self.parameterAsFile(parameters, self.MISSAO, context))
        pasta_out = Path(self.parameterAsString(parameters, self.FOLDEROUT, context))
        pasta_out.mkdir(parents=True, exist_ok=True)

        pontos = sorted(
            p for p in pasta_in.rglob('*')
            if p.is_dir() and RE_PONTO.match(p.name)
        )
        if not pontos:
            raise QgsProcessingException(
                f'Nenhuma pasta de ponto encontrada em {pasta_in}. '
                'A pasta a escolher é a mesma dos passos anteriores.'
            )

        total_bytes = 0
        for i, ponto in enumerate(pontos):
            if feedback.isCanceled():
                break
            feedback.setProgress(i * 100 / len(pontos))
            destino = pasta_out / f'{ponto.name}.zip'
            # Sem filtro de órbita e sem descartar ponto base, ao contrario do
            # P10: o acervo guarda a missão como ela foi medida.
            arquivos = self._zipar_ponto(ponto, destino)
            tamanho = destino.stat().st_size
            total_bytes += tamanho
            feedback.pushInfo(
                f'{ponto.name}: {arquivos} arquivo(s), '
                f'{tamanho / 1024 / 1024:.1f} MB no zip'
            )

        # O gpkg viaja junto: e ele que carrega os atributos dos pontos.
        copia_missao = pasta_out / missao.name
        shutil.copyfile(missao, copia_missao)

        feedback.pushInfo('')
        feedback.pushInfo(
            f'Pacote pronto em {pasta_out}: {len(pontos)} ponto(s), '
            f'{total_bytes / 1024 / 1024:.1f} MB em zips, mais {missao.name}.'
        )
        return {self.OUTPUT: str(pasta_out)}

    @staticmethod
    def _zipar_ponto(ponto, destino):
        """Compacta a pasta INTEIRA do ponto. Devolve quantos arquivos entraram.

        Preservar o caminho relativo importa: e por ele que a importacao sabe que
        um .jpg veio de 3_Foto_Rastreio e não de 7_Imagens_Monografia.

        Devolve a CONTAGEM, e não a soma dos tamanhos. Quem chama mede o zip no
        disco, que é o número que importa para transferir. Reportar a soma dos
        arquivos daria um valor maior que o arquivo gerado, o que confunde.
        """
        if destino.exists():
            destino.unlink()
        entraram = 0
        with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zf:
            for arquivo in sorted(ponto.rglob('*')):
                if not arquivo.is_file():
                    continue
                if arquivo.name in ('.DS_Store', 'Thumbs.db', 'desktop.ini'):
                    continue
                if '__MACOSX' in arquivo.parts:
                    continue
                zf.write(arquivo, arquivo.relative_to(ponto.parent))
                entraram += 1
        return entraram

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
            P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: um zip por ponto, com a pasta inteira, mais o arquivo GeoPackage da missão.

            Antes: P10, insumos do BPC preparados. Na prática, rode este quando a missão estiver toda validada.
            Depois: a importação no Controle do Acervo, que é feita fora do plugin.

            Diferença para o P10, que prepara o pacote do BPC:
            - o P10 leva quatro arquivos por ponto, renomeados, só de órbita FINAL e sem ponto base;
            - este leva a pasta inteira de cada ponto, com as oito subpastas, sem filtro nenhum.

            Tamanho, medido na amostra do repositório (4 pontos):
            - pasta como o medidor entrega, antes do P03: cerca de 11 MB por ponto, dos quais 78% são as fotos de rastreio;
            - depois do P03, que recomprime essas fotos e substitui as originais: cerca de 3,6 MB por ponto;
            - no zip deste passo: cerca de 3,0 MB por ponto, porque JPEG já vem comprimido e o zip só ganha 1,2x.

            Ou seja, uma missão de 100 pontos que passou pelo P03 dá cerca de 300 MB. O pacote do BPC, para comparar, custa cerca de 1,4 MB por ponto.

            Atenção:
            - Um zip por ponto, e não um zip único, para a importação poder ser retomada de onde parou.
            - Rode depois do P03. Antes dele o pacote fica três vezes maior, com as fotos ainda no tamanho original.
            ''')

    def shortDescription(self):
        return self.tr(
            'P17. Monta o pacote COMPLETO da missão para importação no Controle do Acervo: um zip por ponto, com a pasta inteira, mais o arquivo GeoPackage da missão.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PrepareToSCA()
