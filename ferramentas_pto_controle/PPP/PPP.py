# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2022-10-18
        copyright            : (C) 2022 by 1CGEO/DSG
        email                : mateus.sereno@ime.eb.br
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
__date__ = '2022-10-18'
__copyright__ = '(C) 2022 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum)
from qgis.PyQt.QtCore import QCoreApplication, QSettings
from .handlePPP import runShellCmd
import os

class PPP(QgsProcessingAlgorithm):
    """
    This algoritm will only execute the windows command to run the ppp.js
    """

    OUTPUT = 'OUTPUT'
    FOLDER = 'FOLDER'
    FOLDER_EXIST = 'FOLDER_EXIST'
    EMAIL = 'EMAIL'
    BROWSER = 'BROWSER'
    MAX_BROWSERS = 'MAX_BROWSERS'

    BROWSER_INFO = [
        ('Google Chrome', 'chrome'),
        ('Mozilla Firefox', 'firefox'),
        ('Chromium', 'chromium'),
        ('Internet Explorer', 'ie'),
        ('Google Chrome Canary', 'chrome-canary'),
        ('Opera', 'opera'),
        ('Safari', 'safari'),
        ('Microsoft Edge (legacy)', 'edge')
    ]

    def getProxyString(self) -> str:
        settings = QSettings()
        settings.beginGroup('proxy')
        enabled = settings.value('proxyEnabled')
        host = settings.value('proxyHost')
        port = settings.value('proxyPort')
        user = settings.value('proxyUser')
        password = settings.value('proxyPassword')
        type = settings.value('proxyType')
        excludedUrls = list()
        if settings.value('proxyExcludedUrls'):
            excludedUrls = settings.value('proxyExcludedUrls')
        if settings.value('noProxyUrls'):
            excludedUrls += settings.value('noProxyUrls')
        
        if enabled == 'false' or type != 'HttpProxy':
            return ''

        proxyStr = f'--proxy {user}:{password}@{host}:{port}'
        return proxyStr
    
    def countSubfolders(self, path:str) -> int:
        subcount = 0

        subdirs = next(os.walk(path))[1]

        for subdir in subdirs:
            subpath = os.path.join(path, subdir)
            subsubs = next(os.walk(subpath))[1]
            subcount += len(subsubs)

        return subcount

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER,
                self.tr('Selecionar a pasta da estrutura de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER_EXIST,
                self.tr('Selecionar a pasta caso já existam arquivos PPP processados do projeto, evitando duplicatas'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.EMAIL,
                self.tr('Email válido'),
                defaultValue='example@abc.com'
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BROWSER,
                self.tr('Navegador'),
                map(lambda x: x[0], self.BROWSER_INFO),
                defaultValue = 0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_BROWSERS,
                self.tr('Número máximo de navegadores a abrir'),
                type=QgsProcessingParameterNumber.Type.Integer,
                defaultValue=5
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        folder = self.parameterAsFile(parameters, self.FOLDER, context)
        path_exist = self.parameterAsFile(parameters, self.FOLDER_EXIST, context)
        email = self.parameterAsString(parameters, self.EMAIL, context)
        browserIndex = self.parameterAsEnum(parameters, self.BROWSER, context)

        browser_alias = (self.BROWSER_INFO[browserIndex])[1]

        proxy_string = self.getProxyString()

        subfolder_count = self.countSubfolders(folder)
        max_browsers = self.parameterAsInt(parameters, self.MAX_BROWSERS, context)

        browsers_to_open = min(subfolder_count, max_browsers)
        # feedback.pushInfo(f'subfolder_count = {subfolder_count} | max_browsers = {max_browsers}')

        runShellCmd(folder, path_exist, email, proxy_string, browser_alias, browsers_to_open, feedback)

        return {self.OUTPUT: 'Resultados baixados. Verifique sua pasta de downloads.'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '5- Gerar PPP'

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
        Esta rotina acessa o portal do IBGE e realiza o download do processamento realizado pela plataforma de PPP do IBGE.
        Após verificar quais PPPs já foram baixados, a ferramenta abre uma janela (ou múltiplas, a ser especificado nos parâmetros) que realiza o download do PPP da página do IBGE.
        O navegador utilizado deve estar configurado para realizar os downloads de forma automática.
        Os parâmetros necessários para essa rotina são:
        - Pasta com a estrutura de pontos de controle
        - Pasta que possui os PPPs já baixados (para evitar duplicatas)
        - Email
        - Navegador a ser utilizado (de preferência chrome ou firefox)

        ATENÇÃO: O 'Testcafe' versão 0.17.2 deve estar instalado no Shell utilizado pelo QGIS.
        No Windows, pesquise por 'OSGeo4W Shell' no menu iniciar. Abra o shell e digite o comando:
        npm install -g testcafe@0.17.2
        No Linux, basta rodar o mesmo comando no terminal normalmente.

        Caso o npm não esteja instalado, adquira em:
        https://nodejs.org/en/download/
        Baixe o binário (no caso do windows, o .zip).
        Ao extrair terá uma pasta com vários arquivos. Você precisa dos seguintes:
        - node_modules (pasta)
        - node.exe
        - nodevars.bat
        - npm
        - npm.cmd
        Copie os arquivos mencionados e cole na pasta bin do QGIS
        (normalmente é 'C:\\Program Files\\QGIS 3.24.0\\bin')
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PPP()
