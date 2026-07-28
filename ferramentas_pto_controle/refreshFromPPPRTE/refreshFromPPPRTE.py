# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2019-11-18
        copyright            : (C) 2019 by 1CGEO/DSG
        email                : eliton.filho@eb.mil.br, arthur.santos@ime.eb.br, mateus.sereno@ime.eb.br
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
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum)
from qgis.PyQt.QtCore import QCoreApplication
from .handleRefreshFromPPP import HandleRefreshFromPPP
from .handleRefreshFromCSV import HandleRefreshFromCSV


class RefreshFromPPPRTE(QgsProcessingAlgorithm):
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
    TYPE = 'TYPE'
    FOLDER = 'FOLDER'
    MISSAO = 'MISSAO'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TYPE,
                self.tr('Selecione o método de processamento:'),
                options = [self.tr('PPP'), self.tr('RTE')]
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER,
                self.tr('Selecionar a pasta'),
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

    def processAlgorithm(self, parameters, context, feedback):
        process_type = self.parameterAsInt(parameters, self.TYPE, context)
        folder = self.parameterAsFile(parameters, self.FOLDER, context)
        missao = self.parameterAsFile(parameters, self.MISSAO, context)

        if process_type == 0:
            refresh = HandleRefreshFromPPP(folder, missao)
            refresh.readPPP()
        else:
            refresh = HandleRefreshFromCSV(folder, missao)
            refresh.readCSV()

        feedback.pushInfo(f'Pontos atualizados: {refresh.atualizados}')
        feedback.pushInfo(f'Polígonos de controle recontados: {refresh.recontar()}')

        return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'atualizarbancoppprte'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('07 - Atualizar banco com dados do PPP/RTE')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Pós-processamento")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "posprocessamento"

    def shortHelpString(self):
        return self.tr('''
            P07. Carrega no banco o resultado do processamento. É onde os ramos PPP e RTE convergem.

            Antes: P06 (ramo PPP), ou o processamento_rte.csv preenchido (ramo RTE).
            Depois: P08, distribuir as vistas aéreas.

            Escolha da pasta:
            - PPP: a pasta da estrutura de pontos, a mesma dos passos anteriores.
            - RTE: a pasta que contém o CSV do processamento. A rotina lê TODO .csv que houver ali, menos os que têm LEIAME no nome.

            Atenção:
            - No CSV do RTE, "norte" é o valor de 7 dígitos (a coordenada N) e "leste" é o de 6 dígitos (a coordenada E). Trocar as duas colunas grava coordenada errada sem nenhum aviso.
            - O meridiano central vai NEGATIVO no hemisfério oeste, por exemplo -51. É assim que o ramo PPP grava, e é o sinal que o cálculo do fuso espera.
            - O ramo RTE não preenche a coluna fuso, e não lê a coluna ponto_base.

            Desde a troca do PostgreSQL pelo GeoPackage, esta rotina escreve no arquivo da missão criado no P01.
            - Ponto processado que não existe na missão faz a rotina PARAR com o código do ponto na mensagem. Antes o UPDATE não achava a linha e seguia calado.
            - A contagem de pontos por polígono de controle roda ao fim desta rotina.
            ''')

    def shortDescription(self):
        return self.tr(
            'P07. Carrega no banco o resultado do processamento. É onde os ramos PPP e RTE convergem.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return RefreshFromPPPRTE()
