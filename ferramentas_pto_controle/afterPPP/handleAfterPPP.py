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

def organizePPP(estrutura_pasta, pasta_ppp):
    error = True
    errors = []
    pto_regex = r"^[A-Z][A-Z]-(HV|Base|BASE)-[1-9]+[0-9]*$"
    zipfiles = [os.path.join(pasta_ppp, f) for f in os.listdir(pasta_ppp) if "_zipAllRinex.zip_" in f]
    nameFolder = zipfiles[0].split("\\")[-1][:-4]

    ptos_estrutura = {}
    for root, dirs, files in os.walk(estrutura_pasta):
        rootname = Path(root).parts
        if search(pto_regex, rootname[-1]):
            if "6_Processamento" in dirs:
                ptos_estrutura[rootname[-1]] = os.path.join(root, "6_Processamento")

    extractAllRinexPath = os.path.join(pasta_ppp, "extractAllRinex")

    os.mkdir(extractAllRinexPath)
    with zipfile.ZipFile(zipfiles[0], 'r') as zip_ref:
        zip_ref.extractall(extractAllRinexPath)

    for pto in ptos_estrutura:
        for root, dirs, files in os.walk(os.path.join(extractAllRinexPath, f"{nameFolder}")):
            for file in files:
                if file.split(".")[0] != pto:
                    continue
                shutil.move(os.path.join(root, file), ptos_estrutura[pto])
                error = False
    
    shutil.rmtree(os.path.join(pasta_ppp, "extractAllRinex"))
    
    if not error:
        errors.append("Sucesso: Procedimento pós PPP realizado com sucesso!")
    else:
        errors.append("Falhou: O procedimento pós PPP não foi realizado!")
    

    return errors

if __name__ == "__main__":
    organizePPP(estrutura_pasta=sys.argv[1], pasta_ppp=sys.argv[2])