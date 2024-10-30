# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2019-11-18
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
__date__ = '2019-11-18'
__copyright__ = '(C) 2019 by 1CGEO/DSG'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


import os
from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from .validatePoints.validatePoints import ValidatePoints
from .refreshDB.refreshDB import RefreshDB
from .createDB.createDB import CreateDatabase
from .beforePPP.beforePPP import BeforePPP
from .afterPPP.afterPPP import AfterPPP
from .distributeImages.distributeImages import DistributeImages
from .distributeCroqui.distributeCroqui import DistributeCroqui
from .loadToBPC.loadToBPC import LoadToBPC
from .refreshFromPPPRTE.refreshFromPPPRTE import RefreshFromPPPRTE
from .pathFilesInAttribute.pathFilesInAttribute import PathFilesInAttribute
from .downloadFiles.downloadFiles import DownloadFiles
from .fixDateTrimble.fixDateTrimble import FixDateTrimble
from .checkNumber.checkNumber import CheckNumber


class PontoControleProvider(QgsProcessingProvider):
    '''
    Provider do handle the algorithms
    '''
    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(ValidatePoints())
        self.addAlgorithm(RefreshDB())
        self.addAlgorithm(CreateDatabase())
        self.addAlgorithm(BeforePPP())
        self.addAlgorithm(AfterPPP())
        self.addAlgorithm(DistributeImages())
        self.addAlgorithm(DistributeCroqui())
        self.addAlgorithm(LoadToBPC())
        self.addAlgorithm(RefreshFromPPPRTE())
        self.addAlgorithm(PathFilesInAttribute())
        self.addAlgorithm(DownloadFiles())
        self.addAlgorithm(FixDateTrimble())
        self.addAlgorithm(CheckNumber())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'provider'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Ferramentas para Pontos de Controle')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QIcon(os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(__file__)
            )),
            'icons',
            'topo.png'
        ))

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
