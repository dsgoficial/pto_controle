# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Prepara estrutura de pastas para o processamento
Description          : Cria pastas e compacta arquivos para iniciar o processamento PPP e TBC
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
import re
import zipfile
from pathlib import Path


def criaPastas(pasta):
    pto_regex = r"^([A-Z]{2})-(HV|Base|BASE)-[1-9]+[0-9]*$"
    date_regex = r"\d{4}-\d{2}-\d{2}"
    for root, dirs, files in os.walk(pasta):
        if re.match(pto_regex, Path(root).parts[-1]):
            if not "6_Processamento" in dirs:
                os.mkdir(os.path.join(root, "6_Processamento"))

def zipaPPP(pasta):
    to_zip = [x for x in Path(pasta).rglob('2_RINEX/*') if re.match(r'\.\d\d[on|ON]',  x.suffix)]
    points = set([x.parts[-3] for x in to_zip])
    for point in points:
        filtered = list(filter(lambda x: x.stem == point,to_zip))
        if filtered:
            write_path = filtered[0].parent / f'{filtered[0].parts[-3]}.zip'
            with zipfile.ZipFile(write_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for item in filtered:
                    zf.write(item, item.name)
