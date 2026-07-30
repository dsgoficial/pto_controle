# -*- coding: utf-8 -*-

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
__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString,
                       QgsProcessingFeedback,
                       QgsProcessingParameterNumber)
from qgis.PyQt.QtCore import QCoreApplication
from .handleRefreshDB import HandleRefreshDB


class RefreshDB(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    OUTPUT = 'OUTPUT'
    FOLDER = 'FOLDER'
    JSON = 'JSON'
    MISSAO = 'MISSAO'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER,
                self.tr('Selecionar a pasta'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.JSON,
                self.tr('Selecionar o arquivo JSON'),
                extension='json'
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.MISSAO,
                self.tr('Arquivo da missão (GeoPackage), criado no P01'),
                extension='gpkg'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        folder = self.parameterAsFile(parameters, self.FOLDER, context)
        json = self.parameterAsFile(parameters, self.JSON, context)
        missao = self.parameterAsFile(parameters, self.MISSAO, context)

        refresh = HandleRefreshDB(folder, missao, json)
        points = refresh.getPointsFromCSV()
        points2 = refresh.getCoordsFromRinex(points)
        resumo, avisos = refresh.upsert(points2)
        for aviso in avisos:
            feedback.reportError(aviso)
        feedback.pushInfo(
            'Pontos: {inseridos} inseridos, {atualizados} atualizados, '
            '{preservados} preservados por já estarem aprovados.'.format(**resumo)
        )
        msg = refresh.create()
        feedback.pushInfo(f"{msg}")

        return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'atualizarbanco'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('03 - Atualizar a missão')

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
            P03. Varre as subpastas, lê os RINEX de medição e carrega a missão. Ainda com dado NÃO processado, antes do PPP ou do RTE.

            Antes: P02 retornando zero erro. Use a mesma pasta e o mesmo JSON.
            Depois: P04, preparar para processamento.

            Atenção:
            - Esta rotina APAGA a pasta 3_Foto_Rastreio original. Ela recomprime as fotos para jpeg numa pasta nova e substitui a antiga. Exige a biblioteca Pillow no Python do QGIS.
            - Grava tipo_situacao_id como "Aguardando Revisão".
            - Confira o objeto "default" do JSON antes de rodar: é ele que preenche o que o CSV do medidor não traz.

            Desde a troca do PostgreSQL pelo GeoPackage, esta rotina escreve no arquivo da missão criado no P01. Sumiram os cinco parâmetros de conexão.
            - Coluna que o CSV traz e a tabela não tem é DESCARTADA e RELATADA no log, em vez de derrubar a carga.
            ''')

    def shortDescription(self):
        return self.tr(
            'P03. Varre as subpastas, lê os RINEX de medição e carrega a missão. Ainda com dado NÃO processado, antes do PPP ou do RTE.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return RefreshDB()
