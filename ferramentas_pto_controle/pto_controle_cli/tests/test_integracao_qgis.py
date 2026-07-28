# -*- coding: utf-8 -*-
"""
Testes que precisam do QGIS instalado, com o plugin habilitado PARA O qgis_process.

Pulam sozinhos quando o qgis_process não esta ao alcance, então rodam na máquina de
quem desenvolve e não quebram um CI sem QGIS. Sao caros: cada chamada sobe o QGIS
inteiro (segundos), por isso são poucos e o contrato fica em cache entre eles.

Rodam contra o provider REAL, nunca contra mock. E o ponto do desenho: o valor de
ler o contrato ao vivo e não ter copia, e testar contra copia testaria justamente a
copia. Quando o plugin mudar, estes testes quebram, e e esse o alarme.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_integracao_qgis.py -v
"""
import ast
import importlib.util
import json
import re
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
# O CLI mora dentro do pacote do plugin, então o plugin e a pasta de cima.
PLUGIN = CLI_DIR.parent

_spec = importlib.util.spec_from_file_location("pto_controle_cli_integracao", CLI_DIR / "pto_controle_cli.py")
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)

needs_qgis = pytest.mark.skipif(
    cli.find_qgis_process() is None,
    reason="qgis_process nao encontrado (defina PTOCONTROLE_QGIS_PROCESS)",
)


def _python_do_qgis():
    """Interpretador que TEM o módulo `qgis`, ao lado do qgis_process, ou None.

    O CLI roda em qualquer python de propósito, e o python da suite também. Importar
    `qgis` exige o interpretador do QGIS, que não tem pytest instalado. Em vez de
    pedir instalação na máquina de quem desenvolve, os testes que precisam do módulo
    delegam a checagem a um subprocesso deste interpretador.
    """
    qp = cli.find_qgis_process()
    if not qp:
        return None
    for nome in ("python-qgis.bat", "python-qgis", "python3", "python"):
        cand = Path(qp).parent / nome
        if cand.exists():
            return str(cand)
    return None


needs_qgis_python = pytest.mark.skipif(
    _python_do_qgis() is None,
    reason="nao achei o python do QGIS ao lado do qgis_process",
)


def _ids_do_fonte():
    """Ids que o FONTE declara, lidos por ast. A referência contra a qual se compara
    o que o QGIS realmente carregou."""
    ids = set()
    for caminho in sorted(p for p in PLUGIN.rglob("*.py") if CLI_DIR not in p.parents):
        arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
        for no in ast.walk(arvore):
            if not isinstance(no, ast.ClassDef):
                continue
            if "QgsProcessingAlgorithm" not in [b.id for b in no.bases if isinstance(b, ast.Name)]:
                continue
            for metodo in no.body:
                if not (isinstance(metodo, ast.FunctionDef) and metodo.name == "name"):
                    continue
                for corpo in metodo.body:
                    if isinstance(corpo, ast.Return) and isinstance(corpo.value, ast.Constant):
                        ids.add(corpo.value.value)
    return ids


@pytest.fixture(scope="module")
def tabela():
    tab = cli.list_algorithms()
    if not tab:
        pytest.skip(
            "o provider ptocontrole carregou 0 algoritmos. "
            "Rode `python pto_controle_cli.py doctor --fix` e repita."
        )
    return tab


@needs_qgis
def test_o_provider_carrega_todos_os_algoritmos_do_fonte(tabela):
    """Pega os dois lados: algoritmo no fonte que o QGIS não carregou (erro de import
    ou addAlgorithm esquecido) e algoritmo no QGIS que sumiu do fonte."""
    assert set(tabela) == _ids_do_fonte()


@needs_qgis
def test_todo_id_e_invocavel_sem_aspas(tabela):
    """A razao de existir do conserto de 2026-07-28: id com espaço ou acento não se
    escreve numa linha de comando nem numa documentacao."""
    for nome in tabela:
        assert re.match(r"^[a-z0-9]+$", nome), f"id nao invocavel: {nome!r}"


@needs_qgis
def test_o_rotulo_humano_sobreviveu(tabela):
    """O título numerado é o que o usuário do QGIS Desktop ve é o que casa com o
    P01..P16 do manual. Ele mora no displayName, e é o que o `list` mostra."""
    for nome, rotulo in tabela.items():
        assert re.match(r"^\d{2} - ", rotulo), f"{nome}: rótulo inesperado {rotulo!r}"


@needs_qgis
def test_describe_devolve_contrato_de_verdade(tabela):
    alg = "ptocontrole:criarbanco"
    if "criarbanco" not in tabela:
        pytest.skip("criarbanco nao esta na lista")
    data, code, _cached = cli.help_json_cached(alg, refresh=True)
    assert data is not None, f"help falhou (exit {code})"
    params = data.get("parameters", {})
    assert params, "contrato sem parametros"
    # Desde a troca do PostgreSQL pelo GeoPackage, o P01 recebe um destino de
    # arquivo e mais nada. Não se afirma o NOME do parâmetro aqui, que e do
    # contrato vivo; afirma-se que ha uma saida de arquivo.
    assert any(p.get("is_destination") for p in params.values()), (
        f"esperava um parametro de saida em {alg}; achei {sorted(params)}"
    )


@needs_qgis
def test_nenhum_algoritmo_pede_segredo(tabela):
    """Desde a troca do PostgreSQL pelo GeoPackage, a missão e um arquivo e nenhum
    algoritmo recebe senha. O guardrail de segredo do CLI foi REMOVIDO por isso.

    Esta guarda fica: se um parâmetro de senha ou token voltar, alguém
    reintroduziu credencial na linha de comando, e o guardrail precisa voltar
    junto. Aqui o alarme custa uma regex, e não um módulo inteiro de código morto.
    """
    parece_segredo = re.compile(r"senha|password|passwd|secret|token", re.IGNORECASE)
    achados = []
    for nome in sorted(tabela):
        data, _code, _cached = cli.help_json_cached(f"{cli.PROVIDER}:{nome}")
        if data is None:
            continue
        achados += [
            f"{nome}.{p}" for p in data.get("parameters", {}) if parece_segredo.search(p)
        ]
    assert not achados, (
        "parametro de segredo voltou ao plugin: " + ", ".join(achados)
        + ". Reponha o guardrail do CLI (mascara na saida e leitura do ambiente)."
    )


@needs_qgis
def test_todo_algoritmo_tem_descricao_viva(tabela):
    """O `qgis_process help --json` NÃO expoe o shortHelpString(), que é o help
    longo do painel do QGIS. O único canal de descrição que chega ao headless e o
    shortDescription(). Sem ele o `describe` sai sem uma linha do que o algoritmo
    faz, e ninguém percebe: o autor ve o texto na GUI e supoe que o CLI também ve.
    """
    sem_descricao = []
    for nome in sorted(tabela):
        data, code, _cached = cli.help_json_cached(f"{cli.PROVIDER}:{nome}")
        if data is None:
            pytest.skip(f"help de {nome} falhou (exit {code})")
        if not (data.get("algorithm_details", {}).get("short_description") or "").strip():
            sem_descricao.append(nome)
    assert not sem_descricao, (
        "sem shortDescription(): " + ", ".join(sem_descricao)
        + ". O shortHelpString() nao supre: o qgis_process nao o expoe."
    )


@needs_qgis
def test_resolucao_por_prefixo(tabela):
    if "criarbanco" not in tabela:
        pytest.skip("criarbanco nao esta na lista")
    assert cli.resolve_alg("criarbanco") == "ptocontrole:criarbanco"
    assert cli.resolve_alg("criarban") == "ptocontrole:criarbanco"


@needs_qgis
def test_prefixo_ambiguo_e_erro_e_nao_escolha_silenciosa(tabela):
    ambiguos = [p for p in ("atualizar", "distribuir", "preparar")
                if sum(1 for n in tabela if n.startswith(p)) > 1]
    if not ambiguos:
        pytest.skip("nenhum prefixo ambiguo na lista atual")
    with pytest.raises(SystemExit) as exc:
        cli.resolve_alg(ambiguos[0])
    assert "casa com" in str(exc.value)


@needs_qgis
def test_dry_run_reprova_corpo_invalido_sem_executar(tabela):
    """O portao que economiza a execução cara. Código 2 e 'nada foi executado'."""
    if "criarbanco" not in tabela:
        pytest.skip("criarbanco nao esta na lista")
    argv = ["run", "criarbanco", "PARAMETRO_QUE_NAO_EXISTE=1", "--dry-run"]
    assert cli.main(argv) == 2


# --------------------------------------------------------------------------
# Enum do Qt: o que a migracao para Qt6 deixou para tras
#
# Achado em 2026-07-28, pelo chefe, abrindo um algoritmo na caixa de ferramentas:
# `QLineEdit.Password` não existe em Qt6 (virou `QLineEdit.EchoMode.Password`) e
# derruba a janela de TODO algoritmo com senha. O `metadata.txt` declarava
# `supportsQt6=True` desde 2026-03-10, mas a declaracao não migra código.
#
# O teste não carrega lista de enums removidos, que seria catálogo copiado e
# apodreceria. Ele le do FONTE cada acesso `Classe.atributo` onde a Classe veio de
# um `qgis.PyQt.*`, e resolve contra a biblioteca VIVA. Enum novo que o Qt remover
# amanha aparece sozinho.
#
# Só pega o que a GUI usaria: o caminho headless não constrói widget, e foi por isso
# que os 99 testes e a execução real do validarestrutura passaram com o defeito de pe.
# --------------------------------------------------------------------------
def _acessos_qt_no_fonte():
    """[(arquivo, linha, 'Classe', 'atributo', 'módulo')] do plugin inteiro."""
    achados = []
    for caminho in sorted(p for p in PLUGIN.rglob("*.py") if CLI_DIR not in p.parents):
        arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
        # nome importado -> módulo de origem, só para os módulos do qgis.PyQt
        origem = {}
        for no in ast.walk(arvore):
            if isinstance(no, ast.ImportFrom) and (no.module or "").startswith("qgis.PyQt"):
                for alias in no.names:
                    origem[alias.asname or alias.name] = no.module
        if not origem:
            continue
        for no in ast.walk(arvore):
            if not isinstance(no, ast.Attribute) or not isinstance(no.value, ast.Name):
                continue
            if no.value.id in origem:
                achados.append((caminho, no.lineno, no.value.id, no.attr, origem[no.value.id]))
    return achados


# Roda DENTRO do python do QGIS: recebe os acessos por stdin e devolve os que não
# resolvem. Mantido curto de propósito, porque vai como argumento de `-c`.
_SONDA = """
import importlib, json, sys
quebrados = []
for modulo, classe, atributo, onde in json.load(sys.stdin):
    try:
        alvo = getattr(importlib.import_module(modulo), classe)
    except (ImportError, AttributeError):
        quebrados.append(onde + ' ' + modulo + '.' + classe + ' nao importa')
        continue
    if not hasattr(alvo, atributo):
        quebrados.append(
            onde + ' ' + classe + '.' + atributo + ' nao existe neste Qt'
            + ' (em Qt6 o enum e escopado: ' + classe + '.<Enum>.' + atributo + ')'
        )
json.dump(quebrados, sys.stdout)
"""


@needs_qgis_python
def test_todo_acesso_a_enum_do_qt_existe_na_biblioteca_viva(tmp_path):
    import subprocess

    acessos = _acessos_qt_no_fonte()
    assert acessos, "nao achei acesso nenhum ao qgis.PyQt; o coletor deve ter quebrado"

    carga = [
        [modulo, classe, atributo, f"{caminho.name}:{linha}"]
        for caminho, linha, classe, atributo, modulo in acessos
    ]
    # A sonda vai em ARQUIVO, nunca por `-c`: a quebra de linha dentro de um argumento
    # termina a linha de comando do `cmd /c`, e a sonda chegaria truncada.
    script = tmp_path / "sonda_qt.py"
    script.write_text(_SONDA, encoding="utf-8")

    python = _python_do_qgis()
    comando = ["cmd", "/c", python, str(script)] if python.lower().endswith(".bat") \
        else [python, str(script)]
    proc = subprocess.run(
        comando, input=json.dumps(carga), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        pytest.skip(f"a sonda no python do QGIS falhou: {proc.stderr.strip()[:200]}")
    try:
        quebrados = json.loads(proc.stdout.strip())
    except json.JSONDecodeError:
        pytest.skip(f"saida inesperada da sonda: {proc.stdout.strip()[:200]}")
    assert not quebrados, "\n".join(quebrados)
