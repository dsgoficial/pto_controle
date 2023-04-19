# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Organiza arquivos processados do PPP
Description          : Descompacta e distribui na estrutura de pastas os arquivos processados do PPP
Version              : 1.1
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
from re import search
import zipfile
from pathlib import Path
import shutil
import sys

def extraiZip(zip, estrutura):
    _files = [Path(estrutura / x) for x in Path(estrutura).iterdir()]
    for item in _files:
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    with zipfile.ZipFile(zip, 'r') as zip_ref:
        zip_ref.extractall(estrutura)
    if len(os.listdir(estrutura)) == 1:
        source = os.path.join(estrutura, os.listdir(estrutura)[0])
        if os.path.isdir(source):
            for f in os.listdir(source):
                shutil.move(os.path.join(source, f), estrutura)
            shutil.rmtree(source)


def organizePPP(estrutura_pasta, pasta_ppp):
    errors = []
    pto_regex = r"^[A-Z][A-Z]-(HV|Base|BASE)-[1-9]+[0-9]*$"
    zipfiles = {f.split("_")[1][:-4]: os.path.join(pasta_ppp, f) for f in os.listdir(pasta_ppp) if os.path.isfile(
        os.path.join(pasta_ppp, f)) and f.endswith('.zip') and len(f.split("_")) == 4 and search(pto_regex, f.split("_")[1][:-4])}
    ptos_estrutura = {}
    for root, dirs, files in os.walk(estrutura_pasta):
        rootname = Path(root).parts
        if search(pto_regex, rootname[-1]):
            if "6_Processamento_PPP" in dirs:
                ptos_estrutura[rootname[-1]] = os.path.join(root, "6_Processamento_PPP")

    for zip_pto in zipfiles:
        if zip_pto in ptos_estrutura:
            extraiZip(zipfiles[zip_pto], ptos_estrutura[zip_pto])

    if set(zipfiles.keys()) - set(ptos_estrutura.keys()):
        errors.append('Pontos nao encontrados na estrutura: {}'.format(repr(list(set(zipfiles.keys()) - set(ptos_estrutura.keys())))))
    if set(ptos_estrutura.keys()) - set(zipfiles.keys()):
        errors.append('Pontos que não possuem zip: {}'.format(repr(list(set(ptos_estrutura.keys()) - set(zipfiles.keys())))))

    return errors

if __name__ == "__main__":
    organizePPP(estrutura_pasta=sys.argv[1], pasta_ppp=sys.argv[2])