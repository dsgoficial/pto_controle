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

from qgis.core import (QgsCoordinateTransform, QgsFeature, QgsGeometry,
                       QgsLayoutItemMap, QgsPrintLayout, QgsProcessing,
                       QgsProcessingAlgorithm, QgsProcessingException,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFile, QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer, QgsProject,
                       QgsReadWriteContext, QgsSpatialIndex, QgsVectorLayer)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtXml import QDomDocument

import processing

from .handleDistributeImages import HandleDistributeImages


class DistributeImages(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('pontos_de_controle', 'Pontos de controle', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('imagem_de_satelite', 'Imagem de Satelite', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('pasta_do_ponto', 'Selecione a pasta com a(s) estrutura(s) de pontos de controle', behavior=QgsProcessingParameterFile.Folder, fileFilter='Todos os arquivos (*.*)', defaultValue='C:'))

        # As malhas vem dentro do plugin. Os dois parametros abaixo so existem
        # para o caso raro de precisar de outra malha; em branco, usa a do plugin.
        estados_param = QgsProcessingParameterVectorLayer('estados', 'Estados (em branco usa a malha do plugin)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None, optional=True)
        estados_param.setFlags(estados_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(estados_param)

        municipios_param = QgsProcessingParameterVectorLayer('municipios', 'Municipios (em branco usa a malha do plugin)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None, optional=True)
        municipios_param.setFlags(municipios_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(municipios_param)

        escala_satelite_param = QgsProcessingParameterNumber('escala_satelite', 'Escala para Satélite', QgsProcessingParameterNumber.Integer, defaultValue=1000)
        escala_satelite_param.setFlags(escala_satelite_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(escala_satelite_param)

        # A vista municipal e a estadual NAO tem escala fixa. Cada uma enquadra a
        # feicao que contem o ponto, e esta margem e a folga em volta dela.
        margem_param = QgsProcessingParameterNumber('margem', 'Margem em volta do município e do estado (%)', QgsProcessingParameterNumber.Integer, defaultValue=5, minValue=0, maxValue=50)
        margem_param.setFlags(margem_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(margem_param)

    # -------------------------------------------------------------------------

    def _malha_do_plugin(self, assets_path, arquivo, camada, rotulo, feedback):
        caminho = os.path.join(assets_path, arquivo)
        malha = QgsVectorLayer(f'{caminho}|layername={camada}', rotulo, 'ogr')
        if not malha.isValid():
            raise QgsProcessingException(f'Falha ao carregar {arquivo} do plugin.')
        return malha

    def _camada_de_quadros(self, pontos, poligonos, nome, feedback):
        """Uma feicao por ponto, com a geometria do poligono que o contem.

        Essa camada faz dois papeis. E a cobertura do atlas, e por isso o quadro
        de cada pagina sai da extensao do municipio ou do estado daquele ponto, e
        nao de uma escala fixa. E tambem a camada desenhada, o que deixa na imagem
        so o municipio (ou o estado) do ponto, como manda a monografia.

        Os campos do poligono viajam junto porque os estilos rotulam por eles:
        qml_municipio.qml usa NM_MUN e qml_estado.qml usa NM_UF.
        """
        campos_origem = [c for c in poligonos.fields() if c.name().lower() != 'fid']

        quadros = QgsVectorLayer(
            f'MultiPolygon?crs={poligonos.crs().authid()}&field=cod_ponto:string',
            nome, 'memory')
        quadros.dataProvider().addAttributes(campos_origem)
        quadros.updateFields()

        indice = QgsSpatialIndex(poligonos.getFeatures())
        transformacao = QgsCoordinateTransform(
            pontos.crs(), poligonos.crs(), QgsProject.instance())
        precisa_transformar = pontos.crs() != poligonos.crs()

        novas = []
        sem_dono = []
        for ponto in pontos.getFeatures():
            codigo = ponto['cod_ponto']
            geom = QgsGeometry(ponto.geometry())
            if precisa_transformar:
                geom.transform(transformacao)

            dono = self._quem_contem(poligonos, indice, geom)
            if dono is None:
                sem_dono.append(str(codigo))
                continue

            nova = QgsFeature(quadros.fields())
            nova['cod_ponto'] = codigo
            for campo in campos_origem:
                nova[campo.name()] = dono[campo.name()]
            nova.setGeometry(dono.geometry())
            novas.append(nova)

        quadros.dataProvider().addFeatures(novas)
        quadros.updateExtents()

        if sem_dono:
            feedback.reportError(
                f'{nome}: {len(sem_dono)} ponto(s) sem feição que os contenha, e '
                f'sem vizinha proxima: {", ".join(sem_dono[:10])}. '
                'Esses pontos ficam sem a imagem.')
        return quadros

    def _quem_contem(self, poligonos, indice, geom):
        """O poligono que contem o ponto. Sem nenhum, o mais proximo.

        O ponto pode cair sobre o limite (contains falha, intersects pega) ou
        fora da malha, na faixa de praia e na ilha que a malha nao desenha. Nesse
        caso vale o vizinho mais proximo, que e o municipio de fato.
        """
        candidatos = indice.intersects(geom.boundingBox())
        for fid in candidatos:
            if poligonos.getFeature(fid).geometry().contains(geom):
                return poligonos.getFeature(fid)
        for fid in candidatos:
            if poligonos.getFeature(fid).geometry().intersects(geom):
                return poligonos.getFeature(fid)
        vizinhos = indice.nearestNeighbor(geom, 1)
        if vizinhos:
            return poligonos.getFeature(vizinhos[0])
        return None

    def _indice_da_extensao(self, nome='jpg'):
        """A posicao de 'jpg' na lista de formatos do atlaslayouttoimage.

        A lista muda de uma versao do QGIS para outra. No QGIS 4.0.0 o indice 5 e
        'jpeg' e o 6 e 'jpg'; o codigo antigo fixava 5, entao as imagens saiam
        como .jpeg e o HandleDistributeImages, que procura .jpg, nao achava nada.
        """
        from qgis.core import QgsApplication
        alg = QgsApplication.processingRegistry().algorithmById('native:atlaslayouttoimage')
        if alg is not None:
            for definicao in alg.parameterDefinitions():
                if definicao.name() == 'EXTENSION':
                    opcoes = list(definicao.options())
                    if nome in opcoes:
                        return opcoes.index(nome)
        return 6

    def _exportar(self, cobertura, camadas, pasta, context, feedback):
        return processing.run('native:atlaslayouttoimage', {
            'ANTIALIAS': True,
            'COVERAGE_LAYER': cobertura,
            'DPI': 300,
            'EXTENSION': self._indice_da_extensao('jpg'),
            # O nome do arquivo sai do CAMPO, e nao de @atlas_pagename. No QGIS
            # 4.0.0 aquela variavel volta vazia aqui, e as quatro paginas se
            # sobrescreviam num unico arquivo com o nome da pasta.
            'FILENAME_EXPRESSION': '"cod_ponto"',
            'FILTER_EXPRESSION': '',
            'FOLDER': pasta,
            'GEOREFERENCE': False,
            'INCLUDE_METADATA': False,
            'LAYERS': camadas,
            'LAYOUT': 'Vista Aerea',
            'SORTBY_EXPRESSION': '',
            'SORTBY_REVERSE': False
        }, context=context, feedback=feedback, is_child_algorithm=True)

    # -------------------------------------------------------------------------

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        outputs = {}

        script_directory = os.path.dirname(__file__)
        assets_path = os.path.join(script_directory, 'assets')
        template_path = os.path.join(assets_path, 'vista_aerea.qpt')

        pontos_de_controle_layer = self.parameterAsVectorLayer(parameters, 'pontos_de_controle', context)

        estados_layer = self.parameterAsVectorLayer(parameters, 'estados', context)
        if estados_layer is None:
            estados_layer = self._malha_do_plugin(assets_path, 'estados.gpkg', 'estados', 'Estados', feedback)
        municipios_layer = self.parameterAsVectorLayer(parameters, 'municipios', context)
        if municipios_layer is None:
            municipios_layer = self._malha_do_plugin(assets_path, 'municipios.gpkg', 'municipios', 'Municípios', feedback)

        pasta_temp = os.path.join(self.parameterAsFile(parameters, 'pasta_do_ponto', context), 'temp')
        os.makedirs(pasta_temp, exist_ok=True)

        feedback.pushInfo('Carregando o template de layout...')
        project = QgsProject.instance()
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
        # native:atlaslayouttoimage nao acharia 'Vista Aerea'.
        layout.setName('Vista Aerea')
        layout_manager.addLayout(layout)

        map_item = layout.itemById('Map 1')
        if not map_item or not isinstance(map_item, QgsLayoutItemMap):
            feedback.reportError('Item de mapa não encontrado ou inválido.')
            return {}

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

        # --- as duas coberturas de enquadramento -----------------------------
        # Antes as duas vistas usavam escala fixa (1:25.000 e 1:2.000.000) centrada
        # no PONTO. A 1:2.000.000 o quadro cobre 200 km e o Rio Grande do Sul tem
        # 600 km, entao o quadro caia inteiro dentro do estado e a imagem saia em
        # branco, so com o simbolo do ponto. Agora o quadro sai da extensao da
        # feicao que contem o ponto.
        feedback.pushInfo('Descobrindo o município e o estado de cada ponto...')
        quadros_municipio = self._camada_de_quadros(
            pontos_de_controle_layer, municipios_layer, 'quadro_municipio', feedback)
        quadros_estado = self._camada_de_quadros(
            pontos_de_controle_layer, estados_layer, 'quadro_estado', feedback)

        quadros_municipio.loadNamedStyle(os.path.join(assets_path, 'qml_municipio.qml'))
        quadros_estado.loadNamedStyle(os.path.join(assets_path, 'qml_estado.qml'))
        project.addMapLayer(quadros_municipio, False)
        project.addMapLayer(quadros_estado, False)

        margem = self.parameterAsInt(parameters, 'margem', context) / 100.0

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # --- vista aerea: escala fixa, centrada no ponto ----------------------
        feedback.pushInfo('Gerando a vista aérea...')
        # O atlas continua dirigindo o mapa, e por isso o quadro fica centrado no
        # ponto da pagina. So a ESCALA e fixa aqui. Desligar o atlas deixaria o
        # mapa parado na extensao que veio do template.
        map_item.setAtlasDriven(True)
        map_item.setAtlasScalingMode(QgsLayoutItemMap.Fixed)
        map_item.setScale(self.parameterAsDouble(parameters, 'escala_satelite', context))
        atlas.setCoverageLayer(pontos_de_controle_layer)
        outputs['ExportaVistaAereaSatelite'] = self._exportar(
            pontos_de_controle_layer,
            # A ORDEM e de cima para baixo: o PRIMEIRO da lista fica por cima.
            [parameters['pontos_de_controle'], parameters['imagem_de_satelite']],
            os.path.join(pasta_temp, 'satelite'), context, feedback)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # --- vista estadual: enquadra o estado do ponto -----------------------
        feedback.pushInfo('Gerando a vista estadual...')
        # Fundo branco. Na vista aerea o raster cobre tudo e a cor nao aparece;
        # nas duas vistas de localizacao ela e o papel em volta do poligono.
        map_item.setBackgroundColor(QColor(255, 255, 255))
        map_item.setAtlasDriven(True)
        map_item.setAtlasScalingMode(QgsLayoutItemMap.Auto)
        map_item.setAtlasMargin(margem)
        outputs['ExportaVistaEstado'] = self._exportar(
            quadros_estado,
            [parameters['pontos_de_controle'], quadros_estado],
            os.path.join(pasta_temp, 'estado'), context, feedback)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # --- vista municipal: enquadra o municipio do ponto -------------------
        feedback.pushInfo('Gerando a vista municipal...')
        outputs['ExportaVistaMunicipio'] = self._exportar(
            quadros_municipio,
            [parameters['pontos_de_controle'], quadros_municipio],
            os.path.join(pasta_temp, 'municipio'), context, feedback)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        feedback.pushInfo('Distribuindo imagens nas estruturas de pasta...')
        folder_in = self.parameterAsFile(parameters, 'pasta_do_ponto', context)
        handle = HandleDistributeImages(
            folder_in,
            os.path.join(pasta_temp, 'satelite'),
            os.path.join(pasta_temp, 'municipio'),
            os.path.join(pasta_temp, 'estado'))
        handle.create_folder()
        falhas = handle.distribute_images()
        if falhas:
            feedback.reportError(
                f'{len(falhas)} imagem(ns) não copiada(s):\n  ' +
                '\n  '.join(falhas[:15]))
        else:
            feedback.pushInfo(
                f'{len(handle.folders) * 3} imagens distribuídas em '
                f'{len(handle.folders)} pasta(s).')

        feedback.setCurrentStep(7)
        shutil.rmtree(pasta_temp)

        project.removeMapLayer(quadros_municipio.id())
        project.removeMapLayer(quadros_estado.id())
        layout_manager.removeLayout(layout)

        style_ids = pontos_de_controle_layer.listStylesInDatabase()[1]
        for style_id in style_ids:
            pontos_de_controle_layer.deleteStyleFromDatabase(style_id)
        new_point_style_path = os.path.join(assets_path, 'estilo_ponto_controle_final.qml')
        pontos_de_controle_layer.loadNamedStyle(new_point_style_path)
        pontos_de_controle_layer.triggerRepaint()

        return {'resultado': 'Processamento Concluído'}

    def name(self):
        return 'distribuirvistas'

    def displayName(self):
        return self.tr('08 - Distribuir vistas aéreas na estrutura de pasta')

    def group(self):
        return self.tr("Pós-processamento")

    def groupId(self):
        return "posprocessamento"

    def shortHelpString(self):
        return self.tr('''
            P08. Gera pelo compositor de impressão três vistas de cada ponto (local por imagem de satélite, municipal e estadual) e distribui na pasta 7_Imagens_Monografia.

            Antes: P07, com a camada de pontos carregada do banco.
            Depois: P09, gerar a monografia.

            Atenção:
            - A camada de pontos precisa da coluna cod_ponto preenchida.
            - As malhas de município e de estado vêm dentro do plugin (malha do IBGE de 2022, já simplificada para o tamanho da imagem). Só preencha os parâmetros avançados de estados e municípios para usar outra malha.
            - A rotina aplica os PRÓPRIOS estilos, que vêm dentro do plugin.
            - A vista municipal e a estadual enquadram a feição que contém o ponto. Não têm escala fixa. Ajuste a folga em volta pelo parâmetro avançado de margem.
            - Só a vista aérea tem escala fixa, porque nela o enquadramento é o do próprio ponto.
            ''')

    def shortDescription(self):
        return self.tr(
            'P08. Gera pelo compositor de impressão três vistas de cada ponto (local por imagem de satélite, municipal e estadual) e distribui na pasta 7_Imagens_Monografia.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DistributeImages()
