# coding=utf-8

import re
import json
from datetime import datetime, date
from pathlib import Path
import sys
import subprocess
import psycopg2
import psycopg2.extras
import PyPDF2
from secretary import Renderer
from processImages import processImages

class GenerateMonograpy():

    def __init__(self,path, host, port, db_name, user, password):
        self.conn = psycopg2.connect("host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(host, port, db_name, user, password))
        self.path = Path(path)
        self.img_extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']
        with open('config_default_monografia.json') as setting: 
            self.settings = json.load(setting)
        self.points = []
        # processImages(self.path)
    
    def fetchAll(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(u'''
            SELECT * FROM bpc.ponto_controle_p
            ''')
            return cursor.fetchall()

    def fetchOne(self, point):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(u'''
            SELECT *,
            dominios.tipo_ref.code_name as tipo_ref1, 
            dominios.tipo_situacao.nome as tipo_situacao1,
            dominios.tipo_pto_ref_geod_topo.code_name as tipo_pto_ref_geod_topo1,
            dominios.tipo_medicao_altura.code_name as tipo_medicao_altura1,
            dominios.tipo_marco_limite.code_name as tipo_marco_limite1,
            dominios.situacao_marco.code_name as situacao_marco1,
            dominios.sistema_geodesico.code_name as sistema_geodesico1,
            dominios.referencial_grav.code_name as referencial_grav1,
            dominios.referencial_altim.code_name as referencial_altim1,
            dominios.referencia_medicao_altura.code_name as referencia_medicao_altura1,
            dominios.rede_referencia.code_name as rede_referencia1,
            dominios.orbita.code_name as orbita1,
            dominios.metodo_posicionamento.code_name as metodo_pos,
            dominios.classificacao_ponto.nome as classificacao_ponto1
            FROM bpc.ponto_controle_p
            INNER JOIN dominios.tipo_ref on dominios.tipo_ref.code = bpc.ponto_controle_p.tipo_ref
            INNER JOIN dominios.tipo_situacao on dominios.tipo_situacao.code = bpc.ponto_controle_p.tipo_situacao
            INNER JOIN dominios.tipo_pto_ref_geod_topo on dominios.tipo_pto_ref_geod_topo.code = bpc.ponto_controle_p.tipo_pto_ref_geod_topo
            INNER JOIN dominios.tipo_medicao_altura on dominios.tipo_medicao_altura.code = bpc.ponto_controle_p.tipo_medicao_altura
            INNER JOIN dominios.tipo_marco_limite on dominios.tipo_marco_limite.code = bpc.ponto_controle_p.tipo_marco_limite
            INNER JOIN dominios.situacao_marco on dominios.situacao_marco.code = bpc.ponto_controle_p.situacao_marco
            INNER JOIN dominios.sistema_geodesico on dominios.sistema_geodesico.code = bpc.ponto_controle_p.sistema_geodesico
            INNER JOIN dominios.referencial_grav on dominios.referencial_grav.code = bpc.ponto_controle_p.referencial_grav
            INNER JOIN dominios.referencial_altim on dominios.referencial_altim.code = bpc.ponto_controle_p.referencial_altim
            INNER JOIN dominios.referencia_medicao_altura on dominios.referencia_medicao_altura.code = bpc.ponto_controle_p.referencia_medicao_altura
            INNER JOIN dominios.rede_referencia on dominios.rede_referencia.code = bpc.ponto_controle_p.rede_referencia
            INNER JOIN dominios.orbita on dominios.orbita.code = bpc.ponto_controle_p.orbita
            INNER JOIN dominios.metodo_posicionamento on dominios.metodo_posicionamento.code = bpc.ponto_controle_p.metodo_posicionamento
            INNER JOIN dominios.classificacao_ponto on dominios.classificacao_ponto.code = bpc.ponto_controle_p.classificacao_ponto
            WHERE cod_ponto='{}'
            '''.format(point))
            return cursor.fetchone()

    def getFoldersFromStrucuture(self):
        folders = [x for x in self.path.rglob('*') if x.is_dir() and x.name in self.points]
        if not folders:
            raise Exception('Os pontos da pasta não foram localizados no banco de pontos.')
        for folder in folders:
            self.executeProcess(folder)
        
    def getListOfPoints(self):
        data = self.fetchAll()
        self.points = list(map(lambda x: x['cod_ponto'], data))

    def executeProcess(self, folder):
        pto = self.fetchOne(folder.name)
        if pto['ponto_base'] == None:
            pto['orbt_base'] = 'Órbita'
        else:
            pto['orbt_base'] = 'Base'
            pto['orbita1'] = pto['ponto_base']
        pto['dataMono'] = date.today().strftime('%d/%m/%Y')
        # Necessário para diminuir o tamanho dos campo no modelo:
        pto['freq'] = pto['freq_processada']
        pto['mc'] = pto['meridiano_central']
        pto['mascara'] = pto['mascara_elevacao']
        pto['taxa'] = pto['taxa_gravacao']
        pto['sigmaXY'] = pto['precisao_horizontal_esperada']
        pto['sigmaZ'] = pto['precisao_vertical_esperada']
        pto['m'] = 'Sim' if pto['materializado'] else 'Não'
        # por algum bug no odt/secretary não dá pra replicar imagem (no caso a assinatura, que está no rodapé)
        pto['signature'] = self.settings['signature']
        pto['signature1'] = self.settings['signature']
        pto['signature2'] = self.settings['signature']
        pto['altitude_ortometrica'] = '{:.2f}'.format(pto['altitude_ortometrica'])
        pto['altitude_geometrica'] = '{:.2f}'.format(pto['altitude_geometrica'])
        pto['durRast'] = pto["fim_rastreio"] - pto["inicio_rastreio"]
        pto['photoCGEO'] = self.settings['pathImageCGEO']
        pto['crea_engenheiro_responsavel'] = 'CREA: '+pto['crea_engenheiro_responsavel'] if pto['crea_engenheiro_responsavel'] else 'CPF: '+pto['cpf_engenheiro_responsavel']
        try:
            pto['inicio_rastreio'] = pto['inicio_rastreio'].strftime('%d/%m/%Y %H:%M:%S')
            pto['data_processamento'] = pto['data_processamento'].strftime('%d/%m/%Y')
        except AttributeError:
            pass

        # Fotos do ponto
        photosPt = [str(f) for f in Path(folder / '3_Foto_Rastreio').iterdir() if f.suffix in self.img_extensions]
        for _idx, _ in enumerate(photosPt):
            pto['photoPt{}'.format(_idx + 1)] = photosPt[_idx]

        # Não esquecer que as visões aéreas tem que ser geradas!
        pto['photoCroqui'] = [str(f) for f in Path(folder / '4_Croqui').iterdir() if f.suffix in self.img_extensions][0]
        pto['photoAerView'] = str(Path(folder / '7_Imagens_Monografia' / '{}_AEREA.jpg'.format(pto["cod_ponto"])))
        pto['photoView2'] = str(Path(folder / '7_Imagens_Monografia' / '{}_MUNICIPIO.jpg'.format(pto["cod_ponto"])))
        pto['photoView1'] = str(Path(folder / '7_Imagens_Monografia' / '{}_ESTADO.jpg'.format(pto["cod_ponto"])))
        # pto['photoAerView'] = [str(f) for f in Path(self.settings['photoAerView']).iterdir() if f.match('{}*.jpg'.format(pto['cod_ponto']))][0]
        # pto['photoView1'] = [str(f) for f in Path(self.settings['photoView1']).iterdir() if f.match('{}*.jpg'.format(pto['cod_ponto']))][0]
        # pto['photoView2'] = [str(f) for f in Path(self.settings['photoView2']).iterdir() if f.match('{}*.jpg'.format(pto['cod_ponto']))][0]

        engine = Renderer()

        # Path do template
        result = engine.render(
            template='./' + self.settings['modelo'] + '.odt', pto=pto)

        # Cria a pasta 8_Monografia
        Path.mkdir(folder / '8_Monografia', exist_ok=True)

        # Gera o arquivo odt temporário
        path_odt = Path(folder / '8_Monografia' / "{}.odt".format(pto['cod_ponto']))
        with open(str(path_odt), 'wb') as output:
            output.write(result)

        # Gera o pdf
        subprocess.run(["{}".format(self.settings['pathLibreOffice']), "--headless", "--convert-to", "pdf", "{}".format(path_odt)])

        # Transfere o pdf para a estrutura de pastas e deleta o odt
        Path.replace(Path.cwd() / '{}.pdf'.format(pto['cod_ponto']), Path(folder / '8_Monografia' / '{}.pdf'.format(pto['cod_ponto'])))
        Path.unlink(path_odt)

        print('Monografia do ponto {} concluída.'.format(pto["cod_ponto"]))

if __name__ == "__main__":
    generate = GenerateMonograpy(*sys.argv[1:])
    generate.getListOfPoints()
    generate.getFoldersFromStrucuture()