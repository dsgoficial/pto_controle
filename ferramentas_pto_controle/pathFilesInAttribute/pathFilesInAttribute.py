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

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterNumber)
from qgis.PyQt.QtCore import QCoreApplication
import re
from .handlePathFilesInAttribute import HandleUpdateFieldWithPathFiles


class PathFilesInAttribute(QgsProcessingAlgorithm):
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
    SERVERIP = 'SERVERIP'
    PORT = 'PORT'
    BDNAME = 'BDNAME'
    USER = 'USER'
    PASSWORD = 'PASSWORD'

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
            QgsProcessingParameterString(
                self.SERVERIP,
                self.tr('Insira o IP do computador')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PORT,
                self.tr('Insira a porta'),
                minValue=0,
                maxValue=9999,
                defaultValue=5432
            )
        )
        BDNAME = ValidationString(
            self.BDNAME,
            description=self.tr(
                'Insira o nome do banco')
        )
        self.addParameter(BDNAME)

        self.addParameter(
            QgsProcessingParameterString(
                self.USER,
                self.tr('Insira o usuário do PostgreSQL'),
            )
        )

        password = QgsProcessingParameterString(
            self.PASSWORD,
            self.tr('Insira a senha do PostgreSQL'),
        )
        password.setMetadata({
            'widget_wrapper':
            'ferramentas_pto_controle.utils.wrapper.MyWidgetWrapper'})

        self.addParameter(password)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        folderIn = self.parameterAsFile(parameters, self.FOLDERIN, context)
        server_ip = self.parameterAsString(parameters, self.SERVERIP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        bdname = self.parameterAsString(parameters, self.BDNAME, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)

        db = HandleUpdateFieldWithPathFiles(server_ip, port, bdname, user, password)
        msg = db.updateDBPathFiles(folderIn)

        return {self.OUTPUT: msg}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '11 - Inserir nos atributos os caminhos dos arquivos'

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
        Esta ferramenta atualiza os atributos no banco de dados com o caminho dos seguintes arquivos:
        - Fotografias laterais
        - Fotografia aérea
        - Monografia
        - Croqui
        - RINEX.''')
        

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PathFilesInAttribute()


class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True