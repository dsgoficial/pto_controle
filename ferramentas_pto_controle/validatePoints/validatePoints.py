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

import re
import json
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum)
from qgis.PyQt.QtCore import QCoreApplication
from .evaluateStructure import EvaluateStructure


class ValidatePoints(QgsProcessingAlgorithm):
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
    FOLDER = 'FOLDER'
    OPERATORS = 'OPERATORS'
    DATE = 'DATE'
    FUSE = 'FUSE'
    ESTACAO = 'ESTACAO'
    IGN_PROC = 'IGN_PROC'
    FILE_DST = 'FILE_DST'
    JSON = 'JSON'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER,
                self.tr('Selecione a pasta da estrutura de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        param = ValidationString(
            self.OPERATORS,
            description=self.tr(
                'Insira o nome dos operadores separados por ;')
        )
        self.addParameter(param)

        date = ValidationDate(
            self.DATE,
            description=self.tr(
                'Insira a data no formato YYYY-MM-DD;')
        )
        self.addParameter(date)

        self.addParameter(
            QgsProcessingParameterNumber(
                self.FUSE,
                self.tr('Insira o fuso horário'),
                defaultValue=-3
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.ESTACAO,
                self.tr('Selecione o modelo da estação medidora:'),
                options = [self.tr('TOPCON'), self.tr('TRIMBLE')]
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.FILE_DST,
                self.tr('Insira o caminho do relatório de erros'),
                fileFilter='*.txt'
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGN_PROC,
                self.tr('Ignorar as pastas e arquivos de processamento?'),
                defaultValue=False
            )
        )

        json_file = ValidationJSON(
            self.JSON,
            self.tr('Inserir JSON com parâmetros default e parâmetros de validação'),
            extension='json'
        )
        self.addParameter(json_file)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        folder = self.parameterAsFile(parameters, self.FOLDER, context)
        operators = self.parameterAsString(parameters, self.OPERATORS, context)
        date = self.parameterAsString(parameters, self.DATE, context)
        fuse = self.parameterAsInt(parameters, self.FUSE, context)
        ign_proc = self.parameterAsBoolean(parameters, self.IGN_PROC, context)
        file_dst = self.parameterAsFileOutput(
            parameters, self.FILE_DST, context)
        json_file = self.parameterAsFile(parameters, self.JSON, context)
        estacao = self.parameterAsInt(parameters, self.ESTACAO, context)

        evaluate = EvaluateStructure(
            folder, operators, date, fuse, estacao, ign_proc, json_file)
        results = evaluate.evaluate()
        with open(file_dst, 'w') as f:
            erros_text = "\n".join(results)
            f.write(erros_text)

        return {self.OUTPUT: results}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'validarestrutura'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('02 - Validar a estrutura de pastas')

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
            P02, o portão do fluxo. Acha inconsistência na pasta do dia: arquivo faltando, metadado mal preenchido, foto ausente e tempo de medição abaixo do mínimo. Só se segue adiante com zero erro.

            Antes: a pasta entregue pelo medidor, e o JSON de parâmetros preenchido pelo gerente.
            Depois: P03, atualizar o banco.

            Estrutura que ele cobra:
            - A pasta escolhida é a de UM NÍVEL ACIMA das pastas do dia. As pastas do dia se chamam exatamente medidor_AAAA-MM-DD (underscore antes do nome, hífen na data).
            - Cada ponto precisa das subpastas 1_Formato_Nativo, 2_RINEX, 3_Foto_Rastreio e 4_Croqui. A 5_Foto_Auxiliar é opcional.
            - As pastas 6_Processamento, 7_Imagens_Monografia e 8_Monografia só passam com "Ignorar as pastas e arquivos de processamento" ligado.
            - Foto de rastreio: <PONTO>_<azimute>_FOTO.jpg, com azimute de 000 a 360.

            Atenção:
            - O JSON precisa do objeto "validacao" (alt_max_ant e dur_min). Sem ele a rotina não roda.
            - O objeto "default" do JSON é opcional, mas quando a mesma chave aparece no JSON e no CSV do medidor, o CSV VENCE.
            - O CSV só deve trazer as 13 colunas obrigatórias. Coluna a mais, mesmo válida no banco, vira aviso: fixe o valor no "default" do JSON.
            ''')

    def shortDescription(self):
        return self.tr(
            'P02, o portão do fluxo. Acha inconsistência na pasta do dia: arquivo faltando, metadado mal preenchido, foto ausente e tempo de medição abaixo do mínimo. Só se segue adiante com zero erro.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ValidatePoints()


class ValidationString(QgsProcessingParameterString):
    '''
    Auxiliary class for pre validation on measurer's names.
    '''
    # __init__ not necessary

    def __init__(self, name, description=''):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r'([a-z|A-Z]+)(?:;|$)', value):
            return True


class ValidationDate(QgsProcessingParameterString):
    '''
    Auxiliary class for pre validation on dates.
    '''
    # __init__ not necessary

    def __init__(self, name, description=''):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r'20\d\d-[01]\d-[0-3]\d', value):
            return True


class ValidationJSON(QgsProcessingParameterFile):
    '''
    Auxiliary class for pre validation on dates.
    '''

    def checkValueIsAcceptable(self, value, context=None):
        try:
            with open(value) as json_file:
                _tmp = json.load(json_file)
                [_v1, _v2] = [_tmp['validacao']['alt_max_ant'], _tmp['validacao']
                                        ['dur_min']]
        except (OSError, IOError, KeyError):
            return False
        return True
