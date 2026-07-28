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
import pyproj
import shutil
from datetime import datetime, timedelta

from ..utils.missao import (
    conecta,
    colunas_da_tabela,
    upsert_ponto,
    recontar_controle_medicao,
)


class HandleRefreshDB():
    def __init__(self, pasta, missao, json_file):
        self.pasta = Path(pasta)
        self.conn = conecta(missao)
        self.colunas = colunas_da_tabela(self.conn, 'ponto_controle_p')
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
        """Grava os pontos na missao. Devolve (resumo, avisos).

        O `upsert_ponto` espelha o `ON CONFLICT ... WHERE tipo_situacao IN
        (1,2,4,9999)` que existia no PostGIS: ponto ja APROVADO nao se sobrescreve
        por recarga de pasta.

        A chave que a tabela nao tem deixa de entrar CALADA. Antes ela ia direto
        para o SQL e derrubava a carga (ou pior, casava com outra coluna); agora
        ela e descartada e RELATADA, que e o gesto que este vault ja pagou caro
        para aprender.
        """
        resumo = {'inseridos': 0, 'atualizados': 0, 'preservados': 0}
        avisos = []
        traducao = {
            'inserido': 'inseridos',
            'atualizado': 'atualizados',
            'preservado': 'preservados',
        }
        for point in points:
            acao, descartadas = upsert_ponto(self.conn, point, self.colunas)
            resumo[traducao[acao]] += 1
            if descartadas:
                avisos.append(
                    "AVISO: {} - coluna que a tabela nao tem, descartada: {}".format(
                        point.get('cod_ponto', '?'), ', '.join(descartadas)
                    )
                )
            if acao == 'preservado':
                continue
            croqui, arq_rastreio, fotos = self.getAdditionalInfo(point)
            self.conn.execute(
                'UPDATE ponto_controle_p SET numero_fotos = ?, possui_croqui = ?,'
                ' possui_arquivo_rastreio = ?, tipo_situacao = 2,'
                ' latitude = NULL, longitude = NULL WHERE cod_ponto = ?',
                (fotos, bool(croqui), bool(arq_rastreio), point['cod_ponto']),
            )
        self.conn.commit()
        return resumo, avisos

    def recontar(self):
        """A recontagem que era trigger no PostGIS. Aqui e explicita e por lote."""
        tocados = recontar_controle_medicao(self.conn)
        self.conn.commit()
        return tocados

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
    """Monta inicio_rastreio e fim_rastreio no DATETIME do GeoPackage.

    Antes saia '2022-07-03 09:05 -3', que e literal de timestamptz do PostgreSQL e
    so o PostgreSQL entende.

    O GeoPackage exige o ISO 8601 em UTC, com milissegundos e 'Z'
    ('2022-07-03T12:05:00.000Z'). Escrever com deslocamento local
    ('...-03:00') faz o GDAL avisar "non-conformant content, successfully
    parsed": ele aceita hoje, e tolerancia assim e o tipo de coisa que vira erro
    numa versao seguinte. A hora do medidor vem no fuso dele (coluna
    fuso_horario, padrao -3) e e convertida aqui.
    """
    for point in points:
        fuso = point.pop('fuso_horario', -3)
        try:
            horas = int(float(fuso))
        except (TypeError, ValueError):
            horas = -3
        for campo in ('inicio_rastreio', 'fim_rastreio'):
            hora = str(point[campo]).strip()
            if len(hora) == 5:  # HH:MM, que e o que o CSV do medidor traz
                hora += ':00'
            local = datetime.strptime(
                '{} {}'.format(point['data_rastreio'], hora), '%Y-%m-%d %H:%M:%S'
            )
            utc = local - timedelta(hours=horas)
            point[campo] = utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        point['altura_antena'] = point['altura_antena'].replace(',', '.')
        point['altura_objeto'] = point['altura_objeto'].replace(',', '.')
    return points

def transform(x, y, z):
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    return pyproj.transform(ecef, lla, x, y, z, radians=False)

if __name__ == '__main__':
    atualiza_db = HandleRefreshDB(sys.argv[1], sys.argv[2], sys.argv[3])
    values = atualiza_db.getPointsFromCSV()
    points2 = atualiza_db.getCoordsFromRinex(values)
    atualiza_db.upsert(points2)
