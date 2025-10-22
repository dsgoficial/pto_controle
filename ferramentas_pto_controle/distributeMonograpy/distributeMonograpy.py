# -*- coding: utf-8 -*-
import os
import sys
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer, # Mantenha a importação, mesmo que não seja usada
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

# Importação do Handle será feita dentro de processAlgorithm


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
    TEMPLATE_QPT = 'TEMPLATE_QPT' # Adicionado parâmetro para o QPT

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(self.HOST, self.tr('Host do PostgreSQL'), defaultValue='localhost'))
        self.addParameter(QgsProcessingParameterNumber(self.PORTA, self.tr('Porta'), defaultValue=5432, type=QgsProcessingParameterNumber.Integer))
        self.addParameter(QgsProcessingParameterString(self.DATABASE, self.tr('Banco de Dados'), defaultValue='treinamento'))
        self.addParameter(QgsProcessingParameterString(self.USUARIO, self.tr('Usuário'), defaultValue='postgres'))
        self.addParameter(QgsProcessingParameterString(self.SENHA, self.tr('Senha'), defaultValue='senha123')) # isSecret=True para a senha

        self.addParameter(QgsProcessingParameterFile(
            self.PASTA_ESTRUTURA, self.tr('Pasta com Estrutura dos Pontos'),
            behavior=QgsProcessingParameterFile.Folder,
            defaultValue='C:\\Users\\kretzer\\Desktop\\Git\\pto_controle\\arquivos\\antes_processamento'
        ))

        # Adicionado parâmetro para o Template QPT
        self.addParameter(QgsProcessingParameterFile(
             self.TEMPLATE_QPT, self.tr('Arquivo de Template QPT'),
             behavior=QgsProcessingParameterFile.File,
             fileFilter='Layout template (*.qpt)',
             defaultValue=os.path.join(os.path.dirname(__file__), 'assets', 'modelo_teste0.qpt')
        ))
        
        # Remoção dos parâmetros LOGO, ASSINATURA, TIPO_MODELO e USAR_CROQUI se não forem usados na lógica QGIS/Atlas
        # Se você ainda precisar delas, mantenha, mas a lógica de uso deve ser movida para o Handle.

        # self.addParameter(QgsProcessingParameterFile(
        #      self.LOGO, self.tr('Logotipo'),
        #      behavior=QgsProcessingParameterFile.File,
        #      defaultValue='C:\Users\kretzer\Desktop\tutorial_pto_controle'
        # ))

        # self.addParameter(QgsProcessingParameterFile(
        #      self.ASSINATURA, self.tr('Assinatura'),
        #      behavior=QgsProcessingParameterFile.File,
        #      defaultValue=''
        # ))

        self.addParameter(QgsProcessingParameterEnum(
             self.TIPO_MODELO, self.tr('Orientação da Página'),
             options=['Paisagem', 'Retrato'], defaultValue=1
        ))

        self.addParameter(QgsProcessingParameterBoolean(
             self.USAR_CROQUI, self.tr('Usar Croqui Digital (se disponível)'), defaultValue=True
        ))
        # Fim dos parâmetros não essenciais, mas mantidos

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)

        if MISSING_DEPS:
            feedback.reportError(f"Dependências ausentes: {', '.join(MISSING_DEPS)}")
            return {}

        import psycopg2
        # Importa o Handle atualizado do mesmo pacote
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
        template_qpt = self.parameterAsFile(parameters, self.TEMPLATE_QPT, context)


        conn = self.getConnection(host, porta, database, usuario, senha, feedback)
        if not conn:
            feedback.reportError('Falha ao conectar ao banco.')
            return {}
        
        # O caminho do template QPT é obtido diretamente do parâmetro
        # template_path = os.path.join(os.path.dirname(__file__), 'assets', 'modelo_teste0.qpt')

        handler = HandleDistributeMonografia(
            path=pasta_estrutura,
            conn=conn,
            template_qpt=template_qpt, # Usa o template do parâmetro
            settings={'LOGOTIPO': logotipo, 'signature': assinatura},
            digital=usar_croqui_digital,
            feedback=feedback,
            tipo_modelo=tipo_modelo
        )

        # 1. Obter a lista de pastas de pontos para iteração
        folders = handler.getFoldersFromStructure()
        total = len(folders)
        sucesso = 0
        feedback.setCurrentStep(1)
        
        if total == 0:
            feedback.pushInfo("Nenhuma pasta de ponto encontrada na estrutura.")
            conn.close()
            return {}

        # 2. Iterar sobre as pastas (e, implicitamente, sobre os cod_ponto)
        for i, folder in enumerate(folders):
            if feedback.isCanceled():
                 break
                 
            cod_ponto = folder.parts[-1]
            feedback.setProgress((i / total) * 100)
            feedback.pushInfo(f"Processando ponto: {cod_ponto}")
            
            try:
                # 3. Chama o método que busca no banco, preenche o QPT e exporta o PDF
                if handler.executeProcess(folder, tipo_modelo):
                    sucesso += 1
            except Exception as e:
                feedback.reportError(f"Erro em {cod_ponto}: {str(e)}")

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