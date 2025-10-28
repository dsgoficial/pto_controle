import os
import psycopg2
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterFile,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber, 
)
from qgis.PyQt.QtCore import QCoreApplication
from .handleDistributeMonography import HandleDistributeMonography 

class DistributeMonografia(QgsProcessingAlgorithm):
    """Gera PDFs simples dos pontos de controle, sem ODT."""

    # HOST = 'HOST'
    # PORTA = 'PORTA'
    # DATABASE = 'DATABASE'
    # USUARIO = 'USUARIO'
    # SENHA = 'SENHA'
    CAMADA = 'CAMADA'
    SELECIONADA = 'SELECIONADA'
    PASTA_ESTRUTURA = 'PASTA_ESTRUTURA'
    TIPO_MODELO = 'TIPO_MODELO'
    USAR_CROQUI = 'USAR_CROQUI_DIGITAL'
    LOGO = 'LOGOTIPO'
    ASSINATURA = 'ASSINATURA'
    TEMPLATE_QPT = 'TEMPLATE_QPT'

    def initAlgorithm(self, config=None):
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        # self.addParameter(QgsProcessingParameterString(self.HOST, self.tr('Host do PostgreSQL'), defaultValue='localhost'))
        # self.addParameter(QgsProcessingParameterNumber(self.PORTA, self.tr('Porta'), defaultValue=5432, type=QgsProcessingParameterNumber.Integer))
        # self.addParameter(QgsProcessingParameterString(self.DATABASE, self.tr('Banco de Dados'), defaultValue='treinamento'))
        # self.addParameter(QgsProcessingParameterString(self.USUARIO, self.tr('Usuário'), defaultValue='postgres'))
        # SENHA = QgsProcessingParameterString(
        #     self.SENHA,
        #     self.tr('Insira a senha do PostgreSQL'),
        # )
        # SENHA.setMetadata({
        #     'widget_wrapper':
        #     'ferramentas_pto_controle.utils.wrapper.MyWidgetWrapper'})

        # self.addParameter(SENHA)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.CAMADA,
                self.tr("Pontos para Monografia"),
                [QgsProcessing.TypeVectorPoint],
                defaultValue="",
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECIONADA, self.tr("Executar somente nas feições selecionadas")
            )
        )

        self.addParameter(QgsProcessingParameterFile(
            self.PASTA_ESTRUTURA, self.tr('Pasta com Estrutura dos Pontos'),
            behavior=QgsProcessingParameterFile.Folder,
            defaultValue=''
        ))

        self.addParameter(QgsProcessingParameterFile(
             self.LOGO, self.tr('Logotipo'),
             behavior=QgsProcessingParameterFile.File,
             defaultValue=''
        ))

        self.addParameter(QgsProcessingParameterFile(
             self.ASSINATURA, self.tr('Assinatura'),
             behavior=QgsProcessingParameterFile.File,
             defaultValue=''
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
        # host = self.parameterAsString(parameters, self.HOST, context)
        # porta = self.parameterAsInt(parameters, self.PORTA, context)
        # database = self.parameterAsString(parameters, self.DATABASE, context)
        # usuario = self.parameterAsString(parameters, self.USUARIO, context)
        # senha = self.parameterAsString(parameters, self.SENHA, context)
        camada_input = self.parameterAsVectorLayer(parameters, self.CAMADA, context)
        feicao_selecionada = self.parameterAsBool(parameters, self.SELECIONADA, context)
        pasta_estrutura = self.parameterAsFile(parameters, self.PASTA_ESTRUTURA, context)
        logotipo = self.parameterAsFile(parameters, self.LOGO, context)
        assinatura = self.parameterAsFile(parameters, self.ASSINATURA, context)
        tipo_modelo = self.parameterAsEnum(parameters, self.TIPO_MODELO, context)
        usar_croqui_digital = self.parameterAsBool(parameters, self.USAR_CROQUI, context)

        retrato_qpt = os.path.join(self.plugin_dir, 'assets', 'modelo_retrato.qpt')
        paisagem_qpt = os.path.join(self.plugin_dir, 'assets', 'modelo_paisagem.qpt')
        if tipo_modelo == 1:
            template_qpt = retrato_qpt
            feedback.pushInfo('Usando modelo: Retrato')
        else:
            template_qpt = paisagem_qpt
            feedback.pushInfo('Usando modelo: Paisagem')

        # conn = self.getConnection(host, porta, database, usuario, senha, feedback)
        # if not conn:
        #     feedback.reportError('Falha ao conectar ao banco.')
        #     return {}

        handler = HandleDistributeMonography(
            layer = camada_input,
            feicao = feicao_selecionada,
            path=pasta_estrutura,
            template_qpt=template_qpt,
            settings={'LOGOTIPO': logotipo, 'signature': assinatura},
            digital=usar_croqui_digital,
            feedback=feedback,
            tipo_modelo=tipo_modelo
        )
        folders = handler.getFoldersFromStructure()
        total = len(folders)
        sucesso = 0
        feedback.setCurrentStep(1)
        
        if total == 0:
            feedback.pushInfo("Nenhuma pasta de ponto encontrada na estrutura.")
            return {}

        for i, folder in enumerate(folders):
            if feedback.isCanceled():
                feedback.pushInfo("Processamento cancelado pelo usuário.")
                break
            cod_ponto = folder.parts[-1]
            feedback.setProgress((i / total) * 100)
            feedback.pushInfo(f"Processando ponto: {cod_ponto}")
            try:
                if handler.executeProcess(folder, tipo_modelo):
                    sucesso += 1
            except Exception as e:
                feedback.reportError(f"Erro em {cod_ponto}: {str(e)}")

        feedback.pushInfo(f"{sucesso}/{total} PDFs gerados com sucesso.")
        return {'total_gerado': sucesso}


    # def getConnection(self, host, port, db, user, password, feedback):
    #     try:
    #         conn = psycopg2.connect(host=host, port=port, database=db, user=user, password=password)
    #         feedback.pushInfo('Conectado ao banco.')
    #         return conn
    #     except Exception as e:
    #         feedback.reportError(f'Erro ao conectar: {e}')
    #         return None

    def name(self): return '09 - Gerar e distribuir monografias nas pastas'
    def displayName(self): return self.tr(self.name())
    def group(self): return self.tr("Pós-processamento")
    def groupId(self): return "posprocessamento"
    def shortHelpString(self): return "Gera PDFs simples com informações dos pontos, sem usar ODT."
    def tr(self, s): return QCoreApplication.translate('Processing', s)
    def createInstance(self): return DistributeMonografia()