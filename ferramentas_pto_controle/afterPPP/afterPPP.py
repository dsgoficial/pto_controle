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

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile)
from qgis.PyQt.QtCore import QCoreApplication
from .handleAfterPPP import organizePPP


class AfterPPP(QgsProcessingAlgorithm):
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
    FOLDERIN = 'FOLDERIN'
    FOLDEROUT = 'FOLDEROUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr('Selecione a pasta da estrutura de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDEROUT,
                self.tr('Selecionar a pasta dos arquivos PPP'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        folder_in = self.parameterAsFile(parameters, self.FOLDERIN, context)
        folder_out = self.parameterAsFile(parameters, self.FOLDEROUT, context)
        errors = organizePPP(folder_in, folder_out)

        return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '06 - Procedimento pós PPP'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

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
        """
        Retruns a short helper string for the algorithm
        """
        return self.tr('''
        Esta ferramenta descompacta os arquivos PPP no formato .zip e distribui os arquivos na estrutura padrão de pastas de ponto de controle.
        Os parâmetros necessários são:
        - Pasta com a estrutura de pontos de controle
        - Pasta com os arquivos PPP no formato zip
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AfterPPP()
