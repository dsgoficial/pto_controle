# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2025-09-29
        copyright            : (C) 2025 by 1CGEO/DSG
        email                : matheus.alvessilva@eb.mil.br
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
__date__ = '2025-09-29'
__copyright__ = '(C) 2025 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile)
from qgis.PyQt.QtCore import QCoreApplication
import os
import re
from pathlib import Path
import shutil

class ZipFoldersCheckpoints(QgsProcessingAlgorithm):
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
                self.tr('Selecionar a pasta onde serão salvos as pastas dos pontos de controle compactadas'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        folder_in = self.parameterAsFile(parameters, self.FOLDERIN, context)
        folder_out = self.parameterAsFile(parameters, self.FOLDEROUT, context)

        msg = self.create(folder_in)
        feedback.pushInfo(f"{msg}")

        pto_regex = r"^([A-Z]{2})-(HV|Base|BASE)-[1-9]+[0-9]*$"
        for root, dirs, files in os.walk(folder_in):
            if re.match(pto_regex, Path(root).parts[-1]):
                write_path = Path(folder_out) / Path(root).parts[-1]
                shutil.make_archive(write_path, 'zip', root)

        return {self.OUTPUT: 'Processamento Concluído'}

    def create(self, pasta):
        msg = ""
        pto_regex = r"^([A-Z]{2})-(HV|Base|BASE)-[1-9]+[0-9]*$"
        sufixImagesRegex = r".*\.(png|jpg|jpeg)$"
        if any(not re.match(sufixImagesRegex, nameImage.suffix) for nameImage in Path(pasta).rglob('4_Croqui/*')):
            msg += "Verifique se todos os arquivos dentro da pasta do croqui são imagens (.png, .jpg ou .jpeg)."
            return msg
        folderToRename = {}
        for root, dirs, files in os.walk(Path(pasta)):
            if re.match(pto_regex, Path(root).parts[-1]):
                if not "4_Croqui_Processado" in dirs:
                    os.mkdir(os.path.join(root, "4_Croqui_Processado"))
                    folderToRename[os.path.join(root, "4_Croqui_Processado")] = os.path.join(root, "4_Croqui")
                else:
                    msg += "Já há uma pasta de croqui processado."
                    return msg
        msg += self.salvarImagem(pasta)

        for newFolder, oldFolder in folderToRename.items():
            shutil.rmtree(oldFolder)
            os.rename(newFolder, oldFolder)

        return msg
    
    def salvarImagem(self, pasta):
        for nameImage in Path(pasta).rglob('4_Croqui/*'):
            try:
                from PIL import Image
                openImage = Image.open(str(nameImage))
            except ModuleNotFoundError:
                msg = "Verifique se a biblioteca Pillow está instalada, confira as instruções de instalação na documentação."
                return msg
            if isinstance(openImage, str):
                msg = openImage
                return msg
            width, heigth = openImage.size
            if width > heigth:
                size = 1200, 900
            else:
                size = 900, 1200
            folderProcess = os.path.join(nameImage.parent.parent, '4_Croqui_Processado')
            os.makedirs(os.path.dirname(os.path.join(folderProcess, nameImage.name)), exist_ok=True)
            openImage.thumbnail(size, Image.Resampling.LANCZOS)
            openImage.save(os.path.join(folderProcess, nameImage.name), 
                           format='JPEG', 
                           quality=70, 
                           subsampling=2
                        )
        msg = "As imagens processadas foram salvas na pasta 4_Croqui"
        return msg

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '16 - Compactar as pastas dos pontos de controle'

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
        Esta ferramenta compacta individualmente cada pasta de ponto de controle completamente e realiza o "resampling" 
        das fotografias presentes no Croqui para ocupar menos espaço.
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ZipFoldersCheckpoints()
