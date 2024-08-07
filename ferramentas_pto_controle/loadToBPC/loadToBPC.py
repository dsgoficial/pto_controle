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

import subprocess
from pathlib import Path
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber, QgsProcessingUtils,
                       QgsProcessingParameterEnum)
from qgis.PyQt.QtCore import QCoreApplication
from .handleLoadToBPC import HandleLoadToBPC


class LoadToBPC(QgsProcessingAlgorithm):
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
    FOLDERIN = 'FOLDERIN'
    FOLDEROUT = 'FOLDEROUT'
    SERVERIP = 'SERVERIP'
    PORT = 'PORT'
    BDNAME = 'BDNAME'
    USER = 'USER'
    PASSWORD = 'PASSWORD'
    TYPE = 'TYPE'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterEnum(
                self.TYPE,
                self.tr('Selecione o método de processamento:'),
                options = [self.tr('PPP'), self.tr('RTE')]
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDERIN,
                self.tr('Selecione a pasta com a estrutura de pontos de controle'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDEROUT,
                self.tr('Selecione a pasta na qual serão gerados os arquivos:'),
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.SERVERIP,
                self.tr('Insira o IP do computador')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PORT,
                self.tr('Insira a porta')
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.BDNAME,
                self.tr('Insira o nome do banco de dados'),
            )
        )

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
        process_type = self.parameterAsInt(parameters, self.TYPE, context)
        folder_in = self.parameterAsFile(parameters, self.FOLDERIN, context)
        folder_out = self.parameterAsFile(parameters, self.FOLDEROUT, context)
        server_ip = self.parameterAsString(parameters, self.SERVERIP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        bdname = self.parameterAsString(parameters, self.BDNAME, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)

        handle = HandleLoadToBPC(folder_in, folder_out, process_type)
        temp_folder = QgsProcessingUtils.tempFolder()
        where_clausule = handle.getWhereClausule(temp_folder, process_type)

        db_string = "PG:dbname={} host={} port={} user={} password={}".format(
            bdname, server_ip, port, user, password)
    

        multilinestring = '''id,
  cod_ponto,
  cast(data_rastreio AS varchar) as data_medicao,
  tipo_ref,
  latitude,
  longitude,
  norte as coord_n,
  leste as coord_e,
  altitude_ortometrica,
  altitude_geometrica,
  sistema_geodesico,
  outra_ref_plan,
  referencial_altim,
  outro_ref_alt,
  fuso,
  meridiano_central,
  tipo_situacao,
  reserva,
  lote,
  latitude_planejada,
  longitude_planejada,
  medidor as operador_medicao,
  classificacao_ponto,
  observacao,
  metodo_posicionamento as metodo_medicao,
  ponto_base,
  materializado,
  altura_antena,
  tipo_medicao_altura,
  referencia_medicao_altura as ref_med_altura,
  altura_objeto,
  mascara_elevacao,
  taxa_gravacao,
  modelo_gps,
  modelo_antena,
  numero_serie_gps as nr_serie_receptor,
  numero_serie_antena as nr_serie_antena,
  modelo_geoidal,
  precisao_horizontal_esperada as precisao_horizontal,
  precisao_vertical_esperada as precisao_vertical,
  freq_processada,
  data_processamento,
  orbita,
  orgao_executante,
  projeto,
  engenheiro_responsavel as nome_responsavel,
  crea_engenheiro_responsavel as crea_responsavel,
  NULLIF(regexp_replace(cpf_engenheiro_responsavel, '\D','','g'), '')::text as cpf_responsavel,
  geometria_aproximada,
  tipo_pto_ref_geod_topo,
  tipo_marco_limite,
  rede_referencia,
  referencial_grav,
  situacao_marco,
  data_visita,
  valor_gravidade,
  possui_monografia,
  numero_fotos,
  possui_croqui,
  possui_arquivo_rastreio,
  4674 as EPSG,
  cod_ponto||'.zip' as anexos,
  (fim_rastreio - inicio_rastreio) as tempo_rastreio,
  geom
'''
        clausule_validate_bpc = '''
  AND tipo_situacao IN (3)
  AND sistema_geodesico NOT IN (9999)
  AND referencial_altim NOT IN (9999)
  AND referencia_medicao_altura NOT IN (9999)
  AND tipo_medicao_altura NOT IN (9999)
  AND tipo_ref NOT IN (9999)
  AND classificacao_ponto NOT IN (9999)
  AND data_rastreio IS NOT NULL
  AND situacao_marco NOT IN (9999)
  AND metodo_posicionamento NOT IN (9999)
  AND tipo_pto_ref_geod_topo NOT IN (9999)
  AND tipo_marco_limite NOT IN (9999)
  AND rede_referencia NOT IN (9999)
  AND referencial_grav NOT IN (9999)
  AND mascara_elevacao IS NOT NULL
  AND data_processamento IS NOT NULL
  AND inicio_rastreio IS NOT NULL
  AND fim_rastreio IS NOT NULL
  AND engenheiro_responsavel IS NOT NULL
'''
        where_clausule = where_clausule + clausule_validate_bpc
        sql_string = f"SELECT {multilinestring} FROM bpc.ponto_controle_p {where_clausule}"

        gpkg_path = Path(folder_out, 'pontos_exportados.gpkg')

        subprocess.run(["ogr2ogr", "-f", "GPKG", f"{gpkg_path}", f"{db_string}", "-sql", f"{sql_string}", "-nln", "pontos_exportados"])

        if process_type == 0:
            return {self.OUTPUT: 'Processamento Concluído. Pontos não exportados para Geopackage podem ter apresentado inconsistências no metadado, consulte o banco para verificar as informações.'}
        else:
            return {self.OUTPUT: 'Processamento Concluído'}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '10 - Preparar insumos para carregamento no BPC'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Pós-processamento")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "posprocessamento"

    def shortHelpString(self):
        """
        Retruns a short helper string for the algorithm
        """
        return self.tr('''
        Esta ferramenta gera os insumos necessários para carregamento no BPC: o arquivo GeoPackage e o(s) arquivo(s) zipados.
        ''')

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LoadToBPC()
