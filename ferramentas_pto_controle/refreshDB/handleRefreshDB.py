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

import os
import sys
import csv
import re
import json
from pathlib import Path
import psycopg2
import pyproj
import shutil


class HandleRefreshDB():
    def __init__(self, pasta, servidor, porta, nome_bd, usuario, senha, json_file):
        self.pasta = Path(pasta)
        conn_string = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
            servidor, porta, nome_bd, usuario, senha)
        self.conn = psycopg2.connect(conn_string)
        with open(json_file) as setting:
            self.defaults = json.load(setting)['default']

    def getPointsFromCSV(self):
        '''
        Gets every row from CSV to prepare the commit on database
        '''
        points = []
        for root, dirs, files in os.walk(self.pasta):
            for f in files:
                if f.endswith(".csv"):
                    with open(os.path.join(root, f)) as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            # Inserts the defaults from JSON
                            points.append(self.getDefaults(row))
        return createTimeStamp(points)

    def getCoordsFromRinex(self, points):
        '''
        Reads RINEX and gets coordinates
        '''
        for root, dirs, files in os.walk(self.pasta):
            for f in files:
                pasta = root.split(os.sep)[-1]
                if re.search(r'.[0-9][0-9]o|O$', f) and pasta == '2_RINEX':
                    with open(os.path.join(root, f)) as rinex:
                        lines = rinex.readlines()
                        for line in lines:
                            key = line[60:].strip()
                            if key == 'END OF HEADER':
                                break
                            value = list(filter(None, line[:60].strip().split(' ')))
                            if key == 'MARKER NAME':
                                point_name = value[0]
                            if key == 'APPROX POSITION XYZ':
                                x, y, z = value[0], value[1], value[2]
                        results = transform(x, y, z)
                        for point in points:
                            if point['cod_ponto'] == point_name:
                                point['longitude'], point['latitude'], point['altitude_ortometrica'] = results
        return points

    def upsert(self, points):
        for point in points:
            str_key = ''
            str_value = ''
            debug = ''
            lista = list(point.items())
            for key, value in lista:
                str_key += '{},'.format(key)
                if value:
                    str_value += "'{}',".format(value)
                else:
                    str_value += "DEFAULT,"
                debug += '{} : {}\n'.format(key, value)
            with self.conn.cursor() as cursor:
                cursor.execute(u"""
                INSERT INTO bpc.ponto_controle_p ({keys}, geom)
                VALUES ({values}, ST_GeomFromText('POINT({longitude} {latitude})', 4674))
                ON CONFLICT (cod_ponto)
                DO
                UPDATE
                    SET ({keys}, geom) = ({values}, ST_GeomFromText('POINT({longitude} {latitude})', 4674))
                    WHERE ponto_controle_p.tipo_situacao in (1,2,4,9999);
                """.format(keys=str_key[:-1], values=str_value[:-1], **point))
                croqui, arq_rastreio, fotos = self.getAdditionalInfo(point)
                cursor.execute(u'''
                UPDATE bpc.ponto_controle_p SET (numero_fotos, possui_croqui, possui_arquivo_rastreio, tipo_situacao, latitude, longitude) = ({}, {}, {}, 2, NULL, NULL) WHERE cod_ponto = '{}'
                '''.format(fotos, bool(croqui), bool(arq_rastreio), point['cod_ponto']))
        self.conn.commit()

    def getAdditionalInfo(self, point):
        croqui = [x for x in self.pasta.rglob('*') if x.is_file() and x.parent.name == '4_Croqui' and x.match('*{}_CROQUI.*'.format(point['cod_ponto']))]
        arq_rastreio = [x for x in self.pasta.rglob('*') if x.is_file() and x.parent.name == '1_Formato_Nativo' and x.match('*{}.*'.format(point['cod_ponto']))]
        fotos = [x for x in self.pasta.rglob('*') if x.is_file() and x.parent.name == '3_Foto_Rastreio' and x.match('{}*_FOTO.*'.format(point['cod_ponto']))]
        return len(croqui), len(arq_rastreio), len(fotos)

    def getDefaults(self, row):
        to_update = set(self.defaults.keys()).difference(row)
        for item in to_update:
            row.update({item : self.defaults[item]})
        return row
    
    def create(self):
        msg = ""
        pto_regex = r"^([A-Z]{2})-(HV|Base|BASE)-[1-9]+[0-9]*$"
        sufixImagesRegex = r".*\.(png|jpg|jpeg)$"
        if any(not re.match(sufixImagesRegex, nameImage.suffix) for nameImage in self.pasta.rglob('3_Foto_Rastreio/*')):
            msg += "Verifique se todos os arquivos dentro da pasta de fotografias são imagens (.png, .jpg ou .jpeg)."
            return msg
        folderToRename = {}
        for root, dirs, files in os.walk(self.pasta):
            if re.match(pto_regex, Path(root).parts[-1]):
                if not "3_Foto_Rastreio_Processada" in dirs:
                    os.mkdir(os.path.join(root, "3_Foto_Rastreio_Processada"))
                    folderToRename[os.path.join(root, "3_Foto_Rastreio_Processada")] = os.path.join(root, "3_Foto_Rastreio")
                else:
                    msg += "Já há uma pasta de fotos processadas."
                    return msg
        msg += self.salvarImagem()

        for newFolder, oldFolder in folderToRename.items():
            shutil.rmtree(oldFolder)
            os.rename(newFolder, oldFolder)

        return msg
    
    def salvarImagem(self):
        for nameImage in self.pasta.rglob('3_Foto_Rastreio/*'):
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
            folderProcess = os.path.join(nameImage.parent.parent, '3_Foto_Rastreio_Processada')
            os.makedirs(os.path.dirname(os.path.join(folderProcess, nameImage.name)), exist_ok=True)
            openImage.thumbnail(size, Image.Resampling.LANCZOS)
            openImage.save(os.path.join(folderProcess, nameImage.name), 
                           format='JPEG', 
                           quality=70, 
                           subsampling=2
                        )
        msg = "As imagens processadas foram salvas na pasta 3_Foto_Rastreio"
        return msg


def createTimeStamp(points):
    for point in points:
        try:
            fuso = point['fuso_horario']
        except KeyError:
            point['fuso_horario'] = -3
        point['inicio_rastreio'] = '{} {} {}'.format(point['data_rastreio'], point['inicio_rastreio'], point['fuso_horario'])
        point['fim_rastreio'] = '{} {} {}'.format(point['data_rastreio'], point['fim_rastreio'], point['fuso_horario'])
        point['altura_antena'] = point['altura_antena'].replace(',', '.')
        point['altura_objeto'] = point['altura_objeto'].replace(',', '.')
        del point['fuso_horario']
    return points

def transform(x, y, z):
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    return pyproj.transform(ecef, lla, x, y, z, radians=False)

if __name__ == '__main__':
    atualiza_db = HandleRefreshDB(sys.argv[1], sys.argv[2],
                                  sys.argv[3], sys.argv[4],
                                  sys.argv[5], sys.argv[6], sys.argv[7])
    values = atualiza_db.getPointsFromCSV()
    points2 = atualiza_db.getCoordsFromRinex(values)
    atualiza_db.upsert(points2)
