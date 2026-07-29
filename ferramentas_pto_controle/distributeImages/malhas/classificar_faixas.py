# Marca cada municipio com a FAIXA de tolerancia que ele suporta.
#
# O criterio e o tamanho do pixel no terreno quando aquele municipio preenche o
# quadro do P08 (100 x 60 mm a 300 dpi, ou 1181 px de largura). Altamira e vista
# com 1097 m por pixel; Santa Cruz de Minas, com 3,7 m. Uma tolerancia unica ou
# desperdica vertice na primeira ou estraga a segunda.
#
# As faixas dobram: cada uma vale ate o dobro do pixel da anterior e leva o dobro
# da tolerancia. Assim o erro medido em PIXEL fica quase constante em todo o pais.
#
# Uso: python classificar_faixas.py CAMINHO.gpkg

import sys

from osgeo import ogr

ogr.UseExceptions()

LARGURA_PX = 1181
RAZAO_QUADRO = 100 / 60
GRAU_EM_METROS = 111320

# limite superior do pixel, em metros -> faixa. Acima do ultimo, a faixa seguinte.
CORTES = [(10, 1), (20, 2), (40, 3), (80, 4), (160, 5)]


def pixel_em_metros(geometria):
    x0, x1, y0, y1 = geometria.GetEnvelope()
    largura = (x1 - x0) * 1.05
    altura = (y1 - y0) * 1.05
    if largura / altura < RAZAO_QUADRO:
        largura = altura * RAZAO_QUADRO
    return largura / LARGURA_PX * GRAU_EM_METROS


def faixa_de(pixel):
    for limite, faixa in CORTES:
        if pixel < limite:
            return faixa
    return CORTES[-1][1] + 1


def main(caminho):
    fonte = ogr.Open(caminho, 1)
    camada = fonte.GetLayer(0)
    if camada.FindFieldIndex('faixa', 1) < 0:
        camada.CreateField(ogr.FieldDefn('faixa', ogr.OFTInteger))

    contagem = {faixa: 0 for _, faixa in CORTES}
    contagem[CORTES[-1][1] + 1] = 0

    camada.StartTransaction()
    for feicao in camada:
        faixa = faixa_de(pixel_em_metros(feicao.GetGeometryRef()))
        feicao.SetField('faixa', faixa)
        camada.SetFeature(feicao)
        contagem[faixa] += 1
    camada.CommitTransaction()

    print('municipios por faixa: ' +
          '  '.join(f'{k}: {v}' for k, v in sorted(contagem.items())))


if __name__ == '__main__':
    main(sys.argv[1])
