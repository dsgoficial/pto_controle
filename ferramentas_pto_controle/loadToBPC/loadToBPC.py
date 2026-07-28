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
import sqlite3
from datetime import datetime
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


def _cpf_so_digitos(valor):
    """O que o `regexp_replace(cpf, '\\D','','g')` do PostGIS fazia.

    O SQLite não tem regexp_replace, então a limpeza vem para o Python. Devolve
    None quando não sobra digito, que é o `NULLIF(..., '')` do original.
    """
    if not valor:
        return None
    digitos = re.sub(r'\D', '', str(valor))
    return digitos or None


def _tempo_rastreio(inicio, fim):
    """O que o `(fim_rastreio - inicio_rastreio)` do PostGIS fazia.

    ARMADILHA que motiva esta função: no SQLite a subtracao de duas colunas de
    texto não da erro, da ZERO. O tempo de rastreio iria zerado para o BPC sem
    ninguém notar. Medido em 2026-07-28.

    Devolve HH:MM:SS, ou None quando falta uma das pontas.
    """
    if not inicio or not fim:
        return None
    for formato in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ',
                    '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%d %H:%M:%S'):
        try:
            i = datetime.strptime(str(inicio), formato)
            f = datetime.strptime(str(fim), formato)
        except ValueError:
            continue
        segundos = int((f - i).total_seconds())
        sinal = '-' if segundos < 0 else ''
        segundos = abs(segundos)
        return '{}{:02d}:{:02d}:{:02d}'.format(
            sinal, segundos // 3600, (segundos % 3600) // 60, segundos % 60
        )
    return None


def exportar_para_bpc(missao, sql, destino):
    """Escreve o GeoPackage que vai ao BPC. Devolve quantos pontos sairam.

    Substitui a chamada ao `ogr2ogr` contra o PostGIS. Duas expressoes do SQL
    antigo não atravessam para o SQLite e foram para o Python: a limpeza do CPF
    (não ha regexp_replace) e o tempo de rastreio (a subtracao devolveria zero em
    silêncio). O resto do SELECT continua sendo SQL, para a lista de colunas e os
    apelidos permanecerem os mesmos que o BPC já espera.
    """
    from osgeo import ogr, osr

    from ..utils.missao import conecta

    destino = Path(destino)
    if destino.exists():
        destino.unlink()

    con = conecta(missao)
    con.row_factory = sqlite3.Row
    linhas = con.execute(sql).fetchall()
    con.close()

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4674)
    ds = ogr.GetDriverByName('GPKG').CreateDataSource(str(destino))
    layer = ds.CreateLayer('pontos_exportados', srs, ogr.wkbPoint)

    # As colunas de saida são as do SELECT, menos as duas cruas que viram
    # calculadas aqui, mais os dois campos derivados.
    cruas = {'cpf_engenheiro_responsavel', 'inicio_rastreio', 'fim_rastreio', 'geom'}
    colunas = [c for c in (linhas[0].keys() if linhas else []) if c not in cruas]
    saida = colunas + ['cpf_responsavel', 'tempo_rastreio']
    for nome in saida:
        layer.CreateField(ogr.FieldDefn(nome, ogr.OFTString))

    definicao = layer.GetLayerDefn()
    for linha in linhas:
        feat = ogr.Feature(definicao)
        for nome in colunas:
            valor = linha[nome]
            if valor is not None:
                feat.SetField(nome, str(valor))
        cpf = _cpf_so_digitos(linha['cpf_engenheiro_responsavel'])
        if cpf:
            feat.SetField('cpf_responsavel', cpf)
        tempo = _tempo_rastreio(linha['inicio_rastreio'], linha['fim_rastreio'])
        if tempo:
            feat.SetField('tempo_rastreio', tempo)
        if linha['geom'] is not None:
            from ..utils.missao import _wkb_de
            feat.SetGeometry(ogr.CreateGeometryFromWkb(_wkb_de(linha['geom'])))
        layer.CreateFeature(feat)
    ds = None
    return len(linhas)


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
    MISSAO = 'MISSAO'
    TYPE = 'TYPE'

    def initAlgorithm(self, config=None):
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
            QgsProcessingParameterFile(
                self.MISSAO,
                self.tr('Arquivo da missão (GeoPackage), criado no P01'),
                extension='gpkg'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        process_type = self.parameterAsInt(parameters, self.TYPE, context)
        folder_in = self.parameterAsFile(parameters, self.FOLDERIN, context)
        folder_out = self.parameterAsFile(parameters, self.FOLDEROUT, context)
        missao = self.parameterAsFile(parameters, self.MISSAO, context)

        handle = HandleLoadToBPC(folder_in, folder_out, process_type)
        temp_folder = QgsProcessingUtils.tempFolder()
        where_clausule = handle.getWhereClausule(temp_folder, process_type)

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
  cpf_engenheiro_responsavel,
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
  inicio_rastreio,
  fim_rastreio,
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
        sql_string = f"SELECT {multilinestring} FROM ponto_controle_p {where_clausule}"

        gpkg_path = Path(folder_out, 'pontos_exportados.gpkg')
        exportados = exportar_para_bpc(missao, sql_string, gpkg_path)
        feedback.pushInfo(f'Pontos exportados para o BPC: {exportados}')

        if exportados == 0:
            feedback.reportError(
                'Nenhum ponto passou nos critérios do BPC. Os mais comuns são '
                'órbita diferente de FINAL, campo de domínio ainda em 9999 e '
                'data de processamento em branco.'
            )

        if process_type == 0:
            return {self.OUTPUT: 'Processamento Concluído. Pontos não exportados para Geopackage podem ter apresentado inconsistências no metadado, consulte a missão para verificar as informações.'}
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
        return 'prepararbpc'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('10 - Preparar insumos para carregamento no BPC')

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
        return self.tr('''
            P10. Monta os insumos para subir ao Banco de Pontos de Controle da DSG: um .zip por ponto e o GeoPackage pontos_exportados.gpkg.

            Antes: P09, monografias geradas.
            Depois: o carregamento é MANUAL e fora do plugin. Suba os .zip por SFTP e depois carregue o .gpkg em "Adicionar Geopackage", na página web do BPC.

            Atenção:
            - A pasta de entrada precisa de um CSV com a coluna cod_ponto, listando os pontos que vão ao BPC.
            - No ramo PPP, só entram os pontos com ÓRBITA FINAL. Ponto com órbita rápida fica de fora em silêncio, mesmo estando no CSV.
            - Ponto cujo código tenha BASE no meio (por exemplo RS-BASE-5) é descartado.
            - Desde a troca do PostgreSQL pelo GeoPackage, a exportação é feita pelo próprio plugin. Não exige mais o ogr2ogr no PATH.
            - Quer o pacote COMPLETO da missão, sem esses filtros? É o P17, que prepara para o Controle do Acervo.
            ''')

    def shortDescription(self):
        return self.tr(
            'P10. Monta os insumos para subir ao Banco de Pontos de Controle da DSG: um .zip por ponto e o GeoPackage pontos_exportados.gpkg.'
        )

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LoadToBPC()
