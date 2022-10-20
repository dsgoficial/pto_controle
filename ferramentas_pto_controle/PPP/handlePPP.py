# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Processamento PPP em lote
Description          : Realiza o download do ponto processado por PPP do IBGE em lote baseado nos arquivos RINEX de medição
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
import subprocess
from qgis.core import (QgsProcessingFeedback, QgsProcessingException)

def runShellCmd(path_ponto, path_exist, email, proxy_string, browser_alias, browsers_to_open, feedback:QgsProcessingFeedback):
    cur_dir = os.path.dirname(__file__)
    path_ppp_js = os.path.join(cur_dir, 'ppp.js')

    cmd = f'testcafe -c {browsers_to_open} {browser_alias} {path_ppp_js} {path_ponto} {path_exist} {email} {proxy_string}'
    # feedback.pushInfo("Running command: " + cmd)
    try:
        # out = subprocess.run("ver", shell=True, check=True, capture_output=True, encoding="850")
        # feedback.pushInfo("Version:")
        # feedback.pushInfo(out.stdout)

        # out = subprocess.check_output(cmd, shell=True, encoding="850")
        out = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        # feedback.pushInfo(out.stdout)
    except subprocess.CalledProcessError as e:
        # feedback.reportError("Caught CalledProcessError.")
        errorMsg = e.stderr
        emBegin = errorMsg[:10]
        if emBegin == "\'testcafe\'":
            feedback.reportError('testcafe is not installed on the Qgis Shell.')
            feedback.reportError('Open the shell (usually OSGeo4W) and run \'npm install -g testcafe@0.17.2\'.')
            raise QgsProcessingException('testcafe not installed')
        else:
            feedback.reportError("Unexpected CalledProcessError:")
            feedback.reportError(e.stderr)
            raise QgsProcessingException('Unexpected CalledProcessError')
    except:
        raise QgsProcessingException('Unexpected error')