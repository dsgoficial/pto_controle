"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2019-11-18
        copyright            : (C) 2019 by 1CGEO/DSG
        email                : eliton.filho@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '1CGEO/DSG'
__date__ = '2019-11-18'
__copyright__ = '(C) 2019 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterFileDestination)
from qgis.PyQt.QtCore import QCoreApplication
from .gpkg_schema import criar_missao


class CreateDatabase(QgsProcessingAlgorithm):
    """Cria o GeoPackage da missão, copiando a semente versionada no plugin."""

    OUTPUT = 'OUTPUT'
    SAIDA = 'SAIDA'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.SAIDA,
                self.tr('Arquivo da missão (GeoPackage) a ser criado'),
                fileFilter='GeoPackage (*.gpkg)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        saida = self.parameterAsFileOutput(parameters, self.SAIDA, context)
        if not saida.lower().endswith('.gpkg'):
            saida += '.gpkg'

        feedback.pushInfo('Criando a missão a partir da semente do plugin...')
        try:
            # A copia confere, antes de tudo, se a semente corresponde ao
            # new_db.sql de hoje. Semente defasada entregaria uma missão com
            # schema velho, com confiança e sem aviso.
            criado = criar_missao(saida)
        except FileExistsError as erro:
            raise QgsProcessingException(str(erro))
        except (FileNotFoundError, RuntimeError) as erro:
            raise QgsProcessingException(str(erro))

        feedback.pushInfo(f'Missão criada: {criado}')
        feedback.pushInfo(
            'Carregue a camada ponto_controle_p deste arquivo no QGIS para '
            'acompanhar a missão.'
        )
        return {self.OUTPUT: str(criado)}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'criarbanco'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('01 - Criar a missão (GeoPackage)')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("1. Preparar a missão")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "preparacao"

    def shortHelpString(self):
        return self.tr('''
            P01, primeiro passo do fluxo. Cria o arquivo da missão (GeoPackage), já com as tabelas do ponto de controle e os códigos de domínio semeados.

            Antes: nada. Não precisa mais de PostgreSQL nem de PostGIS.
            Depois: P02, validar a estrutura de pastas.

            A missão é um arquivo só, que se copia, se leva a campo e se anexa num e-mail.

            Atenção:
            - Arquivo existente NÃO é sobrescrito. A rotina não apaga nada.
            - O arquivo nasce de uma semente versionada no plugin. Se alguém mexer no schema e não regerar a semente, a rotina RECUSA criar e diz o comando do conserto.
            - A chave estrangeira do GeoPackage é da CONEXÃO, não do servidor. As rotinas do plugin a ligam. Editar o atributo à mão pela tabela do QGIS não liga, e ali dá para gravar código de domínio inexistente.
            ''')

    def shortDescription(self):
        return self.tr(
            'P01, primeiro passo do fluxo. Cria o arquivo da missão (GeoPackage), já com as tabelas do ponto de controle e os códigos de domínio semeados.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateDatabase()