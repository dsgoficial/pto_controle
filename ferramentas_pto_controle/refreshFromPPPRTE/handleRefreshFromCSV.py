# coding=utf8
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import csv

from ..utils.missao import conecta, ponto_gpkg, recontar_controle_medicao

class HandleRefreshFromCSV():

    def __init__(self, path, missao):
        self.folder = Path(path)
        self.conn = conecta(missao)
        self.atualizados = 0
        self.map_orbit = {
            'ULTRA-RÁPIDA': 2,
            'RÁPIDA': 3,
            'FINAL': 4
        }

    def readCSV(self):
        files = [x for x in self.folder.rglob('*.csv')]
        correct_csvs = []
        for item in files:
            if(not item.match("**/*LEIAME*")):
                correct_csvs.append(item)
        
        for correct_csv in correct_csvs:
            with open(correct_csv, newline = '') as csvfile:
                spamreader = csv.DictReader(csvfile, delimiter = ',')
                for row in spamreader:
                    point = {}
                    point['cod_ponto'] = row['cod_ponto']
                    point['latitude'] = row['latitude']
                    point['longitude'] = row['longitude']
                    point['norte'] = row['norte']
                    point['leste'] = row['leste']
                    point['altitude_geometrica'] = row['altitude_geometrica']
                    point['altitude_ortometrica'] = row['altitude_ortometrica']
                    point['modelo_geoidal'] = row['modelo_geoidal']
                    point['data_processamento'] = row['data_processamento']
                    point['meridiano_central'] = row['meridiano_central']
                    self.updateDB(point)

    def updateDB(self, point):
        """Grava o resultado do RTE no ponto, por parâmetro.

        A coluna `fuso` NÃO e preenchida aqui, ao contrario do ramo PPP, que a
        deriva do meridiano central. E assimetria do plugin, não do porte, e esta
        registrada no help do algoritmo.
        """
        cursor = self.conn.execute(
            'UPDATE ponto_controle_p SET norte = ?, leste = ?,'
            ' altitude_geometrica = ?, altitude_ortometrica = ?,'
            ' latitude = ?, longitude = ?, geom = ?, modelo_geoidal = ?,'
            ' data_processamento = ?, meridiano_central = ?'
            ' WHERE cod_ponto = ?',
            (
                point['norte'], point['leste'],
                point['altitude_geometrica'], point['altitude_ortometrica'],
                point['latitude'], point['longitude'],
                ponto_gpkg(point['longitude'], point['latitude']),
                point['modelo_geoidal'], point['data_processamento'],
                point['meridiano_central'], point['cod_ponto'],
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(
                f"o ponto {point['cod_ponto']} nao existe na missao. "
                "Rode o P03 (atualizar banco) antes deste passo."
            )
        self.atualizados += 1
        self.conn.commit()

    def recontar(self):
        tocados = recontar_controle_medicao(self.conn)
        self.conn.commit()
        return tocados

    @staticmethod
    def evaluateCoords(lat, lon):
        lat_deg, lat_min, lat_seg = re.findall(r'(.{2,3}) (\d\d) (.{7})', lat)[0]
        lon_deg, lon_min, lon_seg = re.findall(r'(.{2,3}) (\d\d) (.{7})', lon)[0]

        if float(lat_deg) > 0:
            new_lat = float(lat_deg) + float(lat_min)/60 + float(lat_seg.replace(',', '.'))/3600
        else:
            new_lat = float(lat_deg) - float(lat_min)/60 - float(lat_seg.replace(',', '.'))/3600

        if float(lon_deg) > 0:
            new_lon = float(lon_deg) + float(lon_min)/60 + float(lon_seg.replace(',', '.'))/3600
        else:
            new_lon = float(lon_deg) - float(lon_min)/60 - float(lon_seg.replace(',', '.'))/3600
        return new_lat, new_lon
    
    @staticmethod
    def getFuso(centralMeridian):
        return -(-(180 + centralMeridian)//6) # Equivalent to ceil


if __name__ == "__main__":
    test = HandleRefreshFromCSV(*sys.argv[1:])
    test.readCSV()