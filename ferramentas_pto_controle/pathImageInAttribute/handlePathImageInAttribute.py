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
import re
import psycopg2

class HandleUpdateFieldWithPathImage():
    def __init__(self, servidor, porta, nome_bd, usuario, senha):
        self.server = servidor
        self.port = porta
        self.bdname = nome_bd
        self.user = usuario
        self.password = senha
        conn_string = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
            servidor, porta, nome_bd, usuario, senha
        )
        self.conn = psycopg2.connect(conn_string)
    
    def getPathImages(self, folder):
        img_laterais = [x for x in Path(folder).rglob('3_Foto_Rastreio/*') if re.match("\.jpg", x.suffix)]
        img_aereas = [x for x in Path(folder).rglob('7_Imagens_Monografia/*') if re.match("\.jpg", x.suffix) and x.parts[-1].split("_")[1].split(".")[0] == "AEREA"]

        dictCodPontoImages = defaultdict(list)

        for img_lateral in img_laterais:
            codPonto = img_lateral.parts[-1].split("_")[0]
            dictCodPontoImages[codPonto].append(img_lateral)
        
        for img_aerea in img_aereas:
            codPonto = img_aerea.parts[-1].split("_")[0]
            dictCodPontoImages[codPonto].append(img_aerea)
        
        return dictCodPontoImages
    
    def updateDBPathImages(self, folder):
        dictCodPontoImages = self.getPathImages(folder)
        for codPonto in dictCodPontoImages:
            with self.conn.cursor() as cursor:
                cursor.execute(u'''
                UPDATE bpc.ponto_controle_p SET (
                    endereco_imagem_lateral_1,
                    endereco_imagem_lateral_2,
                    endereco_imagem_lateral_3,
                    endereco_imagem_lateral_4,
                    endereco_imagem_aerea) = ('{}', '{}', '{}', '{}', '{}') 
                WHERE cod_ponto = '{}'
                '''.format(str(dictCodPontoImages[codPonto][0]), str(dictCodPontoImages[codPonto][1]), str(dictCodPontoImages[codPonto][2]), str(dictCodPontoImages[codPonto][3]), str(dictCodPontoImages[codPonto][4]), codPonto))
        self.conn.commit()