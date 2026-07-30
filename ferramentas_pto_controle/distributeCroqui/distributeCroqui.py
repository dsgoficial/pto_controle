# -*- coding: utf-8 -*-
import os
import shutil
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDefinition, QgsProject,
                       QgsPrintLayout, QgsLayoutItemMap, QgsReadWriteContext)
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtCore import QCoreApplication
import processing
from ..utils.atlas import indice_da_extensao
from .handleDistributeCroqui import HandleDistributeCroqui


class DistributeCroqui(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('pontos_de_controle', 'Pontos do Croqui Digital', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('imagem_de_satelite', 'Imagem de Satélite', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('pasta_do_ponto', 'Selecione a pasta com a estrutura de pontos de controle', behavior=QgsProcessingParameterFile.Folder))

        escala_satelite_param = QgsProcessingParameterNumber('escala_satelite', 'Escala para Satélite', QgsProcessingParameterNumber.Integer, defaultValue=500)
        escala_satelite_param.setFlags(escala_satelite_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(escala_satelite_param)

        dpi_param = QgsProcessingParameterNumber('dpi', 'Resolução da imagem (DPI)', QgsProcessingParameterNumber.Integer, defaultValue=300, minValue=72, maxValue=600)
        dpi_param.setFlags(dpi_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(dpi_param)

    def processAlgorithm(self, parameters, context, model_feedback):

        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        outputs = {}

        script_directory = os.path.dirname(__file__)
        assets_path = os.path.join(script_directory, 'assets')
        template_path = os.path.join(assets_path, 'croqui.qpt')

        pasta_temp = os.path.join(self.parameterAsFile(parameters, 'pasta_do_ponto', context), 'temp')
        os.makedirs(pasta_temp, exist_ok=True)

        feedback.pushInfo('Carregando o template de layout...')
        # O native:atlaslayouttoimage resolve o parametro LAYOUT pelo NOME, e
        # procura esse nome no `context.project()`. Headless, no qgis_process, esse
        # projeto e None: o layout ficava registrado no QgsProject.instance(), que
        # o filho nao olha, e o unico sinal era 'Cannot find layout with name
        # "Croqui"' no stderr, sem JSON de saida. Medido em 2026-07-30, no QGIS
        # 4.2.0. Amarrar o contexto ao projeto singleton conserta os dois lados: na
        # GUI o context.project() ja vem preenchido e nada muda aqui.
        project = context.project()
        if project is None:
            project = QgsProject.instance()
            context.setProject(project)
        layout_manager = project.layoutManager()

        layout = QgsPrintLayout(project)

        template_document = QDomDocument()
        with open(template_path, 'r') as template_file:
            template_document.setContent(template_file.read())
        if not layout.loadFromTemplate(template_document, QgsReadWriteContext()):
            feedback.reportError('Falha ao carregar o layout do template.')
            return {}

        # O nome vem do template e o gerenciador indexa por ele. Registrar ANTES
        # de carregar deixaria o layout sem nome no indice, e o
        # native:atlaslayouttoimage nao acharia 'Croqui'.
        layout.setName('Croqui')
        layout_manager.addLayout(layout)

        map_item = layout.itemById('Mapa 1')
        if not map_item or not isinstance(map_item, QgsLayoutItemMap):
            feedback.reportError('Item de mapa não encontrado ou inválido.')
            return {}

        pontos_de_controle_layer = self.parameterAsVectorLayer(parameters, 'pontos_de_controle', context)

        atlas = layout.atlas()
        atlas.setEnabled(True)
        atlas.setCoverageLayer(pontos_de_controle_layer)
        atlas.setPageNameExpression('attribute("cod_ponto")')
        atlas.setFilenameExpression('attribute("cod_ponto")')
        atlas.setFilterFeatures(False)

        point_style_path = os.path.join(assets_path, 'estilo_ponto_controle.qml')
        style_ids = pontos_de_controle_layer.listStylesInDatabase()[1]
        for style_id in style_ids:
            pontos_de_controle_layer.deleteStyleFromDatabase(style_id)
        pontos_de_controle_layer.loadNamedStyle(point_style_path)
        pontos_de_controle_layer.triggerRepaint()

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # O atlas dirige o mapa, e por isso o quadro fica centrado no ponto da
        # pagina. So a ESCALA e fixa. Sem o setAtlasDriven o mapa fica parado na
        # extensao que veio do template, e todas as paginas saem do mesmo lugar:
        # o antigo setExtent(map_item.extent()) era um no-op que escondia isso.
        escala_satelite = self.parameterAsInt(parameters, 'escala_satelite', context)
        # O croqui.qpt vem com keepLayerSet="true" e um <LayerSet/> VAZIO. Assim o
        # quadro fica preso ao proprio conjunto de camadas, ignora o LAYERS que
        # este passo monta e desenha uma pagina BRANCA, com moldura e rotulo e sem
        # mapa. Medido em 2026-07-30: a imagem saia com 6,5% de pixel nao branco,
        # que era so a moldura e o texto. O vista_aerea.qpt do P08 ja vem com
        # keepLayerSet="false", e e por isso que o P08 nunca sofreu disto.
        map_item.setKeepLayerSet(False)
        map_item.setAtlasDriven(True)
        map_item.setAtlasScalingMode(QgsLayoutItemMap.Fixed)
        map_item.setScale(escala_satelite)
        layout.refresh()

        feedback.pushInfo('Gerando o croqui digital sobre a imagem de satélite...')
        alg_params = {
            'ANTIALIAS': True,
            'COVERAGE_LAYER': parameters['pontos_de_controle'],
            'DPI': self.parameterAsInt(parameters, 'dpi', context),
            'EXTENSION': indice_da_extensao('jpg'),
            # O nome do arquivo sai do CAMPO, e nao de @atlas_pagename. No QGIS
            # 4.0.0 aquela variavel volta vazia aqui, e as paginas se
            # sobrescreviam num unico arquivo com o nome da pasta.
            'FILENAME_EXPRESSION': '"cod_ponto"',
            'FILTER_EXPRESSION': '',
            'FOLDER': os.path.join(pasta_temp, 'satelite'),
            'GEOREFERENCE': False,
            'INCLUDE_METADATA': False,
            # A ORDEM e de cima para baixo: o PRIMEIRO da lista fica por cima.
            'LAYERS': [parameters['pontos_de_controle'], parameters['imagem_de_satelite']],
            'LAYOUT': 'Croqui',
            'SORTBY_EXPRESSION': '',
            'SORTBY_REVERSE': False
        }
        outputs['ExportaCroquiSatelite'] = processing.run('native:atlaslayouttoimage', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        feedback.pushInfo('Distribuindo o croqui nas estruturas de pasta...')
        folder_in = self.parameterAsFile(parameters, 'pasta_do_ponto', context)
        folder_aerview = os.path.join(pasta_temp, 'satelite')

        handle = HandleDistributeCroqui(folder_in, folder_aerview)
        handle.create_folder()
        falhas = handle.distribute_croqui()
        if falhas:
            # A pasta temporária FICA quando algo falhou. Apagá-la levava embora as
            # imagens que o atlas gerou, que são a única pista de qual passo
            # errou: nome diferente do esperado, formato diferente, ou nenhuma
            # imagem. Sem elas, diagnosticar exige rodar tudo de novo.
            feedback.reportError(
                f'{len(falhas)} croqui(s) não copiado(s):\n  ' +
                '\n  '.join(falhas[:15]) +
                f'\nAs imagens geradas ficaram em {pasta_temp} para conferência.')
        else:
            feedback.pushInfo(
                f'{len(handle.folders)} croqui(s) distribuído(s) em '
                f'{len(handle.folders)} pasta(s).')
            shutil.rmtree(pasta_temp)

        layout_manager.removeLayout(layout)
        style_ids = pontos_de_controle_layer.listStylesInDatabase()[1]
        for style_id in style_ids:
            pontos_de_controle_layer.deleteStyleFromDatabase(style_id)
        new_point_style_path = os.path.join(assets_path, 'estilo_ponto_controle_final.qml')
        pontos_de_controle_layer.loadNamedStyle(new_point_style_path)
        pontos_de_controle_layer.triggerRepaint()

        return {'resultado': 'Processamento Concluído'}

    def name(self):
        return 'distribuircroqui'

    def displayName(self):
        return self.tr('09 - Gerar e distribuir croqui digital na estrutura de pasta')

    def group(self):
        return self.tr("3. Documentar o ponto")

    def groupId(self):
        return "documentacao"

    def shortHelpString(self):
        return self.tr('''
            P09. Gera o croqui digital por atlas de layout, sobre imagem de satélite, e distribui na pasta 4_Croqui de cada ponto.

            Antes: a camada de pontos do croqui, digitalizada em campo sobre imagem de fundo. O gabarito com o estilo padrão é o arquivos/pontos_croqui.gpkg.
            Depois: P10, gerar a monografia.

            Por que este passo vem ANTES da monografia: o P10 usa o croqui digital com PRIORIDADE sobre o croqui manual. Numerado 15, como esteve até 2026-07-30, ele rodava depois do PDF já gerado, e o croqui digital não entrava em documento nenhum.

            Atenção:
            - A tabela de atributos precisa de cod_ponto, data_posicionamento e operador: é daí que o layout se preenche sozinho. A coluna observacao é opcional.
            - O arquivo sai como <PONTO>_CROQUI_DIGITAL.jpg, ao lado do croqui manual, que é o <PONTO>_CROQUI. Um não substitui o outro, e o P02 aceita qualquer um dos dois.
            - cod_ponto no padrão UF-HV-XXXX, sem zero à esquerda. A pasta BASE também entra, com QUATRO letras no tipo.
            - A escala é parâmetro avançado, com padrão 500 (1:500). O DPI também, com padrão 300.
            ''')

    def shortDescription(self):
        return self.tr(
            'P09. Gera o croqui digital por atlas de layout, sobre imagem de satélite, e distribui na pasta 4_Croqui de cada ponto. Roda antes da monografia, que o consome.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):

        return DistributeCroqui()
