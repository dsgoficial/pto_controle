# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Atualiza banco de dados de ponto de controle
Description          : Atualiza a situação dos pontos medidos no banco de dados de ponto de controle
Version              : 1.0
copyright            : 1ºCGEO / DSG
reference:
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

from collections import defaultdict
from pathlib import Path
import shutil
import psycopg2
import os
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QCoreApplication

class HandleDownloadFiles():
    def downloadSelectFileOfSelectFeatures(self, layer: QgsVectorLayer, folderOut, boolMono, boolCroqui, boolVista, boolRinex, boolFotografias):
        selectedFeatures = layer.getSelectedFeatures()
        msg = ""
        if layer.selectedFeatureCount() == 0:
            msg = "Não há nenhum ponto de controle selecionado."
            return msg
        
        for current, feat in enumerate(selectedFeatures):
            codPonto = feat["cod_ponto"]
            pathPonto = os.path.join(folderOut, codPonto)
            if codPonto in os.listdir(folderOut):
                shutil.rmtree(pathPonto)
            os.mkdir(pathPonto)
            if boolMono:
                msg = self.copyFile(pathPonto, feat["endereco_monografia"])
            
            if boolCroqui:
                msg = self.copyFile(pathPonto, feat["endereco_croqui"])
            
            if boolVista:
                msg = self.copyFile(pathPonto, feat["endereco_imagem_aerea"])
            
            if boolRinex:
                msg = self.copyFile(pathPonto, feat["endereco_rinex"])
            
            if boolFotografias:
                msg = self.copyFile(pathPonto, feat["endereco_imagem_lateral_1"])
                msg = self.copyFile(pathPonto, feat["endereco_imagem_lateral_2"])
                msg = self.copyFile(pathPonto, feat["endereco_imagem_lateral_3"])
                msg = self.copyFile(pathPonto, feat["endereco_imagem_lateral_4"])
        
        return msg
        
    
    def copyFile(self, pathPonto, attribute):
        path = Path(attribute)
        nameFile = path.name
        pathDestination = os.path.join(pathPonto, nameFile)
        shutil.copy(path, pathDestination)
        msg = "O processo foi concluído com sucesso"
        return msg