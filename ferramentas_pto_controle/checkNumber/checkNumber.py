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
        return '14 - Verificar códigos de pontos disponíveis'

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr("Gerenciar Pontos")

    def groupId(self):
        return "gerenciamento"

    def shortHelpString(self):
        return self.tr('''
        Esta ferramenta verifica quais são os números que constam como faltantes no banco fornecido. Por exemplo, suponha que existam os pontos 
                       DF-HV-10, DF-HV-11 e DF-HV 13, a rotina irá retornar um .csv com os pontos DF-HV-1 até DF-HV-9 e o DF-HV-12.''')
        
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CheckNumber()

class ValidationString(QgsProcessingParameterString):
    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[A-Za-z0-9]+$", value):
            return True