import os
from pathlib import Path
import re
from qgis.core import (
    QgsExpressionContextUtils,
    QgsProject,
    QgsPrintLayout,
    QgsLayoutExporter,
    QgsReadWriteContext,
)
from qgis.PyQt.QtXml import QDomDocument
from datetime import timedelta, datetime

class HandleDistributeMonography:
    def __init__(self, layer, feicao, path, template_qpt, settings=None, digital=True, feedback=None, tipo_modelo=None):
        # self.conn = conn
        self.layer = layer
        self.feicao = feicao
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

    # def fetchPointData(self, cod_ponto):
    #     with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    #         cur.execute(PointDataQueries.FETCH_POINT_WITH_DOMAINS, (cod_ponto,))
    #         return cur.fetchone()

    def fetchPointData(self, cod_ponto):
        """Busca o ponto na camada de entrada com base no código do ponto."""
        if self.feicao:
            for feature in self.layer.getSelectedFeatures():
                if str(feature['cod_ponto']) == str(cod_ponto):
                    # Converte atributos em dicionário
                    ponto = feature.attributes()
                    fields = [f.name() for f in self.layer.fields()]
                    ponto_dict = dict(zip(fields, ponto))
                    return ponto_dict
            self.log(f"Ponto {cod_ponto} não encontrado na camada.")
            return None
        if not self.feicao:
            for feature in self.layer.getFeatures():
                if str(feature['cod_ponto']) == str(cod_ponto):
                    # Converte atributos em dicionário
                    ponto = feature.attributes()
                    fields = [f.name() for f in self.layer.fields()]
                    ponto_dict = dict(zip(fields, ponto))
                    return ponto_dict
            self.log(f"Ponto {cod_ponto} não encontrado na camada.")
            return None

    def getFoldersFromStructure(self):
        if self.feicao:
            features = self.layer.getSelectedFeatures()
        else:
            features = self.layer.getFeatures()
        valid_cods = set()
        for feature in features:
            cod = str(feature['cod_ponto'])
            valid_cods.add(cod)
            
        folders = []
        folder_name_pattern = re.compile(r'(\w\w-\w\w-0*\d+)$')
        for x in self.path.rglob('*'):
            if x.is_dir():
                folder_name = x.parts[-1]
                match = folder_name_pattern.match(folder_name)
                if match:
                    cod_from_folder = match.group(1) 
                    if cod_from_folder in valid_cods:
                        folders.append(x)            
        return folders

    def executeProcess(self, folder, tipo_modelo=None):
        cod_ponto = folder.parts[-1] 
        ponto = self.fetchPointData(cod_ponto)
        if not ponto:
            self.log(f"Ponto {cod_ponto} não encontrado no banco.")
            return
        DOMINIOS = {
            "orbita": {
                1: "Ultra Rápida (predita)",
                2: "Ultra Rápida (observada)",
                3: "Rápida",
                4: "Final",
                97: "Não aplicável",
                9999: "A SER PREENCHIDO",
            },
            "metodo_posicionamento": {
                1: "Posicionamento por ponto preciso (PPP)",
                2: "Real Time Kinematic (RTK)",
                3: "Semi-cinemático",
                4: "Relativo Estático",
                5: "Relativo Cinemático",
                6: "Absoluto",
                9999: "A SER PREENCHIDO",
            },
            "sistema_geodesico": {
                1: "SAD-69",
                2: "SIRGAS2000",
                3: "WGS-84",
                4: "Córrego Alegre",
                5: "Astro Chuá",
                6: "SAD-69 (96)",
                99: "Outra referência",
                9999: "A SER PREENCHIDO",
            },
            "referencia_medicao_altura": {
                1: "Nível do solo",
                2: "Nível do objeto",
                9999: "A SER PREENCHIDO",
            },
            "referencial_altim": {
                1: "Torres",
                2: "Imbituba",
                3: "Santana",
                99: "Outra referência",
                9999: "A SER PREENCHIDO",
            },
            "tipo_ref": {
                1: "Altimétrico",
                2: "Planimétrico",
                3: "Planialtimétrico",
                4: "Gravimétrico",
                9999: "A SER PREENCHIDO",
            },
        }

        def traduz_dominios(ponto):
            for campo, mapa in DOMINIOS.items():
                val = ponto.get(campo)
                if val in mapa:
                    ponto[campo] = mapa[val]
            return ponto
        
        ponto = traduz_dominios(ponto)

        def to_datetime(value):
            """Converte valor para datetime Python, aceitando str, QDate, QDateTime ou datetime."""
            if value is None:
                return None
            try:
                # QDateTime
                if hasattr(value, 'toPyDateTime'):
                    return value.toPyDateTime()
                # QDate
                elif hasattr(value, 'toPyDate'):
                    return datetime.combine(value.toPyDate(), datetime.min.time())
                # Nenhum tipo reconhecido
                else:
                    print(f"Tipo desconhecido: {type(value)} -> {value}")
                    return None

            except Exception as e:
                print(f"Erro ao converter valor {value} ({type(value)}): {e}")
                return None
            
        inicio = to_datetime(ponto.get("inicio_rastreio"))
        fim = to_datetime(ponto.get("fim_rastreio"))
        proc = to_datetime(ponto.get("data_processamento"))

        try:
            if inicio and fim:
                ponto['durrast'] = fim - inicio
            else:
                ponto['durrast'] = timedelta(0)
            ponto['inicio_rastreio'] = inicio.strftime('%d/%m/%Y %H:%M:%S') if inicio else ''
            ponto['data_processamento'] = proc.strftime('%d/%m/%Y') if proc else ''
        except Exception as e:
            self.log(f"Erro ao converter datas: {e}")
            ponto['durrast'] = ''


        if ponto['materializado']:
            ponto['materializado'] = 'Sim'
        else:
            ponto['materializado'] = 'Não'

        self.preparePhotos(ponto, folder)

        project = QgsProject.instance()
        layout_name = f"Monografia_{cod_ponto}"
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
        self.setImagesDirectly(layout)

        output_folder = folder / '8_Monografia'
        output_folder.mkdir(exist_ok=True)
        pdf_path = output_folder / f"{cod_ponto}.pdf"

        exporter = QgsLayoutExporter(layout)
        result = exporter.exportToPdf(str(pdf_path), QgsLayoutExporter.PdfExportSettings())

        project.layoutManager().removeLayout(layout)

        if result == QgsLayoutExporter.Success:
            self.log(f"PDF gerado: {pdf_path}")
            return True
        else:
            self.log(f"Falha ao gerar PDF do ponto {cod_ponto}")
            return False

    def preparePhotos(self, ponto, folder):
        """Localiza e adiciona fotos nos campos do ponto"""
        fotos = folder / '3_Foto_Rastreio'
        if fotos.exists():
            for i, f in enumerate(sorted(fotos.iterdir())):
                if f.suffix in self.img_extensions:
                    ponto[f'photoPt{i + 1}'] = str(f)

        croqui_folder = folder / '4_Croqui'
        if croqui_folder.exists():
            croqui_files = [f for f in croqui_folder.iterdir() if f.suffix in self.img_extensions]
            croqui_digital = [str(f) for f in croqui_files if f.stem.endswith('_CROQUI_DIGITAL')]
            croqui_normal = [str(f) for f in croqui_files if f.stem.endswith('_CROQUI')]
            if self.digital and croqui_digital:
                ponto['photoCroqui'] = croqui_digital[0]
            elif croqui_normal:
                ponto['photoCroqui'] = croqui_normal[0]

        img_folder = folder / '7_Imagens_Monografia'
        cod_ponto = ponto['cod_ponto']
        aerea = img_folder / f"{cod_ponto}_AEREA.jpg"
        estado = img_folder / f"{cod_ponto}_ESTADO.jpg"
        municipio = img_folder / f"{cod_ponto}_MUNICIPIO.jpg"
        
        if aerea.exists():
            ponto['photoAerView'] = str(aerea.resolve())
        if estado.exists():
            ponto['photoView1'] = str(estado.resolve())
        if municipio.exists():
            ponto['photoView2'] = str(municipio.resolve())


    def _injectProjectVariables_Final(self, layout, data: dict, cod_ponto: str):
        """Injeta variáveis diretamente no layout (escopo de layout)"""
        for k, v in data.items():
            valor = str(v) if v is not None else ""
            QgsExpressionContextUtils.setLayoutVariable(layout, k, valor)

        QgsExpressionContextUtils.setLayoutVariable(layout, 'cod_ponto', cod_ponto)
        QgsExpressionContextUtils.setLayoutVariable(layout, 'pasta_estrutura', str(self.path))

        photo_keys = [
            'photoCroqui', 'photoAerView', 'photoView1', 'photoView2',
            'photoPt1', 'photoPt2', 'photoPt3', 'photoPt4'
        ]

        for key in photo_keys:
            path_img = data.get(key)
            if path_img and Path(path_img).is_file():
                uri = Path(path_img).resolve().as_uri()
                QgsExpressionContextUtils.setLayoutVariable(layout, key, uri)
            else:
                QgsExpressionContextUtils.setLayoutVariable(layout, key, "")
                self.log(f" Variável {key} não definida ou arquivo ausente.")

        extra_imgs = {
            'logoInstituicao': self.settings.get('LOGOTIPO'),
            'assinaturaResponsavel': self.settings.get('signature')
        }

        for key, path_img in extra_imgs.items():
            if path_img and Path(path_img).is_file():
                uri = Path(path_img).resolve().as_uri()
                QgsExpressionContextUtils.setLayoutVariable(layout, key, uri)
            else:
                QgsExpressionContextUtils.setLayoutVariable(layout, key, "")
                self.log(f" Variável extra {key} não definida ou arquivo ausente.")


    def setImagesDirectly(self, layout: QgsPrintLayout):
        """Define o caminho das imagens diretamente nos itens do layout"""
        image_map = {
            'photoCroqui': 'Croqui',
            'photoAerView': 'AereaView',
            'photoView1': 'Municipio',
            'photoView2': 'Estado',
            'photoPt1': 'Foto1',
            'photoPt2': 'Foto2',
            'photoPt3': 'Foto3',
            'photoPt4': 'Foto4',
            'logoInstituicao': 'logo',          
            'assinaturaResponsavel': 'assinatura',
        }

        for var_name, item_id in image_map.items():
            context = layout.createExpressionContext()
            path_uri = context.variable(var_name)
            item = layout.itemById(item_id)

            if not item:
                self.log(f" Item não encontrado: {item_id}")
                continue

            if not path_uri:
                self.log(f" Nenhum caminho definido para {item_id} ({var_name})")
                continue

            try:
                local_path = path_uri.replace('file:///', '', 1)
                if not os.path.isfile(local_path):
                    self.log(f" Arquivo não encontrado: {local_path}")
                    continue

                item.setPicturePath(local_path)
                item.refresh()

            except Exception as e:
                self.log(f" Erro ao aplicar imagem em {item_id}: {e}")

# class PointDataQueries:    
#     FETCH_POINT_WITH_DOMAINS = """
#         SELECT *,
#             dominios.tipo_ref.code_name as tipo_ref1,
#             dominios.metodo_posicionamento.code_name as metodo_pos,
#             dominios.referencial_altim.code_name as referencial_altim1,
#             dominios.sistema_geodesico.code_name as sistema_geodesico1,
#             dominios.orbita.code_name as orbita1,
#             dominios.referencia_medicao_altura.code_name as refalt
#         FROM bpc.ponto_controle_p
#         INNER JOIN dominios.tipo_ref 
#             ON dominios.tipo_ref.code = bpc.ponto_controle_p.tipo_ref
#         INNER JOIN dominios.metodo_posicionamento 
#             ON dominios.metodo_posicionamento.code = bpc.ponto_controle_p.metodo_posicionamento
#         INNER JOIN dominios.referencial_altim 
#             ON dominios.referencial_altim.code = bpc.ponto_controle_p.referencial_altim
#         INNER JOIN dominios.sistema_geodesico 
#             ON dominios.sistema_geodesico.code = bpc.ponto_controle_p.sistema_geodesico
#         INNER JOIN dominios.orbita 
#             ON dominios.orbita.code = bpc.ponto_controle_p.orbita
#         INNER JOIN dominios.referencia_medicao_altura 
#             ON dominios.referencia_medicao_altura.code = bpc.ponto_controle_p.referencia_medicao_altura
#         WHERE cod_ponto = %s
#     """