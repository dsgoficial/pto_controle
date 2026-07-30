# -*- coding: utf-8 -*-
"""Cria o GeoPackage da missão a partir do MESMO new_db.sql que criava o PostGIS.

O `new_db.sql` continua sendo a única fonte do schema. Manter um `.sql` de
GeoPackage ao lado dele criaria dois arquivos com as mesmas 19 tabelas, que
divergiriam no primeiro campo novo que alguém acrescentasse em um só, e a
divergência seria silenciosa.

A tradução roda quando alguém GERA a semente, e não em campo. O P01 apenas copia
a semente versionada, então o interpretador de SQL nunca roda na máquina de quem
está medindo ponto. O teste `test_schema_gpkg.py` confere tabela a tabela e
coluna a coluna que a semente corresponde ao `new_db.sql`.

O que a tradução faz, e por quê:

- `dominios.X` vira `dominios_X` e `bpc.X` vira `X`. GeoPackage não tem schema.
  O prefixo `bpc.` cai porque é ele que dá o nome das CAMADAS que o usuário vê no
  QGIS, e `ponto_controle_p` é o nome que os algoritmos P08 e P09 já esperam.
- `SERIAL NOT NULL PRIMARY KEY` vira `INTEGER PRIMARY KEY AUTOINCREMENT`, que é o
  que o GDAL reconhece como identificador de feição.
- `VARCHAR(n)` vira `TEXT`. O GDAL avisa "Field format 'VARCHAR(255)' not
  supported", e o tipo canônico do GeoPackage é TEXT.
- `TIMESTAMP WITH TIME ZONE` vira `DATETIME`. Sem isso o SQLite aceita a coluna e
  o GDAL a IGNORA: ela existe no arquivo e some no QGIS. Foi o que aconteceu com
  inicio_rastreio e fim_rastreio, medido em 2026-07-28.
- `geometry(TIPO,4674)` vira a coluna de geometria, registrada no
  `gpkg_geometry_columns`. O `POINTZ` vira POINT com z=1.
- Some o `CREATE EXTENSION`, o `CREATE SCHEMA`, o `ALTER TABLE ... OWNER TO`, o
  índice GiST (o GeoPackage usa RTree) e a tabela `public.layer_styles`, que no
  GeoPackage tem mecanismo próprio.

SMALLINT, FLOAT, REAL, DATE, TIME e BOOLEAN atravessam intactos: são tipos
válidos de GeoPackage.

ARMADILHA que vale registrar: a chave estrangeira do GeoPackage é da CONEXÃO, e
não do servidor. Ela só é verificada com `PRAGMA foreign_keys=ON`, que este módulo
liga em toda escrita. Uma sessão de edição do QGIS sobre a camada NÃO liga, então
editar o atributo à mão pode gravar código de domínio inexistente. No PostgreSQL
isso era impossível. Medido em 2026-07-28.
"""
import hashlib
import re
import shutil
import sqlite3
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE_SQL = AQUI / "new_db.sql"
SEMENTE = AQUI / "missao_semente.gpkg"

SRID = 4674

# Linhas inteiras que não atravessam.
RE_DESCARTE = re.compile(
    r"^\s*(CREATE\s+EXTENSION|CREATE\s+SCHEMA|ALTER\s+TABLE\s+\S+\s+OWNER\s+TO"
    r"|CREATE\s+INDEX)\b",
    re.IGNORECASE,
)
# `geometry(POINT,4674)` e `geometry(POINTZ,4674)`
RE_GEOM = re.compile(r"\bgeometry\(\s*(\w+)\s*,\s*(\d+)\s*\)", re.IGNORECASE)
RE_SERIAL = re.compile(r"\bSERIAL\s+NOT\s+NULL\s+PRIMARY\s+KEY\b", re.IGNORECASE)
RE_VARCHAR = re.compile(r"\bVARCHAR\s*\(\s*\d+\s*\)", re.IGNORECASE)
# `TIMESTAMP WITH TIME ZONE` não é tipo de GeoPackage. Escrito assim, o SQLite
# aceita a coluna e o GDAL a IGNORA: ela existe no arquivo e some no QGIS. Foi o
# que aconteceu com inicio_rastreio e fim_rastreio, medido em 2026-07-28.
RE_TIMESTAMP = re.compile(
    r"\btimestamp(\s+with(out)?\s+time\s+zone)?\b", re.IGNORECASE
)
RE_DEFAULT_NOW = re.compile(r"\bDEFAULT\s+now\(\)", re.IGNORECASE)
RE_CREATE_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?P<esquema>\w+)\.(?P<tabela>\w+)\s*\(", re.IGNORECASE
)


def _renomeia(texto):
    """`dominios.x` vira `dominios_x`; `bpc.x` vira `x`."""
    texto = re.sub(r"\bdominios\.(\w+)", r"dominios_\1", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\bbpc\.(\w+)", r"\1", texto, flags=re.IGNORECASE)
    return texto


def _corta_comentario(linha):
    """Tira o comentario `--` que não esteja dentro de aspas simples."""
    fora = True
    for i, ch in enumerate(linha):
        if ch == "'":
            fora = not fora
        elif ch == "-" and fora and linha[i : i + 2] == "--":
            return linha[:i]
    return linha


def separa_comandos(sql):
    """Quebra o script em comandos.

    Respeita a aspa simples E o `$$` do corpo plpgsql. Sem tratar o `$$`, o corpo
    da função `atualizar_controle_medicao` (que tem `;` em toda linha) e picado em
    fragmentos, e o fragmento final gruda no CREATE TABLE seguinte. Foi assim que a
    tabela `public.layer_styles` escapou do descarte na primeira versão.
    """
    comandos, atual, fora_aspa, fora_cifrao = [], [], True, True
    for linha in sql.splitlines():
        if fora_aspa and fora_cifrao and RE_DESCARTE.match(linha):
            continue
        atual.append(linha)
        i = 0
        while i < len(linha):
            if linha.startswith("$$", i) and fora_aspa:
                fora_cifrao = not fora_cifrao
                i += 2
                continue
            if linha[i] == "'" and fora_cifrao:
                fora_aspa = not fora_aspa
            i += 1
        if fora_aspa and fora_cifrao and linha.rstrip().endswith(";"):
            comandos.append("\n".join(atual))
            atual = []
    if atual and "".join(atual).strip():
        comandos.append("\n".join(atual))
    return [c for c in comandos if c.strip()]


def traduz(sql):
    """Devolve (comandos_ddl, comandos_insert, espaciais).

    `espaciais` e {tabela: (tipo_geom, tem_z)}, o que o registro do GeoPackage
    precisa saber e que o DDL sozinho não diz.
    """
    ddl, inserts, espaciais = [], [], {}

    for comando in separa_comandos(sql):
        bruto = comando.strip()

        alvo_insert = re.match(r"^\s*INSERT\s+INTO\s+(\w+)\.(\w+)", bruto, re.IGNORECASE)
        if alvo_insert:
            # O schema `public` guarda só o layer_styles, que no GeoPackage tem
            # mecanismo próprio. Nada dele atravessa.
            if alvo_insert.group(1).lower() != "public":
                inserts.append(_renomeia(bruto))
            continue

        m = RE_CREATE_TABLE.search(bruto)
        if not m:
            continue  # função, trigger é o que mais não atravessa
        if m.group("esquema").lower() == "public":
            continue

        tabela = m.group("tabela")
        linhas = []
        for linha in bruto.splitlines():
            linha = _corta_comentario(linha).rstrip()
            if not linha.strip():
                continue
            g = RE_GEOM.search(linha)
            if g:
                tipo = g.group(1).upper()
                tem_z = tipo.endswith("Z")
                espaciais[tabela] = (tipo[:-1] if tem_z else tipo, tem_z)
                # A coluna de geometria do GeoPackage não leva NOT NULL: o GDAL
                # escreve a feição antes da geometria em alguns caminhos.
                linha = RE_GEOM.sub(espaciais[tabela][0], linha)
                linha = re.sub(r"\s+NOT\s+NULL", "", linha, flags=re.IGNORECASE)
            linha = RE_SERIAL.sub("INTEGER PRIMARY KEY AUTOINCREMENT", linha)
            linha = RE_VARCHAR.sub("TEXT", linha)
            linha = RE_TIMESTAMP.sub("DATETIME", linha)
            linha = RE_DEFAULT_NOW.sub("DEFAULT CURRENT_TIMESTAMP", linha)
            linhas.append(linha)
        ddl.append(_renomeia("\n".join(linhas)))

    return ddl, inserts, espaciais


def _registra(con, tabela, espaciais):
    """Poe a tabela no catálogo do GeoPackage. Sem isso o GDAL não a enxerga."""
    if tabela in espaciais:
        tipo, tem_z = espaciais[tabela]
        con.execute(
            "INSERT INTO gpkg_contents (table_name, data_type, identifier, srs_id)"
            " VALUES (?, 'features', ?, ?)",
            (tabela, tabela, SRID),
        )
        con.execute(
            "INSERT INTO gpkg_geometry_columns"
            " (table_name, column_name, geometry_type_name, srs_id, z, m)"
            " VALUES (?, 'geom', ?, ?, ?, 0)",
            (tabela, tipo, SRID, 1 if tem_z else 0),
        )
    else:
        con.execute(
            "INSERT INTO gpkg_contents (table_name, data_type, identifier)"
            " VALUES (?, 'attributes', ?)",
            (tabela, tabela),
        )


def digital_do_sql(fonte_sql=None):
    """sha256 do new_db.sql, gravado dentro da semente.

    A guarda de atualidade NÃO pode ser por data de arquivo: num clone novo o git
    escreve todos os arquivos no mesmo instante, e a comparação de mtime aprovaria
    uma semente velha. A impressão digital do CONTEUDO atravessa o clone.
    """
    caminho = fonte_sql or FONTE_SQL
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def gerar_semente(caminho, fonte_sql=None):
    """Gera a SEMENTE, a partir do new_db.sql. Devolve (tabelas, linhas_de_dominio).

    Isto é ferramenta de manutenção, e não roda em campo. Quem mexer no
    `new_db.sql` roda `python -m createDB.gpkg_schema` (ou o teste, que avisa) e
    commita a semente nova. O P01 só COPIA a semente, então o parser de SQL nunca
    roda na máquina de quem esta medindo ponto.
    """
    from osgeo import ogr, osr

    destino = Path(caminho)
    if destino.exists():
        raise FileExistsError(
            f"{destino} ja existe. A geracao nao sobrescreve: apague a semente "
            "antiga de proposito antes de gerar a nova."
        )
    destino.parent.mkdir(parents=True, exist_ok=True)

    sql = (fonte_sql or FONTE_SQL).read_text(encoding="utf-8")
    ddl, inserts, espaciais = traduz(sql)

    # O GDAL semeia gpkg_contents, gpkg_spatial_ref_sys e companhia. A camada
    # semente existe só para o SRID 4674 entrar no gpkg_spatial_ref_sys, e sai
    # logo em seguida. Quem a remove e o próprio OGR: apagar a linha do
    # gpkg_contents na mao viola a chave estrangeira do catálogo, que aponta do
    # gpkg_geometry_columns para ele, e ainda deixaria as tabelas do RTree órfãs.
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(SRID)
    fonte = ogr.GetDriverByName("GPKG").CreateDataSource(str(destino))
    fonte.CreateLayer("semente_srs", srs, ogr.wkbPoint)
    fonte = None

    fonte = ogr.Open(str(destino), 1)
    for i in range(fonte.GetLayerCount()):
        if fonte.GetLayer(i).GetName() == "semente_srs":
            fonte.DeleteLayer(i)
            break
    fonte = None

    con = sqlite3.connect(str(destino))
    try:
        con.execute("PRAGMA foreign_keys=ON")
        for comando in ddl:
            con.execute(comando)
            m = re.search(r"CREATE\s+TABLE\s+(\w+)", comando, re.IGNORECASE)
            _registra(con, m.group(1), espaciais)
        for comando in inserts:
            con.execute(comando)
        # A impressão digital do new_db.sql viaja DENTRO da semente. E ela que o
        # P01 confere antes de copiar, para não entregar uma missão com schema
        # velho. Semente defasada e pior que semente ausente: responde com
        # confiança um schema que já mudou.
        con.execute(
            "CREATE TABLE pto_controle_semente ("
            " chave TEXT NOT NULL PRIMARY KEY, valor TEXT NOT NULL)"
        )
        con.execute(
            "INSERT INTO gpkg_contents (table_name, data_type, identifier)"
            " VALUES ('pto_controle_semente','attributes','pto_controle_semente')"
        )
        con.execute(
            "INSERT INTO pto_controle_semente VALUES ('digital_new_db_sql', ?)",
            (digital_do_sql(fonte_sql),),
        )
        con.commit()
        tabelas = [
            r[0]
            for r in con.execute("SELECT table_name FROM gpkg_contents")
            if r[0] != "pto_controle_semente"
        ]
        dominios = sum(
            con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in tabelas
            if t.startswith("dominios_")
        )
    finally:
        con.close()

    return sorted(tabelas), dominios


def criar_missao(destino, semente=None):
    """Cria o GeoPackage de uma missão COPIANDO a semente. É o que o P01 faz.

    Copiar em vez de traduzir tem duas vantagens que importam em campo: e
    instantaneo, e não depende de interpretar SQL na máquina de quem esta medindo.
    Antes de copiar, confere que a semente corresponde ao `new_db.sql` de hoje.
    """
    origem = Path(semente or SEMENTE)
    alvo = Path(destino)

    if not origem.exists():
        raise FileNotFoundError(
            f"semente ausente: {origem}\n"
            "  Gere com: python -m createDB.gpkg_schema"
        )
    if alvo.exists():
        raise FileExistsError(
            f"{alvo} ja existe. A criacao nao sobrescreve: escolha outro nome ou "
            "apague o arquivo a mao, de proposito."
        )

    con = sqlite3.connect(str(origem))
    try:
        linha = con.execute(
            "SELECT valor FROM pto_controle_semente WHERE chave='digital_new_db_sql'"
        ).fetchone()
    finally:
        con.close()
    atual = digital_do_sql()
    if not linha or linha[0] != atual:
        raise RuntimeError(
            "a semente NAO corresponde ao new_db.sql de hoje.\n"
            f"  semente: {(linha[0] if linha else '(ausente)')[:16]}\n"
            f"  new_db : {atual[:16]}\n"
            "  Alguem mexeu no schema e nao regerou a semente. Conserto:\n"
            "    apague createDB/missao_semente.gpkg e rode\n"
            "    python -m createDB.gpkg_schema"
        )

    alvo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origem, alvo)
    return alvo


def conecta(caminho):
    """Conexão com a FK LIGADA. Use sempre esta, nunca o sqlite3.connect cru:
    sem o PRAGMA a chave estrangeira não é verificada e o código de domínio
    inválido entra calado."""
    con = sqlite3.connect(str(caminho))
    con.execute("PRAGMA foreign_keys=ON")
    return con


if __name__ == "__main__":
    # Ferramenta de manutenção: regera a semente depois de mexer no new_db.sql.
    if SEMENTE.exists():
        print(f"A semente ja existe: {SEMENTE}")
        print("Apague-a de proposito antes de gerar a nova.")
        sys.exit(1)
    tabelas, dominios = gerar_semente(SEMENTE)
    print(f"semente gerada: {SEMENTE}")
    print(f"  {len(tabelas)} tabelas, {dominios} linhas de dominio")
    print(f"  digital do new_db.sql: {digital_do_sql()[:16]}")
    print("\nCommite a semente junto com a mudanca do new_db.sql.")
