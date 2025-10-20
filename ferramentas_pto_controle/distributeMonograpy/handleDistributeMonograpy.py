# -*- coding: utf-8 -*-
import os
from pathlib import Path
import psycopg2
import psycopg2.extras
from qgis.core import (
    QgsProject,
    QgsPrintLayout,
    QgsLayoutExporter,
    QgsReadWriteContext,
)
from qgis.PyQt.QtXml import QDomDocument

class HandleDistributeMonografia:
    def __init__(self, conn, path, template_qpt, settings=None, digital=True, feedback=None, tipo_modelo=None):
        self.conn = conn
        self.path = Path(path)
        self.template_qpt = template_qpt
        self.settings = settings or {}
        self.digital = digital
        self.feedback = feedback
        self.tipo_modelo = tipo_modelo

    def log(self, msg):
        if self.feedback:
            self.feedback.pushInfo(msg)
        else:
            print(msg)

    def fetchPointData(self, cod_ponto):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT * ,
                    dominios.tipo_ref.code_name as tipo_ref1,
                    dominios.metodo_posicionamento.code_name as metodo_pos,
                    dominios.referencial_altim.code_name as referencial_altim1,
                    dominios.sistema_geodesico.code_name as sistema_geodesico1,
                    dominios.orbita.code_name as orbita1,
                    dominios.referencia_medicao_altura.code_name as refalt
                FROM bpc.ponto_controle_p
                INNER JOIN dominios.tipo_ref ON dominios.tipo_ref.code = bpc.ponto_controle_p.tipo_ref
                INNER JOIN dominios.metodo_posicionamento ON dominios.metodo_posicionamento.code = bpc.ponto_controle_p.metodo_posicionamento
                INNER JOIN dominios.referencial_altim ON dominios.referencial_altim.code = bpc.ponto_controle_p.referencial_altim
                INNER JOIN dominios.sistema_geodesico ON dominios.sistema_geodesico.code = bpc.ponto_controle_p.sistema_geodesico
                INNER JOIN dominios.orbita ON dominios.orbita.code = bpc.ponto_controle_p.orbita
                INNER JOIN dominios.referencia_medicao_altura ON dominios.referencia_medicao_altura.code = bpc.ponto_controle_p.referencia_medicao_altura
                WHERE cod_ponto = %s
            """, (cod_ponto,))
            return cur.fetchone()

    def getFoldersFromStructure(self):
        import re
        folders = [x for x in self.path.rglob(
            '*') if x.is_dir() and re.match(r'\w\w-\w\w-0*\d+', x.parts[-1])]
        return folders

    def executeProcess(self, folder, tipo_modelo=None):
        cod_ponto = folder.parts[-1] 

        ponto = self.fetchPointData(cod_ponto)
        ponto['durrast'] = ponto["fim_rastreio"] - ponto["inicio_rastreio"]
        ponto['inicio_rastreio'] = ponto['inicio_rastreio'].strftime('%d/%m/%Y %H:%M:%S')
        ponto['data_processamento'] = ponto['data_processamento'].strftime('%d/%m/%Y')
        if ponto['materializado']:
            ponto['materializado'] = 'Sim'
        else:
            ponto['materializado'] = 'Não'

        if not ponto:
            self.log(f"Ponto {cod_ponto} não encontrado no banco.")
            return

        # --- Carrega layout QPT ---
        project = QgsProject.instance()
        # É importante que o layout tenha um nome exclusivo para evitar conflito com layouts existentes
        layout_name = f"Monografia_{cod_ponto}"
        
        # Tenta pegar um layout existente com o nome, se não existir, cria um
        layout = project.layoutManager().layoutByName(layout_name)
        if not layout:
             layout = QgsPrintLayout(project)
             layout.setName(layout_name)
             project.layoutManager().addLayout(layout)
             
        layout.initializeDefaults()

        doc = QDomDocument()
        try:
            with open(self.template_qpt, 'r', encoding='utf-8') as f:
                content = f.read()
                doc.setContent(content)
        except Exception as e:
             self.log(f"Erro ao carregar o template QPT: {e}")
             return

        read_write_context = QgsReadWriteContext()
        if not layout.loadFromTemplate(doc, read_write_context):
             self.log(f"Falha ao carregar o template no layout: {self.template_qpt}")
             return

        # --- Substitui campos do layout ---
        # Este método de substituição é rudimentar (apenas texto de rótulos). 
        # Para ser mais robusto e usar o poder do QGIS, o ideal seria usar 
        # 'Atlas Feature Attributes' ou 'Map Title' no template QPT com expressões.
        for item in layout.items():
            if hasattr(item, "text") and isinstance(item.text(), str):
                text = item.text()
                for k, v in ponto.items():
                    if v is None:
                        v = ""
                    text = text.replace(f'[{k}]', str(v))
                item.setText(text)
            
            # TODO: Se o seu template QPT usar o 'Map Theme' ou 'Map Extent' 
            # para o croqui digital, você precisará de código extra aqui. 
            # Se a imagem do croqui digital já estiver na pasta, use um 'Picture'
            # no QPT com uma expressão como: 
            # 'file:///[% "pasta_estrutura" %]/[% "cod_ponto" %]/4_Croqui/[% "cod_ponto" %]_CROQUI_DIGITAL.jpg'
            # A variável 'pasta_estrutura' e 'cod_ponto' precisariam ser configuradas
            # como variáveis de projeto/layout antes da exportação.

        # Definição de variáveis de layout para uso no QPT (útil para o croqui digital)
        layout.set=('path_structure', str(self.path))
        layout.set=('cod_ponto', cod_ponto)

        output_folder = folder / '8_Monografia'
        output_folder.mkdir(exist_ok=True)
        pdf_path = output_folder / f"{cod_ponto}.pdf"

        exporter = QgsLayoutExporter(layout)
        result = exporter.exportToPdf(str(pdf_path), QgsLayoutExporter.PdfExportSettings())

        project.layoutManager().removeLayout(layout)

        if result == QgsLayoutExporter.Success:
            self.log(f"✓ PDF gerado: {pdf_path}")
            return True
        else:
            self.log(f"⚠ Falha ao gerar PDF do ponto {cod_ponto}")
            return False
