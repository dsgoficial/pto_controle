# -*- coding: utf-8 -*-
import os
from pathlib import Path
import psycopg2
import psycopg2.extras
from qgis.core import (
    QgsLayout,
    QgsExpressionContextUtils,
    QgsExpressionContextScope,
    QgsProject,
    QgsPrintLayout,
    QgsLayoutExporter,
    QgsReadWriteContext,
)
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtCore import QFile

class HandleDistributeMonografia:
    def __init__(self, conn, path, template_qpt, settings=None, digital=True, feedback=None, tipo_modelo=None):
        self.conn = conn
        self.path = Path(path)
        self.template_qpt = template_qpt
        self.settings = settings or {}
        self.digital = digital
        self.feedback = feedback
        self.tipo_modelo = tipo_modelo
        self.img_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']

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

        self.preparePhotos(ponto, folder)

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

        self._injectProjectVariables_Final(layout, ponto, cod_ponto)

        # --- NOVO CÓDIGO: Configura as imagens diretamente via setPicturePath ---
        self.setImagesDirectly(layout)
        # ----------------------------------------------------------------------

        # --- Substitui campos do layout ---
        # Este método de substituição é rudimentar (apenas texto de rótulos). 
        # Para ser mais robusto e usar o poder do QGIS, o ideal seria usar 
        # 'Atlas Feature Attributes' ou 'Map Title' no template QPT com expressões.
        # for item in layout.items():
        #     if hasattr(item, "text") and isinstance(item.text(), str):
        #         text = item.text()
        #         for k, v in ponto.items():
        #             if v is None:
        #                 v = ""
        #             text = text.replace(f'[{k}]', str(v))
        #         item.setText(text)
            
            # TODO: Se o seu template QPT usar o 'Map Theme' ou 'Map Extent' 
            # para o croqui digital, você precisará de código extra aqui. 
            # Se a imagem do croqui digital já estiver na pasta, use um 'Picture'
            # no QPT com uma expressão como: 
            # 'file:///[% "pasta_estrutura" %]/[% "cod_ponto" %]/4_Croqui/[% "cod_ponto" %]_CROQUI_DIGITAL.jpg'
            # A variável 'pasta_estrutura' e 'cod_ponto' precisariam ser configuradas
            # como variáveis de projeto/layout antes da exportação.

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

    def preparePhotos(self, pto, folder):
        """Localiza e adiciona fotos nos campos do ponto"""
        fotos = folder / '3_Foto_Rastreio'
        if fotos.exists():
            for i, f in enumerate(sorted(fotos.iterdir())):
                if f.suffix in self.img_extensions:
                    pto[f'photoPt{i + 1}'] = str(f)

        croqui_folder = folder / '4_Croqui'
        if croqui_folder.exists():
            croqui_files = [f for f in croqui_folder.iterdir() if f.suffix in self.img_extensions]
            croqui_digital = [str(f) for f in croqui_files if f.stem.endswith('_CROQUI_DIGITAL')]
            croqui_normal = [str(f) for f in croqui_files if f.stem.endswith('_CROQUI')]
            if self.digital and croqui_digital:
                pto['photoCroqui'] = croqui_digital[0]
            elif croqui_normal:
                pto['photoCroqui'] = croqui_normal[0]

        img_folder = folder / '7_Imagens_Monografia'
        cod_ponto = pto['cod_ponto']
        # Importante: verificar se as imagens existem antes de adicionar
        aerea = img_folder / f"{cod_ponto}_AEREA.jpg"
        estado = img_folder / f"{cod_ponto}_ESTADO.jpg"
        municipio = img_folder / f"{cod_ponto}_MUNICIPIO.jpg"
        
        if aerea.exists():
            pto['photoAerView'] = str(aerea.resolve())
        if estado.exists():
            pto['photoView1'] = str(estado.resolve())
        if municipio.exists():
            pto['photoView2'] = str(municipio.resolve())


    def _injectProjectVariables_Final(self, layout, data: dict, cod_ponto: str):
        """
        Injeta variáveis diretamente no layout (escopo de layout),
        compatível com todas as versões do QGIS.
        """

        # Injeta variáveis de dados
        for k, v in data.items():
            valor = str(v) if v is not None else ""
            QgsExpressionContextUtils.setLayoutVariable(layout, k, valor)

        # Injeta variáveis adicionais
        QgsExpressionContextUtils.setLayoutVariable(layout, 'cod_ponto', cod_ponto)
        QgsExpressionContextUtils.setLayoutVariable(layout, 'pasta_estrutura', str(self.path))

        # Injeta variáveis de imagem (validando caminhos)
        photo_keys = [
            'photoCroqui', 'photoAerView', 'photoView1', 'photoView2',
            'photoPt1', 'photoPt2', 'photoPt3', 'photoPt4'
        ]

        for key in photo_keys:
            path_img = data.get(key)
            if path_img and path_img.strip():
                path_obj = Path(path_img)
                
                if path_obj.is_file():
                    caminho_final = path_obj.resolve().as_uri()
                    
                    QgsExpressionContextUtils.setLayoutVariable(layout, key, caminho_final) # <--- USAR ESTA LINHA
                    
                    self.log(f"✓ {key}: {caminho_final}")

                    # DEBUG
                    scope = QgsExpressionContextUtils.layoutScope(layout)
                    valor_injetado = scope.variable(key)
                    if valor_injetado != caminho_final:
                        self.log(f"ERRO FATAL: Variável {key} ainda está inconsistente!")
                    else:
                        self.log(f"DEBUG: Variável {key} lida corretamente no escopo do layout.")
                        
                else:
                    self.log(f"⚠ Imagem não encontrada para {key}: {path_img}")
                    QgsExpressionContextUtils.setLayoutVariable(layout, key, "")
            else:
                QgsExpressionContextUtils.setLayoutVariable(layout, key, "")

        self.log("✓ Variáveis injetadas no layout com sucesso.")

    def setImagesDirectly(self, layout: QgsPrintLayout):
        """
        Define o caminho das imagens nos itens QgsLayoutItemPicture do layout
        usando setPicturePath(), contornando problemas de expressão.
        """
        
        # Mapeamento: {'Nome da Variável': 'ID/Nome do Item no QPT'}
        # VOCÊ PRECISA GARANTIR QUE OS VALORES (IDs dos Itens) ESTÃO CORRETOS NO SEU TEMPLATE QPT!
        image_map = {
            'photoCroqui': 'Croqui',     
            'photoAerView': 'AereaView',     
            'photoView1': 'Municipio',      
            'photoView2': 'Estado',   
            'photoPt1': 'Foto1',
            'photoPt2': 'Foto2',
            'photoPt3': 'Foto3',
            'photoPt4': 'Foto4',
        }

        for var_name, item_id in image_map.items():
            # 1. Obtém o caminho da imagem da variável de layout
            scope = QgsExpressionContextUtils.layoutScope(layout)
            path_uri = scope.variable(var_name)
            
            # 2. Encontra o item de layout
            item = layout.itemById(item_id)
            
            # 3. Verifica se o item existe e se o caminho é válido
            if item is None:
                self.log(f"Item de Layout não encontrado: {item_id}")
                continue
            
            if not path_uri or not path_uri.startswith('file:///'):
                 self.log(f"Caminho URI inválido para {item_id} ({var_name}): {path_uri}")
                 # Opcional: define um caminho para um placeholder ou seta para vazio
                 # item.setPicturePath("") 
                 continue

            # 4. Define o caminho da imagem (o PyQGIS resolve o URI)
            try:
                # O item deve ser um QgsLayoutItemPicture para setPicturePath funcionar
                # O item.setPicturePath espera um caminho local, mas o URI file:/// funciona
                item.setPicturePath(path_uri) 
                
                # Garante que a imagem seja redesenhada (como no seu exemplo)
                item.refresh() 
                self.log(f"✓ Imagem definida para {item_id} usando setPicturePath.")
                
            except AttributeError:
                self.log(f"⚠ O item '{item_id}' não é um QgsLayoutItemPicture. Não pode usar setPicturePath.")
            except Exception as e:
                self.log(f"Erro ao definir a imagem para {item_id}: {e}")