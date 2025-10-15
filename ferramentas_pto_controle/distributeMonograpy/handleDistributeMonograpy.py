# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path
from datetime import date
import psycopg2
import psycopg2.extras
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PyQt5 import QtGui


class HandleDistributeMonografia:
    def __init__(self, path, conn, settings, digital=False, feedback=None):
        self.conn = conn
        self.path = Path(path)
        self.settings = settings
        self.digital = digital
        self.feedback = feedback
        self.img_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
        self.points = []
        self.folders = []

    def log(self, msg):
        if self.feedback:
            self.feedback.pushInfo(msg)
        else:
            print(msg)

    def getListOfPoints(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('SELECT cod_ponto FROM bpc.ponto_controle_p')
            self.points = [r['cod_ponto'] for r in cur.fetchall()]
        return self.points

    def getFoldersFromStructure(self):
        self.folders = [
            x for x in self.path.rglob('*')
            if x.is_dir() and re.match(r'\w\w-\w\w-0*\d+', x.name)
        ]
        return self.folders

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

    # -------------------------------------------------------------------
    # Função principal de geração
    # -------------------------------------------------------------------
    def executeProcess(self, folder, tipo_modelo):
        cod_ponto = folder.name
        pto = self.fetchPointData(cod_ponto)
        if not pto:
            raise Exception(f"Ponto {cod_ponto} não encontrado no banco de dados.")

        # === Preparação de campos ===
        pto['dataMono'] = date.today().strftime('%d/%m/%Y')
        pto['m'] = 'Sim' if pto.get('materializado') else 'Não'
        pto['freq'] = pto.get('freq_processada', '')
        pto['mc'] = pto.get('meridiano_central', '')
        pto['mascara'] = pto.get('mascara_elevacao', '')
        pto['taxa'] = pto.get('taxa_gravacao', '')
        pto['sigmaXY'] = pto.get('precisao_horizontal_esperada', '')
        pto['sigmaZ'] = pto.get('precisao_vertical_esperada', '')
        pto['durRast'] = pto["fim_rastreio"] - pto["inicio_rastreio"]

        if pto.get('inicio_rastreio'):
            try:
                pto['inicio_rastreio'] = pto['inicio_rastreio'].strftime('%d/%m/%Y %H:%M:%S')
            except Exception:
                pass
        if pto.get('data_processamento'):
            try:
                pto['data_processamento'] = pto['data_processamento'].strftime('%d/%m/%Y')
            except Exception:
                pass

        pto['crea_engenheiro_responsavel'] = (
            f"CREA: {pto['crea_engenheiro_responsavel']}"
            if pto.get('crea_engenheiro_responsavel')
            else f"CPF: {pto.get('cpf_engenheiro_responsavel', '')}"
        )

        # === Fotos ===
        self.preparePhotos(pto, folder)

        # === Cria PDF ===
        mono_folder = folder / '8_Monografia'
        mono_folder.mkdir(exist_ok=True)
        pdf_path = mono_folder / f"{cod_ponto}.pdf"
        orientacao = portrait(A4) if tipo_modelo == 1 else landscape(A4)

        c = canvas.Canvas(str(pdf_path), pagesize=orientacao)
        largura, altura = orientacao

        def cabecalho():
            """Cabeçalho com logotipo CGEO e título"""
            logo = self.settings.get('LOGOTIPO') 
            if logo and os.path.exists(logo): 
                c.drawImage(logo, 30, altura - 145, width=72, preserveAspectRatio=True)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, altura - 60, "MONOGRAFIA DO PONTO DE CONTROLE")
            c.line(50, altura - 95, largura - 50, altura - 95)

        cabecalho()

        x, y = 60, altura - 120
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, f"Ponto: {cod_ponto}")
        y -= 25
        c.setFont("Helvetica", 10)

        def linha(label, valor):
            nonlocal y
            c.drawString(x, y, f"{label}: {valor}")
            y -= 13
            if y < 80:
                c.showPage()
                y = altura - 100
                c.setFont("Helvetica", 10)

        # --- Dados Gerais ---
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, "DADOS GERAIS")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Executante", pto.get("orgao_executante", "")),
            ("Projeto", pto.get("projeto", "")),
            ("Método de posicionamento", pto.get("metodo_pos", "")),
            ("Tipo de referência", pto.get("tipo_ref1", "")),
            ("Materializado", pto.get("m", "")),
        ]: linha(campo, valor)

        # --- Coordenadas ---
        y -= 8; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "COORDENADAS PLANAS (UTM)")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Norte (m)", pto.get("norte", "")),
            ("Leste (m)", pto.get("leste", "")),
            ("Fuso", pto.get("fuso", "")),
            ("Meridiano Central", pto.get("mc", "")),
            ("Sistema Geodésico", pto.get("sistema_geodesico1", "")),
        ]: linha(campo, valor)

        # --- Altitude ---
        y -= 8; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "ALTITUDE")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Elipsoidal (m)", pto.get("altitude_geometrica", "")),
            ("Ortométrica (m)", pto.get("altitude_ortometrica", "")),
            ("Modelo", pto.get("modelo_geoidal", "")), ######################################################################
            ("Referencial Altimétrico", pto.get("referencial_altim1", "")),
        ]: linha(campo, valor)

        # --- Precisão ---
        y -= 47; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "PRECISÃO")
        y -= 18; c.setFont("Helvetica", 10)
        linha("Precisão horizontal esperada (m)", pto.get("sigmaXY", ""))
        linha("Precisão vertical esperada (m)", pto.get("sigmaZ", ""))

        # --- Equipamentos ---
        x = largura/2
        y = y + 252; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "DESCRIÇÃO DOS EQUIPAMENTOS")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Receptor GPS", pto.get("modelo_gps", "")),
            ("Série GPS", pto.get("numero_serie_gps", "")),
            ("Antena", pto.get("modelo_antena", "")),
            ("Série Antena", pto.get("numero_serie_antena", "")),
        ]: linha(campo, valor)

        # --- Medição ---
        y -= 21; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "DESCRIÇÃO DA MEDIÇÃO")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Operador", pto.get("medidor", "")), ###########################################################
            ("Data/Hora do rastreio", pto.get("inicio_rastreio", "")), ###########################################
            ("Tempo de rastreio", pto.get("durRast", "")), ##############################################
            ("Máscara de elevação", pto.get("mascara_elevacao", "")), ##############################################
            ("Taxa de gravação", pto.get("taxa_gravacao", "")), ##############################################
            ("Altura da antena (m)", pto.get("altura_antena", "")), ##############################################
            ("Referência de med. da altura", pto.get("refalt", "")),
        ]: linha(campo, valor)

        # --- Processamento ---
        y -= 8; c.setFont("Helvetica-Bold", 11); c.drawString(x, y, "PROCESSAMENTO")
        y -= 18; c.setFont("Helvetica", 10)
        for campo, valor in [
            ("Frequência Processada", pto.get("freq", "")),
            ("Data de Processamento", pto.get("data_processamento", "")),
            ("Órbita", pto.get("orbita1", "")), ############################################################################
        ]: linha(campo, valor)

        # --- Fotos de localização do ponto ---
        foto_loc1 = pto.get("photoView1")
        foto_loc2 = pto.get("photoView2")
        y -= 27 

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(largura / 2, y, "LOCALIZAÇÃO DO PONTO")

        largura_img_loc = 240    
        altura_img_loc = 180     
        espaco_loc = 10          # espaço entre as duas imagens (~0,35 cm)          
        y = y - 5 - altura_img_loc
        
        x_total_loc = (largura_img_loc * 2) + espaco_loc
        x_inicio_loc = (largura - x_total_loc) / 2

        if foto_loc1 and os.path.exists(foto_loc1):
            try:
                img1_loc = ImageReader(foto_loc1)
                c.drawImage(
                    img1_loc,
                    x_inicio_loc,
                    y,
                    width=largura_img_loc,
                    height=altura_img_loc,
                    preserveAspectRatio=True
                )
            except Exception as e:
                self.log(f"Erro ao carregar imagem de localização 1: {e}")

        if foto_loc2 and os.path.exists(foto_loc2):
            try:
                img2_loc = ImageReader(foto_loc2)
                c.drawImage(
                    img2_loc,
                    x_inicio_loc + largura_img_loc + espaco_loc,
                    y,
                    width=largura_img_loc,
                    height=altura_img_loc,
                    preserveAspectRatio=True
                )
            except Exception as e:
                self.log(f"Erro ao carregar imagem de localização 2: {e}")

        # --- FOTOS ---
        c.showPage()

        # --- Foto aérea grande e centralizada ---
        foto_aerea = pto.get("photoAerView")
        if foto_aerea and os.path.exists(foto_aerea):
            try:
                img = ImageReader(foto_aerea)
                largura_img = 490
                altura_img = 350
                x_img = (largura - largura_img) / 2
                y_img = altura - 420
                c.drawImage(img, x_img, y_img, width=largura_img, height=altura_img, preserveAspectRatio=False)
                c.setFont("Helvetica-Bold", 12)
                c.drawCentredString(largura / 2, y_img + altura_img + 20, "Vista Aérea")
            except Exception as e:
                self.log(f"Erro ao carregar imagem aérea: {e}")

        # --- Outras fotos (2x2) ---
        fotos_quadrado = [
            ("Foto 1", "photoPt1"),
            ("Foto 2", "photoPt2"),
            ("Foto 3", "photoPt3"),
            ("Foto 4", "photoPt4"),
        ]

        x_inicial = 100
        y_inicial = y_img - 204  # abaixo da imagem aérea
        espaco_x = 230
        espaco_y = 200
        largura_img2 = 142
        altura_img2 = 149

        colunas = 2
        linha2 = 0
        coluna = 0

        for label, key in fotos_quadrado:
            img_path = pto.get(key)
            if img_path and os.path.exists(img_path):
                try:
                    img = ImageReader(img_path)
                    x = x_inicial + (coluna * espaco_x)
                    y = y_inicial - (linha2 * espaco_y)

                    c.drawImage(img, x, y, width=largura_img2, height=altura_img2, preserveAspectRatio=False)
                    c.setFont("Helvetica", 11)
                    c.drawCentredString(x + (largura_img2/2), y + altura_img2 + 10, label)

                    coluna += 1
                    if coluna >= colunas:
                        coluna = 0
                        linha2 += 1
                except Exception as e:
                    self.log(f"Erro ao carregar imagem {img_path}: {e}")

        # --- Página 2: Croqui ---
        croqui_path = pto.get("photoCroqui")
        if croqui_path and os.path.exists(croqui_path):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            titulo = "CROQUI"
            titulo_largura = c.stringWidth(titulo, "Helvetica-Bold", 10)
            c.drawString((largura - titulo_largura) / 2, altura - 50, titulo)

            try:
                img = ImageReader(croqui_path)
                largura_img = 451  # margem de 60 em cada lado
                altura_img = 642    # margem vertical
                x_img = (largura - largura_img)/2
                y_img = altura - 40 - altura_img
                c.drawImage(img, x_img, y_img, width=largura_img, height=altura_img, preserveAspectRatio=True)
            except Exception as e:
                self.log(f"Erro ao carregar croqui: {e}")

        # --- Responsável Técnico ---
        y_resp = y_img - 12 ; c.setFont("Helvetica-Bold", 11); c.drawString(x, y_resp, "RESPONSÁVEL TÉCNICO")
        y = y_resp - 18; c.setFont("Helvetica", 10)
        linha("Data", pto.get("dataMono", ""))
        linha("Engenheiro", pto.get("engenheiro_responsavel", ""))
        linha("CREA", pto.get("crea_engenheiro_responsavel", ""))

        # Insere imagem da assinatura (se houver)
        assinatura = self.settings.get("signature")
        if assinatura and os.path.exists(assinatura):
            try:
                c.drawImage(assinatura, 100, y_resp - 70, width=142, height=70, mask='auto')
            except Exception as e:
                self.log(f"Erro ao carregar assinatura: {e}")

        # Finaliza o PDF
        c.save()
        self.log(f"✓ PDF do ponto {cod_ponto} gerado com fotos e croqui: {pdf_path}")

    # -------------------------------------------------------------------
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
        pto['photoAerView'] = str(img_folder / f"{cod_ponto}_AEREA.jpg")
        pto['photoView1'] = str(img_folder / f"{cod_ponto}_ESTADO.jpg")
        pto['photoView2'] = str(img_folder / f"{cod_ponto}_MUNICIPIO.jpg")
