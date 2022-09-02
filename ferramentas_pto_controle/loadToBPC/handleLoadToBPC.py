# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2019-12-04
        copyright            : (C) 2019 by 1CGEO/DSG
        email                : eliton.filho@eb.mil.br
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
__date__ = '2019-12-04'
__copyright__ = '(C) 2019 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import csv
import zipfile
from pathlib import Path


class HandleLoadToBPC():

    def __init__(self, folderin, folderout):
        self.folder = folderin
        self.output = folderout

    def getWhereClausule(self):
        '''
        Reads points from CSV and prompts the generation of zipfile.
        Returns WHERE clausule in the end
        '''
        points = ''
        for root, dirs, files in os.walk(self.folder):
            for f in files:
                if f.endswith(".csv"):
                    self.gerenatezip(Path(root))
                    with open(os.path.join(root, f)) as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            points += "'{}',".format(row['cod_ponto'])
        return "WHERE cod_ponto IN ({})".format(points[:-1])

    def gerenatezip(self, root):
        '''
        Creates an expression generator to select folders with points, then
        checks the existence of PPP files and generates the zips
        '''
        points = (x for x in root.iterdir() if Path(
            root / x / '1_Formato_Nativo').exists())
        for point in points:
            name = point.name
            files = [
                point / '1_Formato_Nativo' / '{}.T01'.format(name),
                point / '2_RINEX' / '{}.zip'.format(name),
                point / '8_Monografia' / '{}.pdf'.format(name)
            ]
            path_ppp = point / '6_Processamento_PPP'
            for child in path_ppp.iterdir():
                if child.suffix == '.pdf':
                    files.append(child)
            # for item in files:
                # if not item.exists():
                    # raise FileNotFoundError(f'O arquivo {item} não existe. Verifique a estrutura de pastas.')
            zf = zipfile.ZipFile(
                Path(self.output, '{}.zip'.format(name)), 'w', zipfile.ZIP_DEFLATED)
            for item in files:
                if item.exists():
                    zf.write(item, item.relative_to(point))
