# -*- coding: utf-8 -*-
"""Acesso ao GeoPackage da missao: o que substitui o psycopg2 no plugin.

Tres coisas que o PostGIS dava de graca e aqui precisam de codigo:

1. **A geometria.** Nao ha `ST_GeomFromText` no SQLite puro (medido em
   2026-07-28: a funcao existe no dialeto SQLite do GDAL, e nao na conexao comum).
   O ponto vai no formato binario do GeoPackage, montado por `ponto_gpkg`.
2. **A chave estrangeira.** Ela e da CONEXAO, nao do servidor: so vale com
   `PRAGMA foreign_keys=ON`. Use sempre `conecta`, nunca `sqlite3.connect` cru.
3. **A recontagem do controle_medicao_a.** Era trigger plpgsql com `ST_Intersects`
   a cada INSERT, UPDATE e DELETE. Virou `recontar_controle_medicao`, chamada ao
   fim das rotinas que escrevem ponto.

Ao portar, os comandos passaram a usar PARAMETRO em vez de interpolar valor na
string. O codigo antigo montava `'{}'.format(valor)`, o que quebra em nome com
apostrofo e nao tem defesa nenhuma contra o que vier do CSV do medidor.
"""
import struct
from pathlib import Path

SRID = 4674


def conecta(caminho):
    """Conexao com a missao, com a chave estrangeira LIGADA."""
    from ..createDB.gpkg_schema import conecta as _conecta

    return _conecta(caminho)


def ponto_gpkg(longitude, latitude, srid=SRID):
    """Devolve o BLOB de geometria que o GeoPackage espera, para um ponto 2D.

    O formato e o do padrao OGC GeoPackage: cabecalho 'GP', versao, flags,
    srs_id, e em seguida o WKB. Sem envelope, que e opcional para ponto.
    Devolve None quando falta coordenada, que e o caso do ponto ainda nao
    processado (o P03 grava o ponto antes de existir PPP ou RTE).
    """
    if longitude in (None, "") or latitude in (None, ""):
        return None
    lon, lat = float(longitude), float(latitude)

    # magic 'GP', versao 0, flags 0x01 (cabecalho little-endian, sem envelope)
    cabecalho = b"GP" + struct.pack("<BBi", 0, 0x01, srid)
    # WKB: byte de ordem (1 = little), tipo 1 (Point), x, y
    wkb = struct.pack("<BIdd", 1, 1, lon, lat)
    return cabecalho + wkb


def _le_geometria(blob):
    """(lon, lat) de um BLOB de ponto do GeoPackage, ou None. Usado na conferencia."""
    if not blob or blob[:2] != b"GP":
        return None
    flags = blob[3]
    envelope = (flags >> 1) & 0x07
    tamanho_envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(envelope, 0)
    inicio = 8 + tamanho_envelope
    ordem, tipo = struct.unpack_from("<BI", blob, inicio)
    if tipo != 1:
        return None
    return struct.unpack_from("<dd", blob, inicio + 5)


def colunas_da_tabela(con, tabela):
    """Nomes das colunas, lidos do arquivo. Serve para descartar a chave que o CSV
    trouxe e a tabela nao tem, em vez de estourar no meio da carga."""
    return [r[1] for r in con.execute(f"PRAGMA table_info({tabela})")]


def upsert_ponto(con, dados, colunas_validas=None):
    """Insere ou atualiza um ponto pelo cod_ponto. Devolve (acao, descartadas).

    Espelha o `ON CONFLICT (cod_ponto) DO UPDATE ... WHERE tipo_situacao IN
    (1,2,4,9999)` do PostGIS: ponto ja APROVADO (situacao 3) nao se sobrescreve
    por recarga de pasta.

    `descartadas` sao as chaves que o CSV ou o JSON trouxeram e a tabela nao tem.
    O chamador AVISA em vez de engolir, porque campo com nome errado que entra
    calado e o modo de falha mais caro que este vault ja catalogou.
    """
    if colunas_validas is None:
        colunas_validas = colunas_da_tabela(con, "ponto_controle_p")
    validas = set(colunas_validas)

    dados = dict(dados)
    descartadas = sorted(k for k in dados if k not in validas)
    for k in descartadas:
        dados.pop(k)

    geom = ponto_gpkg(dados.get("longitude"), dados.get("latitude"))
    campos = [k for k, v in dados.items() if v not in (None, "")]
    valores = [dados[k] for k in campos]

    existe = con.execute(
        "SELECT tipo_situacao FROM ponto_controle_p WHERE cod_ponto = ?",
        (dados["cod_ponto"],),
    ).fetchone()

    if existe is None:
        col_sql = ", ".join(campos + ["geom"])
        marc = ", ".join(["?"] * (len(valores) + 1))
        con.execute(
            f"INSERT INTO ponto_controle_p ({col_sql}) VALUES ({marc})",
            valores + [geom],
        )
        return "inserido", descartadas

    if existe[0] == 3:
        # Aprovado nao se mexe. E a mesma regra do WHERE do ON CONFLICT antigo.
        return "preservado", descartadas

    atrib = ", ".join(f"{c} = ?" for c in campos)
    con.execute(
        f"UPDATE ponto_controle_p SET {atrib}, geom = ? WHERE cod_ponto = ?",
        valores + [geom, dados["cod_ponto"]],
    )
    return "atualizado", descartadas


def recontar_controle_medicao(con):
    """Recalcula total_pontos_aprovados e total_pontos_em_avaliacao por poligono.

    Substitui a funcao plpgsql `atualizar_controle_medicao`, que era disparada por
    trigger. O SQLite nao tem `ST_Intersects` na conexao comum, entao o teste de
    ponto em poligono acontece aqui, pelo OGR.

    Diferenca de comportamento que vale registrar: no PostgreSQL a recontagem era
    por LINHA e automatica. Aqui ela e por LOTE e explicita, entao quem escreve
    ponto tem de chamar. Em compensacao, custa uma passada em vez de uma por
    ponto inserido.

    Devolve quantos poligonos foram atualizados.
    """
    from osgeo import ogr

    poligonos = []
    for fid, blob in con.execute(
        "SELECT id, geom FROM controle_medicao_a WHERE geom IS NOT NULL"
    ):
        # O BLOB do GeoPackage tem cabecalho antes do WKB; o OGR le o formato.
        geom = ogr.CreateGeometryFromWkb(_wkb_de(blob))
        if geom is not None:
            poligonos.append((fid, geom))

    if not poligonos:
        return 0

    pontos = []
    for situacao, blob in con.execute(
        "SELECT tipo_situacao, geom FROM ponto_controle_p WHERE geom IS NOT NULL"
    ):
        coord = _le_geometria(blob)
        if coord:
            p = ogr.Geometry(ogr.wkbPoint)
            p.AddPoint_2D(coord[0], coord[1])
            pontos.append((situacao, p))

    tocados = 0
    for fid, poligono in poligonos:
        aprovados = sum(1 for s, p in pontos if s == 3 and poligono.Intersects(p))
        avaliacao = sum(1 for s, p in pontos if s == 2 and poligono.Intersects(p))
        con.execute(
            "UPDATE controle_medicao_a SET total_pontos_aprovados = ?,"
            " total_pontos_em_avaliacao = ? WHERE id = ?",
            (aprovados, avaliacao, fid),
        )
        tocados += 1
    return tocados


def _wkb_de(blob):
    """Tira o cabecalho do GeoPackage e devolve o WKB puro."""
    if not blob or blob[:2] != b"GP":
        return blob
    flags = blob[3]
    envelope = (flags >> 1) & 0x07
    tamanho = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(envelope, 0)
    return blob[8 + tamanho:]
