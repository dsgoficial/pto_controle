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

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber)
from qgis.PyQt.QtCore import QCoreApplication
import re
from .handleCreateDB import HandleCreateDB


class CreateDatabase(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """
    OUTPUT = 'OUTPUT'
    SERVERIP = 'SERVERIP'
    PORT = 'PORT'
    BDNAME = 'BDNAME'
    USER = 'USER'
    PASSWORD = 'PASSWORD'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.SERVERIP,
                self.tr('Insira o IP do computador')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PORT,
                self.tr('Insira a porta'),
                minValue=0,
                maxValue=9999,
                defaultValue=5432
            )
        )
        
        BDNAME = ValidationString(
            self.BDNAME,
            description=self.tr(
                'Insira o nome do banco')
        )
        self.addParameter(BDNAME)

        self.addParameter(
            QgsProcessingParameterString(
                self.USER,
                self.tr('Insira o usuário do PostgreSQL'),
            )
        )

        password = QgsProcessingParameterString(
            self.PASSWORD,
            self.tr('Insira a senha do PostgreSQL'),
        )
        password.setMetadata({
            'widget_wrapper':
            'ferramentas_pto_controle.utils.wrapper.MyWidgetWrapper'})

        self.addParameter(password)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        server_ip = self.parameterAsString(parameters, self.SERVERIP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        bdname = self.parameterAsString(parameters, self.BDNAME, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)

        db = HandleCreateDB(server_ip, port, bdname, user, password)
        db.create()

        return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'criarbanco'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('01 - Criar banco de dados')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Pré-processamento")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "preprocessamento"

    def shortHelpString(self):
        return self.tr('''
            P01, primeiro passo do fluxo. Cria o banco PostGIS estruturado do ponto de controle, com os schemas de domínio e o bpc.

            Antes: o PostgreSQL com PostGIS já instalado, e um usuário com permissão de criar banco.
            Depois: P02, validar a estrutura de pastas.

            Atenção:
            - Banco com o mesmo nome NÃO é sobrescrito. A rotina não apaga nada.
            - Use nome sem espaço e sem caractere especial.
            - Pela linha de comando, exporte PTOCONTROLE_DB_PASSWORD em vez de passar a senha como parâmetro.
            ''')

    def shortDescription(self):
        return self.tr(
            'P01, primeiro passo do fluxo. Cria o banco PostGIS estruturado do ponto de controle, com os schemas de domínio e o bpc.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateDatabase()

class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True