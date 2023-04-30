# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2020-01-07
        copyright            : (C) 2020 by 1CGEO/DSG
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
__date__ = '2020-01-07'
__copyright__ = '(C) 2020 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import subprocess
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber)
from qgis.PyQt.QtCore import QCoreApplication
from .handleDistributeImages import HandleDistributeImages


class DistributeImages(QgsProcessingAlgorithm):
    """
    This algorithm distributes the aerial views inside the folder structure
    """

    FOLDERIN = 'FOLDERIN'
    FOLDERAERVIEW = 'FOLDERAERVIEW'
    FOLDERVIEW1 = 'FOLDERVIEW1'
    FOLDERVIEW2 = 'FOLDERVIEW2'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr(
                    'Selecione a pasta com a(s) estrutura(s) de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERAERVIEW,
                self.tr('Selecione a pasta com as imagens aéreas'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERVIEW1,
                self.tr('Selecione a pasta com as imagens aéreas (nível município)'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERVIEW2,
                self.tr('Selecione a pasta com as imagens aéreas (nível estado)'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        folder_in = self.parameterAsFile(parameters, self.FOLDERIN, context)
        folder_aerview = self.parameterAsFile(parameters, self.FOLDERAERVIEW, context)
        folder_view1 = self.parameterAsFile(parameters, self.FOLDERVIEW1, context)
        folder_view2 = self.parameterAsFile(parameters, self.FOLDERVIEW2, context)

        handle = HandleDistributeImages(
            folder_in, folder_aerview, folder_view1, folder_view2)

        handle.create_folder()
        handle.distribute_images()

        return {self.OUTPUT: ''}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '08 - Distribuir vistas aéreas na estrutura de pasta'

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
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return None

    def shortHelpString(self):
        """
        Retruns a short helper string for the algorithm
        """
        return self.tr('''
        Esta ferramenta distribui as imagens aéreas aéreas dos pontos nas estruturas de pasta.
        Note que esta rotina é necessária para a geração da monografia.
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DistributeImages()
