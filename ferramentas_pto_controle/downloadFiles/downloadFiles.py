# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2023-09-14
        copyright            : (C) 2023 by 1CGEO/DSG
        email                : matheus.silva@ime.eb.br
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
__date__ = '2023-09-14'
__copyright__ = '(C) 2023 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterBoolean)
from qgis.PyQt.QtCore import QCoreApplication
import re
from .handleDownloadFiles import HandleDownloadFiles


class DownloadFiles(QgsProcessingAlgorithm):
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
    LYR_PTO_CONTROLE_P = 'LYR_PTO_CONTROLE_P'
    FOLDEROUT = 'FOLDEROUT'
    MONOGRAFIA = 'MONOGRAFIA'
    CROQUI = 'CROQUI'
    VISTA_AEREA = 'VISTA_AEREA'
    RINEX = 'RINEX'
    FOTOGRAFIAS = 'FOTOGRAFIAS'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.LYR_PTO_CONTROLE_P,
                self.tr('Camada do ponto de controle'),
                defaultValue="ponto_controle_p"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDEROUT,
                self.tr('Pasta onde serão salvos os arquivos'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.MONOGRAFIA,
                self.tr('Realizar o download do arquivo Monografia'),
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CROQUI,
                self.tr('Realizar o download do arquivo Croqui'),
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.VISTA_AEREA,
                self.tr('Realizar o download da fotografia Vista Aérea'),
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.RINEX,
                self.tr('Realizar o download do arquivo RINEX'),
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FOTOGRAFIAS,
                self.tr('Realizar o downloado das fotografias laterais'),
                defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        lyrPtoControle = self.parameterAsVectorLayer(parameters, self.LYR_PTO_CONTROLE_P, context)
        folderOut = self.parameterAsFile(parameters, self.FOLDEROUT, context)
        boolMonografia = self.parameterAsBool(parameters, self.MONOGRAFIA, context)
        boolCroqui = self.parameterAsBool(parameters, self.CROQUI, context)
        boolVistaAerea = self.parameterAsBool(parameters, self.VISTA_AEREA, context)
        boolRinex = self.parameterAsBool(parameters, self.RINEX, context)
        boolFotografias = self.parameterAsBool(parameters, self.FOTOGRAFIAS, context)
        
        db = HandleDownloadFiles()
        msg = db.downloadSelectFileOfSelectFeatures(lyrPtoControle, folderOut, boolMonografia, boolCroqui, boolVistaAerea, boolRinex, boolFotografias)

        return {self.OUTPUT: msg}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '12 - Download dos arquivos'

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
        return self.tr("Gerenciar Pontos")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "gerenciamento"

    def shortHelpString(self):
        """
        Retruns a short helper string for the algorithm
        """
        return self.tr('''
        Esta ferramenta realiza o download dos arquivos das feições selecionadas do banco de ponto de controle.
        Os arquivos que o usuário poderá realizar o download são:
        - Fotografias laterais
        - Fotografia aérea
        - Monografia
        - Croqui
        - RINEX''')
        

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DownloadFiles()


class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True