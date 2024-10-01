# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PontoControle
                                 A QGIS plugin
 Ferramentas para a gerência de pontos de controle
                              -------------------
        begin                : 2020-01-07
        copyright            : (C) 2020 by 1CGEO/DSG
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
__date__ = '2024-09-09'
__copyright__ = '(C) 2024 by 1CGEO/DSG'

__revision__ = '$Format:%H$'

import os
import shutil
from qgis.core import QgsProcessing, QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback, QgsProcessingParameterVectorLayer, QgsProcessingParameterFile, QgsProcessingParameterRasterLayer, QgsProcessingParameterNumber, QgsProcessingParameterDefinition, QgsProject, QgsPrintLayout, QgsLayoutItemMap, QgsReadWriteContext, QgsVectorLayer
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtCore import QCoreApplication
import processing
from .handleDistributeImages import HandleDistributeImages


class DistributeImages(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('pontos_de_controle', 'Pontos de controle', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estados', 'Estados', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('municipios', 'Municipios', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('imagem_de_satelite', 'Imagem de Satelite', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('pasta_do_ponto', 'Selecione a pasta com a(s) estrutura(s) de pontos de controle', behavior=QgsProcessingParameterFile.Folder, fileFilter='Todos os arquivos (*.*)', defaultValue='C:'))

        escala_satelite_param = QgsProcessingParameterNumber('escala_satelite', 'Escala para Satélite', QgsProcessingParameterNumber.Integer, defaultValue=1000)
        escala_satelite_param.setFlags(escala_satelite_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(escala_satelite_param)

        escala_municipio_param = QgsProcessingParameterNumber('escala_municipio', 'Escala para Município', QgsProcessingParameterNumber.Integer, defaultValue=25000)
        escala_municipio_param.setFlags(escala_municipio_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(escala_municipio_param)

        escala_estado_param = QgsProcessingParameterNumber('escala_estado', 'Escala para Estado', QgsProcessingParameterNumber.Integer, defaultValue=2000000)
        escala_estado_param.setFlags(escala_estado_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(escala_estado_param)

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        outputs = {}

        script_directory = os.path.dirname(__file__)
        assets_path = os.path.join(script_directory, 'assets')
        template_path = os.path.join(assets_path, 'vista_aerea.qpt')

        pais_path = os.path.join(assets_path, 'PAIS.gpkg')
        pais_layer = QgsVectorLayer(f"{pais_path}|layername=geoft_pais", 'País', 'ogr')

        if not pais_layer.isValid():
            feedback.reportError('Falha ao carregar a camada PAIS.gpkg.')
            return {}

        pasta_temp = os.path.join(self.parameterAsFile(parameters, 'pasta_do_ponto', context), 'temp')
        os.makedirs(pasta_temp, exist_ok=True)

        feedback.pushInfo('Carregando o template de layout...')
        project = QgsProject.instance()
        layout_manager = project.layoutManager()

        layout = QgsPrintLayout(project)
        if layout is None:
            layout = QgsPrintLayout(project)
        layout_manager.addLayout(layout)

        template_document = QDomDocument()
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
            template_document.setContent(template_content)
        read_write_context = QgsReadWriteContext()
        success = layout.loadFromTemplate(template_document, read_write_context)
        if not success:
            feedback.reportError('Falha ao carregar o layout do template.')
            return {}

        map_item = layout.itemById('Map 1')
        if not map_item or not isinstance(map_item, QgsLayoutItemMap):
            feedback.reportError('Item de mapa não encontrado ou inválido.')
            return {}

        pontos_de_controle_layer = self.parameterAsVectorLayer(parameters, 'pontos_de_controle', context)

        atlas = layout.atlas()
        atlas.setEnabled(True)
        atlas.setCoverageLayer(pontos_de_controle_layer)
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

        state_style_path = os.path.join(assets_path, 'qml_estado.qml')
        alg_params = {
            'INPUT': parameters['estados'],
            'STYLE': state_style_path
        }
        outputs['EstiloEstado'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        escala_satelite = self.parameterAsDouble(parameters, 'escala_satelite', context)
        map_item.setScale(escala_satelite)
        alg_params = {
            'ANTIALIAS': True,
            'COVERAGE_LAYER': parameters['pontos_de_controle'],
            'DPI': 300,
            'EXTENSION': 5,
            'FILENAME_EXPRESSION': "@atlas_pagename",
            'FILTER_EXPRESSION': '',
            'FOLDER': os.path.join(pasta_temp, 'satelite'),
            'GEOREFERENCE': False,
            'INCLUDE_METADATA': False,
            'LAYERS': [parameters['pontos_de_controle'], parameters['imagem_de_satelite']],
            'LAYOUT': 'Vista Aerea',
            'SORTBY_EXPRESSION': '',
            'SORTBY_REVERSE': False
        }
        outputs['ExportaVistaAereaSatelite'] = processing.run('native:atlaslayouttoimage', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        city_style_path = os.path.join(assets_path, 'qml_municipio.qml')
        alg_params = {
            'INPUT': parameters['municipios'],
            'STYLE': city_style_path
        }
        outputs['EstiloMunicipio'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        escala_estado = self.parameterAsDouble(parameters, 'escala_estado', context)
        map_item.setScale(escala_estado)
        alg_params = {
            'ANTIALIAS': True,
            'COVERAGE_LAYER': parameters['pontos_de_controle'],
            'DPI': 300,
            'EXTENSION': 5,
            'FILENAME_EXPRESSION': "@atlas_pagename",
            'FILTER_EXPRESSION': '',
            'FOLDER': os.path.join(pasta_temp, 'estado'),
            'GEOREFERENCE': False,
            'INCLUDE_METADATA': False,
            'LAYERS': [parameters['pontos_de_controle'], pais_layer, parameters['estados']],
            'LAYOUT': 'Vista Aerea',
            'SORTBY_EXPRESSION': '',
            'SORTBY_REVERSE': False
        }
        outputs['ExportaVistaAereaEstados'] = processing.run('native:atlaslayouttoimage', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        escala_municipio = self.parameterAsDouble(parameters, 'escala_municipio', context)
        map_item.setScale(escala_municipio)
        alg_params = {
            'ANTIALIAS': True,
            'COVERAGE_LAYER': parameters['pontos_de_controle'],
            'DPI': 300,
            'EXTENSION': 5,
            'FILENAME_EXPRESSION': "@atlas_pagename",
            'FILTER_EXPRESSION': '',
            'FOLDER': os.path.join(pasta_temp, 'municipio'),
            'GEOREFERENCE': False,
            'INCLUDE_METADATA': False,
            'LAYERS': [parameters['pontos_de_controle'], pais_layer, parameters['municipios']],
            'LAYOUT': 'Vista Aerea',
            'SORTBY_EXPRESSION': '',
            'SORTBY_REVERSE': False
        }
        outputs['ExportaVistaAereaMunicipios'] = processing.run('native:atlaslayouttoimage', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        feedback.pushInfo('Distribuindo imagens nas estruturas de pasta...')
        folder_in = self.parameterAsFile(parameters, 'pasta_do_ponto', context)
        folder_aerview = os.path.join(pasta_temp, 'satelite')
        folder_view1 = os.path.join(pasta_temp, 'municipio')
        folder_view2 = os.path.join(pasta_temp, 'estado')

        handle = HandleDistributeImages(folder_in, folder_aerview, folder_view1, folder_view2)
        handle.create_folder()
        handle.distribute_images()

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
        return '08 - Distribuir vistas aéreas na estrutura de pasta'

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr("Pós-processamento")

    def groupId(self):
        return "posprocessamento"

    def shortHelpString(self):
        return self.tr('''
        Esta ferramenta gera e distribui as imagens aéreas dos pontos em estrutura de pastas.
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        
        return DistributeImages()
