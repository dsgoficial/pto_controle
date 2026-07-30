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
from .distributeMonograpy.distributeMonograpy import DistributeMonografia
from .loadToBPC.loadToBPC import LoadToBPC
from .refreshFromPPPRTE.refreshFromPPPRTE import RefreshFromPPPRTE
from .fixDateTrimble.fixDateTrimble import FixDateTrimble
from .prepareToSCA.prepareToSCA import PrepareToSCA

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

        A ordem aqui é a ordem do FLUXO, e não a de importação. Ela repete a
        numeração dos rótulos: 01 a 04 preparam a missão, 06 e 07 incorporam o
        processamento, 08 a 10 documentam o ponto e 11 e 12 entregam. Não existe
        05: é o processamento externo (PPP no IBGE ou RTE em outro software).
        A auxiliar não é numerada, porque não tem posto no fluxo.
        """
        # 1. Preparar a missão
        self.addAlgorithm(CreateDatabase())
        self.addAlgorithm(ValidatePoints())
        self.addAlgorithm(RefreshDB())
        self.addAlgorithm(BeforePPP())
        # 2. Incorporar o processamento
        self.addAlgorithm(AfterPPP())
        self.addAlgorithm(RefreshFromPPPRTE())
        # 3. Documentar o ponto
        self.addAlgorithm(DistributeImages())
        self.addAlgorithm(DistributeCroqui())
        self.addAlgorithm(DistributeMonografia())
        # 4. Entregar
        self.addAlgorithm(LoadToBPC())
        self.addAlgorithm(PrepareToSCA())
        # Auxiliares
        self.addAlgorithm(FixDateTrimble())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'ptocontrole'

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
