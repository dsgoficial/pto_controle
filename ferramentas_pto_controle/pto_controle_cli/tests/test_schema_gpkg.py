# -*- coding: utf-8 -*-
"""
Prova que a SEMENTE do GeoPackage carrega o MESMO schema que o PostGIS carregava.

O `new_db.sql` continua sendo a unica fonte do schema. A semente
(`createDB/missao_semente.gpkg`) e derivada dele por `gpkg_schema.gerar_semente`,
versionada, e o P01 apenas a COPIA: em campo nao se interpreta SQL.

Semente e artefato derivado, e artefato derivado apodrece. Sao duas guardas:

- `test_semente_corresponde_ao_new_db_sql` compara a impressao digital gravada
  dentro da semente com a do `new_db.sql` de hoje. Nao precisa de GDAL, entao roda
  SEMPRE. E a guarda que pega o esquecimento de regerar.
- as demais abrem a semente e comparam tabela a tabela e coluna a coluna.

A guarda e por CONTEUDO e nao por data: num clone novo o git escreve todos os
arquivos no mesmo instante, e comparar mtime aprovaria uma semente velha.

Confere as DUAS superficies, e a distincao nao e teorica. Coluna de tipo invalido
no GeoPackage (foi o caso de `TIMESTAMP WITH TIME ZONE`) EXISTE no arquivo, passa
na conferencia por SQLite, e some para o GDAL, ou seja, some no QGIS. Achado em
2026-07-28, quando `inicio_rastreio` e `fim_rastreio` ficaram invisiveis.

Roda num subprocesso do python do QGIS, que e onde o GDAL existe. O python da
suite nao tem osgeo, e instalar na maquina de quem desenvolve nao e nosso papel.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_schema_gpkg.py -v
"""
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
PLUGIN = CLI_DIR.parent

_spec = importlib.util.spec_from_file_location(
    "pto_controle_cli_schema", CLI_DIR / "pto_controle_cli.py"
)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)


def _python_do_qgis():
    qp = cli.find_qgis_process()
    if not qp:
        return None
    for nome in ("python-qgis.bat", "python-qgis", "python3", "python"):
        cand = Path(qp).parent / nome
        if cand.exists():
            return str(cand)
    return None


needs_gdal = pytest.mark.skipif(
    _python_do_qgis() is None,
    reason="nao achei o python do QGIS (e onde mora o GDAL)",
)

# --------------------------------------------------------------------------
# A guarda principal: nao precisa de GDAL, entao nunca pula.
# --------------------------------------------------------------------------
def test_semente_corresponde_ao_new_db_sql():
    """Pega o esquecimento de regerar a semente depois de mexer no schema.

    Semente defasada e PIOR que semente ausente: ela entrega uma missao com
    schema velho, com confianca e sem aviso."""
    import hashlib
    import sqlite3

    semente = PLUGIN / "createDB" / "missao_semente.gpkg"
    assert semente.exists(), (
        f"semente ausente: {semente}. Gere com: python -m createDB.gpkg_schema"
    )
    con = sqlite3.connect(str(semente))
    try:
        linha = con.execute(
            "SELECT valor FROM pto_controle_semente WHERE chave='digital_new_db_sql'"
        ).fetchone()
    finally:
        con.close()
    atual = hashlib.sha256(
        (PLUGIN / "createDB" / "new_db.sql").read_bytes()
    ).hexdigest()
    assert linha and linha[0] == atual, (
        "a semente nao corresponde ao new_db.sql de hoje.\n"
        "  Conserto: apague createDB/missao_semente.gpkg e rode\n"
        "            python -m createDB.gpkg_schema"
    )


# Roda dentro do python do QGIS: copia a semente e devolve o que ela tem,
# pelo SQLite e pelo GDAL, para o teste comparar aqui fora.
_SONDA = r"""
import json, sys, tempfile, importlib.util
from pathlib import Path

plugin = Path(sys.argv[1])
destino = Path(tempfile.mkdtemp()) / "missao.gpkg"

spec = importlib.util.spec_from_file_location("gs", plugin / "createDB" / "gpkg_schema.py")
gs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gs)

gs.criar_missao(destino)

con = gs.conecta(destino)
tabelas = [r[0] for r in con.execute("SELECT table_name FROM gpkg_contents")
           if r[0] != "pto_controle_semente"]
dominios = sum(con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
               for t in tabelas if t.startswith("dominios_"))
no_arquivo = {t: sorted(r[1].lower() for r in con.execute("PRAGMA table_info(%s)" % t))
              for t in tabelas}
con.close()

from osgeo import ogr, gdal
gdal.UseExceptions()
ds = ogr.Open(str(destino))
visivel, geometrias = {}, {}
for i in range(ds.GetLayerCount()):
    lyr = ds.GetLayer(i)
    dfn = lyr.GetLayerDefn()
    campos = [dfn.GetFieldDefn(j).GetName().lower() for j in range(dfn.GetFieldCount())]
    if lyr.GetFIDColumn():
        campos.append(lyr.GetFIDColumn().lower())
    if lyr.GetGeometryColumn():
        campos.append(lyr.GetGeometryColumn().lower())
        srs = lyr.GetSpatialRef()
        geometrias[lyr.GetName()] = [
            ogr.GeometryTypeToName(lyr.GetGeomType()),
            srs.GetAuthorityCode(None) if srs else None,
        ]
    visivel[lyr.GetName()] = sorted(set(campos))
ds = None
no_arquivo = {t: c for t, c in no_arquivo.items() if t != "pto_controle_semente"}
visivel = {t: c for t, c in visivel.items() if t != "pto_controle_semente"}

json.dump({"tabelas": tabelas, "dominios": dominios,
           "no_arquivo": no_arquivo, "visivel": visivel,
           "geometrias": geometrias}, sys.stdout)
"""


@pytest.fixture(scope="module")
def gpkg(tmp_path_factory):
    script = tmp_path_factory.mktemp("sonda") / "sonda_schema.py"
    script.write_text(_SONDA, encoding="utf-8")
    python = _python_do_qgis()
    comando = ["cmd", "/c", python, str(script), str(PLUGIN)] \
        if python.lower().endswith(".bat") else [python, str(script), str(PLUGIN)]
    proc = subprocess.run(
        comando, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if proc.returncode != 0:
        pytest.skip(f"a sonda no python do QGIS falhou: {proc.stderr.strip()[-400:]}")
    try:
        return json.loads(proc.stdout.strip())
    except json.JSONDecodeError:
        pytest.skip(f"saida inesperada da sonda: {proc.stdout.strip()[:300]}")


def _declarado_no_postgis():
    """{tabela: [colunas]} lido do new_db.sql, o lado PostGIS da comparacao."""
    import re

    sql = (PLUGIN / "createDB" / "new_db.sql").read_text(encoding="utf-8")
    esperado = {}
    for m in re.finditer(
        r"CREATE\s+TABLE\s+(\w+)\.(\w+)\s*\((?P<corpo>[\s\S]*?)\n\);", sql, re.IGNORECASE
    ):
        esquema, tabela = m.group(1), m.group(2)
        if esquema == "public":
            continue  # layer_styles: o GeoPackage tem mecanismo proprio
        nome = f"dominios_{tabela}" if esquema == "dominios" else tabela
        colunas = []
        for linha in m.group("corpo").splitlines():
            linha = linha.split("--")[0].strip().rstrip(",")
            if not linha or re.match(
                r"^(CONSTRAINT|PRIMARY\s+KEY|UNIQUE|FOREIGN)\b", linha, re.IGNORECASE
            ):
                continue
            colunas.append(linha.split()[0].lower())
        esperado[nome] = sorted(colunas)
    return esperado


@needs_gdal
def test_nenhuma_tabela_se_perdeu(gpkg):
    esperado = _declarado_no_postgis()
    assert set(esperado) == set(gpkg["no_arquivo"]), (
        f"so no PostGIS: {sorted(set(esperado) - set(gpkg['no_arquivo']))}; "
        f"so no GeoPackage: {sorted(set(gpkg['no_arquivo']) - set(esperado))}"
    )


@needs_gdal
def test_nenhuma_coluna_se_perdeu(gpkg):
    esperado = _declarado_no_postgis()
    divergencias = []
    for nome, colunas in sorted(esperado.items()):
        obtidas = set(gpkg["no_arquivo"].get(nome, []))
        faltando = set(colunas) - obtidas
        sobrando = obtidas - set(colunas)
        if faltando:
            divergencias.append(f"{nome}: PERDEU {sorted(faltando)}")
        if sobrando:
            divergencias.append(f"{nome}: coluna a mais {sorted(sobrando)}")
    assert not divergencias, "\n".join(divergencias)


@needs_gdal
def test_toda_coluna_do_arquivo_e_visivel_ao_gdal(gpkg):
    """A conferencia que a comparacao por SQLite NAO faz.

    Coluna com tipo que o GeoPackage nao define existe no arquivo e some no QGIS.
    Aconteceu com TIMESTAMP WITH TIME ZONE em inicio_rastreio e fim_rastreio."""
    invisiveis = []
    for nome, colunas in sorted(gpkg["no_arquivo"].items()):
        some = set(colunas) - set(gpkg["visivel"].get(nome, []))
        if some:
            invisiveis.append(f"{nome}: {sorted(some)}")
    assert not invisiveis, (
        "coluna existe no arquivo e o GDAL nao enxerga (tipo invalido no "
        "GeoPackage):\n" + "\n".join(invisiveis)
    )


@needs_gdal
def test_as_tres_camadas_espaciais_tem_geometria_e_srs(gpkg):
    esperado = {
        "ponto_controle_p": "Point",
        "controle_medicao_a": "Polygon",
        "ponto_controle_virtual_p": "3D Point",
    }
    for nome, tipo in esperado.items():
        assert nome in gpkg["geometrias"], f"{nome} nao tem coluna de geometria"
        obtido, srs = gpkg["geometrias"][nome]
        assert obtido == tipo, f"{nome}: geometria {obtido}, esperava {tipo}"
        assert srs == "4674", f"{nome}: SRS {srs}, esperava 4674"


@needs_gdal
def test_os_dominios_foram_semeados(gpkg):
    """Sem os codigos semeados, toda escrita bate na chave estrangeira."""
    assert gpkg["dominios"] == 98, (
        f"{gpkg['dominios']} linhas de dominio, esperava 98. "
        "Se o new_db.sql ganhou ou perdeu codigo, ajuste o numero aqui de proposito."
    )
    assert sum(1 for t in gpkg["tabelas"] if t.startswith("dominios_")) == 15
