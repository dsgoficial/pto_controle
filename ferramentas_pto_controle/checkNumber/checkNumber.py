from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFile)
from qgis.PyQt.QtCore import QCoreApplication
import re
from .handleCheckNumber import HandleCheckNumber


class CheckNumber(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    SERVERIP = 'SERVERIP'
    FOLDEROUT = 'FOLDEROUT'
    LYR_PTO_CONTROLE_P = 'LYR_PTO_CONTROLE_P'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.LYR_PTO_CONTROLE_P,
                self.tr('Camada do ponto de controle'),
                defaultValue="ponto_controle_p"
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDEROUT,
                self.tr('Pasta onde será salvo o .csv com os codigos disponíveis'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        lyrPtoControle = self.parameterAsVectorLayer(parameters, self.LYR_PTO_CONTROLE_P, context)
        folderOut = self.parameterAsFile(parameters, self.FOLDEROUT, context)

        cN = HandleCheckNumber()
        msg = cN.checkNumber(lyrPtoControle, folderOut)

        return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        return 'verificarcodigos'

    def displayName(self):
        return self.tr('14 - Verificar códigos de pontos disponíveis')

    def group(self):
        return self.tr("Gerenciar Pontos")

    def groupId(self):
        return "gerenciamento"

    def shortHelpString(self):
        return self.tr('''
            P14. Recebe a camada de pontos de controle e aponta os buracos na numeração, ou seja, os códigos disponíveis para uma próxima medição. Salva a lista em arquivo.

            Exemplo: existindo DF-HV-10, DF-HV-11 e DF-HV-13, a rotina devolve de DF-HV-1 a DF-HV-9, mais o DF-HV-12.

            Atenção: o código do ponto segue UF-HV-XXXX, com até 4 dígitos e SEM zero à esquerda.
            ''')

    def shortDescription(self):
        return self.tr(
            'P14. Recebe a camada de pontos de controle e aponta os buracos na numeração, ou seja, os códigos disponíveis para uma próxima medição. Salva a lista em arquivo.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CheckNumber()

class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True