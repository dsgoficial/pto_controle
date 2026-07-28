# -*- coding: utf-8 -*-
"""Acesso ao GeoPackage da missão: o que substitui o psycopg2 no plugin.

Duas coisas que o PostGIS dava de graça e aqui precisam de código:

1. **A geometria.** Não há `ST_GeomFromText` no SQLite puro (medido em
   2026-07-28: a função existe no dialeto SQLite do GDAL, e não na conexão
   comum). O ponto vai no formato binário do GeoPackage, montado por `ponto_gpkg`.
2. **A chave estrangeira.** Ela é da CONEXÃO, não do servidor: só vale com
   `PRAGMA foreign_keys=ON`. Use sempre `conecta`, nunca `sqlite3.connect` cru.

Ao portar, os comandos passaram a usar PARÂMETRO em vez de interpolar valor na
string. O código antigo montava `'{}'.format(valor)`, o que quebra em nome com
apóstrofo e não tem defesa nenhuma contra o que vier do CSV do medidor.

Houve aqui uma terceira função, `recontar_controle_medicao`, que substituía o
trigger plpgsql de contagem por polígono. Ela saiu em 2026-07-28, quando o chefe
decidiu que o `controle_medicao_a` e o `ponto_controle_virtual_p` não são
necessários nem no plugin nem no Controle do Acervo. Com ela saiu a dependência
de OGR neste módulo.
"""
import struct

SRID = 4674


def conecta(caminho):
    """Conexão com a missão, com a chave estrangeira LIGADA."""
    from ..createDB.gpkg_schema import conecta as _conecta

    return _conecta(caminho)


def ponto_gpkg(longitude, latitude, srid=SRID):
    """Devolve o BLOB de geometria que o GeoPackage espera, para um ponto 2D.

    O formato é o do padrão OGC GeoPackage: cabeçalho 'GP', versão, flags,
    srs_id, e em seguida o WKB. Sem envelope, que é opcional para ponto.

    Devolve None quando falta coordenada, que é o caso do ponto ainda não
    processado (o P03 grava o ponto antes de existir PPP ou RTE).
    """
    if longitude in (None, "") or latitude in (None, ""):
        return None
    lon, lat = float(longitude), float(latitude)

    # magic 'GP', versão 0, flags 0x01 (cabeçalho little-endian, sem envelope)
    cabecalho = b"GP" + struct.pack("<BBi", 0, 0x01, srid)
    # WKB: byte de ordem (1 = little), tipo 1 (Point), x, y
    wkb = struct.pack("<BIdd", 1, 1, lon, lat)
    return cabecalho + wkb


def _wkb_de(blob):
    """Tira o cabeçalho do GeoPackage e devolve o WKB puro."""
    if not blob or blob[:2] != b"GP":
        return blob
    flags = blob[3]
    envelope = (flags >> 1) & 0x07
    tamanho = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(envelope, 0)
    return blob[8 + tamanho:]


def colunas_da_tabela(con, tabela):
    """Nomes das colunas, lidos do arquivo. Serve para descartar a chave que o CSV
    trouxe e a tabela não tem, em vez de estourar no meio da carga."""
    return [r[1] for r in con.execute(f"PRAGMA table_info({tabela})")]


def upsert_ponto(con, dados, colunas_validas=None):
    """Insere ou atualiza um ponto pelo cod_ponto. Devolve (ação, descartadas).

    Espelha o `ON CONFLICT (cod_ponto) DO UPDATE ... WHERE tipo_situacao IN
    (1,2,4,9999)` do PostGIS: ponto já APROVADO (situação 3) não se sobrescreve
    por recarga de pasta.

    `descartadas` são as chaves que o CSV ou o JSON trouxeram e a tabela não tem.
    O chamador AVISA em vez de engolir, porque campo com nome errado que entra
    calado é o modo de falha mais caro que este vault já catalogou.
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
        marcadores = ", ".join(["?"] * (len(valores) + 1))
        con.execute(
            f"INSERT INTO ponto_controle_p ({col_sql}) VALUES ({marcadores})",
            valores + [geom],
        )
        return "inserido", descartadas

    if existe[0] == 3:
        # Aprovado não se mexe. É a mesma regra do WHERE do ON CONFLICT antigo.
        return "preservado", descartadas

    atribuicoes = ", ".join(f"{c} = ?" for c in campos)
    con.execute(
        f"UPDATE ponto_controle_p SET {atribuicoes}, geom = ? WHERE cod_ponto = ?",
        valores + [geom, dados["cod_ponto"]],
    )
    return "atualizado", descartadas
