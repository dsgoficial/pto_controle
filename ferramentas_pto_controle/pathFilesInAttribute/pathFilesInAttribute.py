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
    MISSAO = 'MISSAO'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr('Selecione a pasta da estrutura de pontos de controle'),
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
        folderIn = self.parameterAsFile(parameters, self.FOLDERIN, context)
        missao = self.parameterAsFile(parameters, self.MISSAO, context)

        db = HandleUpdateFieldWithPathFiles(missao)
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
        return 'caminhosnosatributos'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('11 - Inserir nos atributos os caminhos dos arquivos')

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
        return self.tr('''
            P11. Grava nos atributos do banco o caminho dos arquivos de cada ponto: as quatro fotos laterais, a foto aérea, a monografia, o croqui e o RINEX.

            Antes: a estrutura de pastas completa. Rodar com a estrutura pela metade grava caminho para arquivo que não existe.
            Depois: habilita o P12, que baixa os arquivos por esses caminhos.

            Atenção: o caminho gravado é o do momento da execução. Mover a estrutura de pastas depois disso quebra os links, e é preciso rodar de novo.

            Desde a troca do PostgreSQL pelo GeoPackage, esta rotina escreve no arquivo da missão criado no P01.
            - O caminho gravado é ABSOLUTO e do momento da execução. Como a missão viaja como arquivo, mover a estrutura de pastas depois disso quebra os links.
            ''')

    def shortDescription(self):
        return self.tr(
            'P11. Grava nos atributos do banco o caminho dos arquivos de cada ponto: as quatro fotos laterais, a foto aérea, a monografia, o croqui e o RINEX.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PathFilesInAttribute()


class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True