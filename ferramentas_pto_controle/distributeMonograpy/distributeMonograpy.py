# -*- coding: utf-8 -*-
import os
import sys
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer, 
    QgsProcessingParameterFile,
    QgsProcessingParameterEnum,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber, 
)
from qgis.PyQt.QtCore import QCoreApplication

MISSING_DEPS = []

try:
    import psycopg2
except ImportError:
    MISSING_DEPS.append('psycopg2-binary')

HandleDistributeMonografia = None


class DistributeMonografia(QgsProcessingAlgorithm):
    """Gera PDFs simples dos pontos de controle, sem ODT."""

    HOST = 'HOST'
    PORTA = 'PORTA'
    DATABASE = 'DATABASE'
    USUARIO = 'USUARIO'
    SENHA = 'SENHA'
    PASTA_ESTRUTURA = 'PASTA_ESTRUTURA'
    TIPO_MODELO = 'TIPO_MODELO'
    USAR_CROQUI = 'USAR_CROQUI_DIGITAL'
    LOGO = 'LOGOTIPO'
    ASSINATURA = 'ASSINATURA'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(self.HOST, self.tr('Host do PostgreSQL'), defaultValue='localhost'))
        self.addParameter(QgsProcessingParameterNumber(self.PORTA, self.tr('Porta'), defaultValue=5432, type=QgsProcessingParameterNumber.Integer))
        self.addParameter(QgsProcessingParameterString(self.DATABASE, self.tr('Banco de Dados'), defaultValue='treinamento'))
        self.addParameter(QgsProcessingParameterString(self.USUARIO, self.tr('Usuário'), defaultValue='postgres'))
        self.addParameter(QgsProcessingParameterString(self.SENHA, self.tr('Senha'), defaultValue='senha123'))

        self.addParameter(QgsProcessingParameterFile(
            self.PASTA_ESTRUTURA, self.tr('Pasta com Estrutura dos Pontos'),
            behavior=QgsProcessingParameterFile.Folder,
            defaultValue='C:\\Users\\kretzer\\Desktop\\Git\\pto_controle\\arquivos\\antes_processamento'
        ))

        self.addParameter(QgsProcessingParameterFile(
            self.LOGO, self.tr('Logotipo'),
            behavior=QgsProcessingParameterFile.File,
            defaultValue='C:\\Users\\kretzer\\Desktop\\tutorial_pto_controle\\logoCGEO1.png'
        ))

        self.addParameter(QgsProcessingParameterFile(
            self.ASSINATURA, self.tr('Assinatura'),
            behavior=QgsProcessingParameterFile.File,
            defaultValue='C:\\Users\\kretzer\\Desktop\\tutorial_pto_controle\\assinatura.png'
        ))

        self.addParameter(QgsProcessingParameterEnum(
            self.TIPO_MODELO, self.tr('Orientação da Página'),
            options=['Paisagem', 'Retrato'], defaultValue=1
        ))

        self.addParameter(QgsProcessingParameterBoolean(
            self.USAR_CROQUI, self.tr('Usar Croqui Digital (se disponível)'), defaultValue=True
        ))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)

        if MISSING_DEPS:
            feedback.reportError(f"Dependências ausentes: {', '.join(MISSING_DEPS)}")
            return {}

        import psycopg2
        from .handleDistributeMonograpy import HandleDistributeMonografia

        host = self.parameterAsString(parameters, self.HOST, context)
        porta = self.parameterAsInt(parameters, self.PORTA, context)
        database = self.parameterAsString(parameters, self.DATABASE, context)
        usuario = self.parameterAsString(parameters, self.USUARIO, context)
        senha = self.parameterAsString(parameters, self.SENHA, context)
        pasta_estrutura = self.parameterAsFile(parameters, self.PASTA_ESTRUTURA, context)
        logotipo = self.parameterAsFile(parameters, self.LOGO, context)
        assinatura = self.parameterAsFile(parameters, self.ASSINATURA, context)
        tipo_modelo = self.parameterAsEnum(parameters, self.TIPO_MODELO, context)
        usar_croqui_digital = self.parameterAsBool(parameters, self.USAR_CROQUI, context)

        conn = self.getConnection(host, porta, database, usuario, senha, feedback)
        if not conn:
            feedback.reportError('Falha ao conectar ao banco.')
            return {}

        handler = HandleDistributeMonografia(
            path=pasta_estrutura,
            conn=conn,
            settings={'LOGOTIPO': logotipo, 'signature': assinatura},
            digital=usar_croqui_digital,
            feedback=feedback
        )

        folders = handler.getFoldersFromStructure()
        total = len(folders)
        sucesso = 0

        for i, folder in enumerate(folders):
            feedback.setProgress((i / total) * 100)
            try:
                handler.executeProcess(folder, tipo_modelo)
                sucesso += 1
            except Exception as e:
                feedback.reportError(f"Erro em {folder.name}: {str(e)}")

        conn.close()
        feedback.pushInfo(f"{sucesso}/{total} PDFs gerados com sucesso.")
        return {'total_gerado': sucesso}

    def getConnection(self, host, port, db, user, password, feedback):
        try:
            conn = psycopg2.connect(host=host, port=port, database=db, user=user, password=password)
            feedback.pushInfo('✓ Conectado ao banco.')
            return conn
        except Exception as e:
            feedback.reportError(f'Erro ao conectar: {e}')
            return None

    def name(self): return '09 - Distribuir monografia na estrutura de pastas'
    def displayName(self): return self.tr(self.name())
    def group(self): return self.tr("Pós-processamento")
    def groupId(self): return "posprocessamento"
    def shortHelpString(self): return "Gera PDFs simples com informações dos pontos, sem usar ODT."
    def tr(self, s): return QCoreApplication.translate('Processing', s)
    def createInstance(self): return DistributeMonografia()
