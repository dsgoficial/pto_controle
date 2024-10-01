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
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDateTime)
from qgis.PyQt.QtCore import QCoreApplication
import re
import os

class FixDateTrimble(QgsProcessingAlgorithm):
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

    FOLDERIN = 'FOLDERIN'
    FOLDEROUT = 'FOLDEROUT'
    OUTPUT = 'OUTPUT'
    DATE = 'DATE'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr('Selecione a pasta que contenha os pontos a serem ajustados:'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDEROUT,
                self.tr('Selecione a pasta onde os arquivos serão salvos:'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        DATE = ValidationDate(
            self.DATE,
            description=self.tr(
                'Insira a data no formato DD-MM-YYYY')
        )
        self.addParameter(DATE)


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        FOLDERIN = self.parameterAsFile(parameters, self.FOLDERIN, context)
        FOLDEROUT = self.parameterAsFile(parameters, self.FOLDEROUT, context)
        DATE = self.parameterAsString(parameters, self.DATE, context)
        DAY, MONTH, YEAR = DATE.split('-')
        DATE = [DAY, MONTH, YEAR]
        for arquivoNome in os.listdir(FOLDERIN):
            arquivoEntradaCaminho = os.path.join(FOLDERIN, arquivoNome)
            abrevAno = DATE[2][-2:]
            with open(arquivoEntradaCaminho) as f:
                primeira_linha = f.readline()
                if 'OBSERVATION DATA' in primeira_linha:
                    arquivoSaida = open(os.path.join(FOLDEROUT, f'{arquivoNome.split(".")[0]}.{abrevAno}o'), 'a')
                    with open(arquivoEntradaCaminho) as f:
                        fimCabecalho = False
                        for linha in f.readlines():
                            if (
                                'TIME OF FIRST OBS' in linha
                                or
                                'TIME OF LAST OBS' in linha
                            ):
                                novaLinha = f'  {DATE[2]}    {DATE[1].ljust(2)}    {DATE[0].ljust(2)}' + linha[18:]
                                arquivoSaida.write(novaLinha)
                                continue
                            if 'END OF HEADER' in linha:
                                fimCabecalho = True
                                arquivoSaida.write(linha)
                                continue
                            if not( fimCabecalho ) or not (linha[:2].count(' ') == 1):
                                arquivoSaida.write(linha)
                                continue
                            novaLinha = f' {abrevAno} {DATE[1].ljust(2)} {DATE[0].ljust(2)}' + linha[9:]
                            arquivoSaida.write(novaLinha)
                    arquivoSaida.close()
                if 'NAVIGATION DATA' in primeira_linha:
                    arquivoSaida = open(os.path.join(FOLDEROUT, f'{arquivoNome.split(".")[0]}.{abrevAno}n'), 'a')
                    with open(arquivoEntradaCaminho) as f:
                        fimCabecalho = False
                        for linha in f.readlines():
                            if 'END OF HEADER' in linha:
                                fimCabecalho = True
                                arquivoSaida.write(linha)
                                continue
                            if not( fimCabecalho ) or not (linha[:3].count(' ') <= 2 ):
                                arquivoSaida.write(linha)
                                continue

                            novaLinha = linha[:2] + f' {abrevAno} {DATE[1].ljust(2)} {DATE[0].ljust(2)}' + linha[11:]
                            arquivoSaida.write(novaLinha)
                    arquivoSaida.close()
                if 'METEOROLOGICAL DATA' in primeira_linha:
                    arquivoSaida = open(os.path.join(FOLDEROUT, f'{arquivoNome.split(".")[0]}.{abrevAno}m'), 'a')
                    with open(arquivoEntradaCaminho) as f:
                        fimCabecalho = False
                        for linha in f.readlines():
                            if 'END OF HEADER' in linha:
                                fimCabecalho = True
                                arquivoSaida.write(linha)
                                continue
                            if not( fimCabecalho ) or not (linha[:3].count(' ') <= 2 ):
                                arquivoSaida.write(linha)
                                continue

                            novaLinha = linha[:2] + f' {abrevAno} {DATE[1].ljust(2)} {DATE[0].ljust(2)}' + linha[11:]
                            arquivoSaida.write(novaLinha)
                    arquivoSaida.close()

        return {self.OUTPUT: ''}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '13 - Corrigir Data Arquivo TRIMBLE'

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
        Esta ferramenta corrige as datas dos arquivos RINEX de rastreadoras TRIMBLE que encerraram seu ciclo de ToW''')
        

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FixDateTrimble()


class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True
        
class ValidationDate(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r'[0-3]\d-[01]\d-20\d\d', value):
            return True