# -*- coding: utf-8 -*-
"""
Guarda dos IDS do plugin, lida do fonte por `ast` (sem importar QGIS).

Por que este teste existe: em um QgsProcessingAlgorithm, o `name()` E o
identificador, não o rótulo. Ate 2026-07-28 os 15 algoritmos devolviam ali o
título humano ('01 - Criar banco de dados'), o que produzia ids com espaço e
acento e tornava o plugin inutilizável pelo qgis_process. O conserto só se
sustenta com um alarme: quem colar um título no `name()` de novo quebra aqui.

Le o fonte com `ast` de propósito. Importar os módulos exigiria o QGIS, e a
propriedade que se quer garantir e sintática, não de execução.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_ids_do_plugin.py -v
"""
import ast
import json
import re
from pathlib import Path

import pytest

CLI_DIR = Path(__file__).resolve().parent.parent
# O CLI mora dentro do pacote do plugin, então o plugin e a pasta de cima.
PLUGIN = CLI_DIR.parent
ANNOTATIONS = CLI_DIR / "annotations.json"

# A regra do QGIS, transcrita do docstring que o próprio plugin carrega:
# "Names should contain lowercase alphanumeric characters only and no spaces or
# other formatting characters."
RE_ID_VALIDO = re.compile(r"^[a-z0-9]+$")
PROVIDER = "ptocontrole"


def _retorno_constante(classe, metodo):
    """String devolvida por `def <metodo>(self): return '...'`, ou None.

    None quer dizer 'não é uma constante' (ex.: `return self.tr(self.name())`),
    que é informação útil para o teste, não falha de leitura.
    """
    for no in classe.body:
        if not isinstance(no, ast.FunctionDef) or no.name != metodo:
            continue
        for corpo in no.body:
            if isinstance(corpo, ast.Return) and isinstance(corpo.value, ast.Constant):
                if isinstance(corpo.value.value, str):
                    return corpo.value.value
    return None


def _chamada_tr_constante(classe, metodo):
    """String dentro de `return self.tr('...')`, ou None."""
    for no in classe.body:
        if not isinstance(no, ast.FunctionDef) or no.name != metodo:
            continue
        for corpo in no.body:
            if not (isinstance(corpo, ast.Return) and isinstance(corpo.value, ast.Call)):
                continue
            args = corpo.value.args
            if args and isinstance(args[0], ast.Constant) and isinstance(args[0].value, str):
                return args[0].value
    return None


def _classes_de(caminho, base):
    arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    for no in ast.walk(arvore):
        if not isinstance(no, ast.ClassDef):
            continue
        nomes_base = [b.id for b in no.bases if isinstance(b, ast.Name)]
        if base in nomes_base:
            yield no


def fontes_do_plugin():
    """Os .py do plugin, fora a pasta do próprio CLI (que não tem algoritmo)."""
    return sorted(p for p in PLUGIN.rglob("*.py") if CLI_DIR not in p.parents)


def algoritmos():
    """[(arquivo, classe_ast)] de todo QgsProcessingAlgorithm do plugin."""
    achados = []
    for caminho in fontes_do_plugin():
        for classe in _classes_de(caminho, "QgsProcessingAlgorithm"):
            achados.append((caminho, classe))
    return achados


ALGORITMOS = algoritmos()


def test_achou_os_algoritmos():
    """Se este teste quebrar, os outros deste arquivo passariam por vacuidade.

    Eram 15 até 2026-07-28, quando o P17 (preparar a missão para o Controle do
    Acervo) entrou. Ao acrescentar algoritmo, ajuste este número de PROPOSITO."""
    assert len(ALGORITMOS) == 16, [c.name for _, c in ALGORITMOS]


@pytest.mark.parametrize("caminho,classe", ALGORITMOS, ids=lambda x: getattr(x, "name", ""))
def test_name_e_um_id_valido(caminho, classe):
    nome = _retorno_constante(classe, "name")
    assert nome is not None, f"{classe.name}: name() nao devolve uma string constante"
    assert RE_ID_VALIDO.match(nome), (
        f"{classe.name} em {caminho.name}: name() devolve {nome!r}. "
        "O name() é o ID do algoritmo: só minúscula e dígito, sem espaço, acento, "
        "hífen ou numeração. O título humano vai no displayName()."
    )


@pytest.mark.parametrize("caminho,classe", ALGORITMOS, ids=lambda x: getattr(x, "name", ""))
def test_display_name_carrega_o_titulo_humano(caminho, classe):
    """O rótulo da caixa de ferramentas do QGIS não pode ter sumido no conserto do id."""
    titulo = _chamada_tr_constante(classe, "displayName")
    assert titulo, f"{classe.name}: displayName() deveria devolver self.tr('<título>')"
    # O prefixo numérico é o que ordena a lista no QGIS e casa com o P01..P16 do manual.
    assert re.match(r"^\d{2} - ", titulo), (
        f"{classe.name}: displayName() = {titulo!r}, esperava começar com 'NN - '"
    )


def test_ids_sao_unicos():
    nomes = [_retorno_constante(c, "name") for _, c in ALGORITMOS]
    duplicados = {n for n in nomes if nomes.count(n) > 1}
    assert not duplicados, f"id repetido no provider: {duplicados}"


def test_numeracao_do_manual_sem_repeticao():
    """Os números do displayName são os passos P01..P16 do manual de uso."""
    titulos = [_chamada_tr_constante(c, "displayName") for _, c in ALGORITMOS]
    numeros = sorted(int(t[:2]) for t in titulos)
    assert len(set(numeros)) == len(numeros), f"passo repetido: {numeros}"
    # O 05 e externo (PPP no site do IBGE, ou RTE noutro software): não é algoritmo.
    assert 5 not in numeros


def test_provider_tem_id_proprio():
    caminho = PLUGIN / "ponto_controle_provider.py"
    classes = list(_classes_de(caminho, "QgsProcessingProvider"))
    assert len(classes) == 1
    identificador = _retorno_constante(classes[0], "id")
    assert identificador == PROVIDER, (
        f"provider id = {identificador!r}. O id generico 'provider' colide com "
        "qualquer outro plugin que use o mesmo padrao de template."
    )


def test_provider_registra_todos_os_algoritmos():
    """addAlgorithm() esquecido e algoritmo que existe no fonte e some do QGIS."""
    caminho = PLUGIN / "ponto_controle_provider.py"
    arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    registradas = {
        no.args[0].func.id
        for no in ast.walk(arvore)
        if isinstance(no, ast.Call)
        and isinstance(no.func, ast.Attribute)
        and no.func.attr == "addAlgorithm"
        and no.args
        and isinstance(no.args[0], ast.Call)
        and isinstance(no.args[0].func, ast.Name)
    }
    no_fonte = {c.name for _, c in ALGORITMOS}
    assert no_fonte == registradas, (
        f"so no fonte: {no_fonte - registradas}; so no provider: {registradas - no_fonte}"
    )


# --------------------------------------------------------------------------
# Anotações curadas x ids reais
#
# Este e o alarme de renomeação: a prosa curada aponta ids, e um id que muda sem
# a anotação acompanhar deixaria o `describe` mudo, sem ninguém perceber.
# --------------------------------------------------------------------------
def test_anotacoes_apontam_algoritmos_que_existem():
    dados = json.loads(ANNOTATIONS.read_text(encoding="utf-8"))
    chaves = {k for k in dados if not k.startswith("_")}
    ids = {f"{PROVIDER}:{_retorno_constante(c, 'name')}" for _, c in ALGORITMOS}
    assert chaves - ids == set(), f"anotacao para id inexistente: {chaves - ids}"


def test_anotacoes_nao_repetem_o_que_o_describe_ja_le():
    """Regra do padrão agent-first: contrato copiado apodrece. A anotação só pode
    trazer o que a introspecao não alcanca (ordem do fluxo, armadilha), nunca a
    lista de parâmetros."""
    dados = json.loads(ANNOTATIONS.read_text(encoding="utf-8"))
    for chave, anotacao in dados.items():
        if chave.startswith("_"):
            continue
        assert "parameters" not in anotacao, f"{chave}: parametro nao entra na anotacao"
        assert set(anotacao) <= {"description", "constraints", "example"}, (
            f"{chave}: chave inesperada {set(anotacao) - {'description', 'constraints', 'example'}}"
        )
