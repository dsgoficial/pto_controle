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

# As quatro FASES do fluxo, na ordem, mais o balde da auxiliar. A ordem desta
# lista e o contrato: o numero do passo tem de crescer junto com a fase, senao a
# caixa de ferramentas promete uma sequencia que o fluxo nao tem.
FASES = ["preparacao", "processamento", "documentacao", "entrega"]
GRUPO_AUXILIAR = "auxiliares"
# O 05 nao existe (processamento externo: PPP no IBGE ou RTE noutro software).
PASSOS_ESPERADOS = {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12}


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
    Acervo) entrou, e voltaram a 15 em 2026-07-29, quando o P14 (verificar
    códigos disponíveis) saiu para o Controle do Acervo. Caíram a 12 em
    2026-07-30, com a poda do P11 (caminhos nos atributos), do P12 (download dos
    arquivos) e do P16 (compactar as pastas). Ao acrescentar ou remover
    algoritmo, ajuste este número de PROPOSITO."""
    assert len(ALGORITMOS) == 12, [c.name for _, c in ALGORITMOS]


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
    # O prefixo numérico é o que ordena a lista no QGIS e casa com o P01..P12 do
    # manual. Quem NAO tem número é a auxiliar, e a regra é essa: número é posto
    # no fluxo. A auxiliar não tem posto, e numerá-la mente sobre quando rodar.
    if _retorno_constante(classe, "groupId") == GRUPO_AUXILIAR:
        assert not re.match(r"^\d", titulo), (
            f"{classe.name}: e auxiliar e o rotulo {titulo!r} comeca com numero. "
            "Numero e posto no fluxo: quem esta fora do fluxo nao recebe."
        )
        return
    assert re.match(r"^\d{2} - ", titulo), (
        f"{classe.name}: displayName() = {titulo!r}, esperava começar com 'NN - '"
    )


def test_ids_sao_unicos():
    nomes = [_retorno_constante(c, "name") for _, c in ALGORITMOS]
    duplicados = {n for n in nomes if nomes.count(n) > 1}
    assert not duplicados, f"id repetido no provider: {duplicados}"


def _passos():
    """[(numero, groupId, classe)] dos algoritmos NUMERADOS, na ordem do rótulo."""
    passos = []
    for _, classe in ALGORITMOS:
        if _retorno_constante(classe, "groupId") == GRUPO_AUXILIAR:
            continue
        titulo = _chamada_tr_constante(classe, "displayName")
        passos.append((int(titulo[:2]), _retorno_constante(classe, "groupId"), classe))
    return sorted(passos)


def test_numeracao_do_manual_e_exatamente_a_esperada():
    """Os números do displayName são os passos P01..P12 do manual de uso.

    O teste cobra o CONJUNTO, e não só a unicidade. Depois da renumeração de
    2026-07-30 a sequência é contígua fora do 05, que é o passo externo (PPP no
    site do IBGE, ou RTE noutro software). Buraco novo aqui é sinal de algoritmo
    removido sem renumerar o resto, e o manual do doc_dgeo passaria a apontar
    passo que não existe. Ao mudar o fluxo de propósito, mude PASSOS_ESPERADOS
    junto, e o manual com ele."""
    numeros = {n for n, _, _ in _passos()}
    assert numeros == PASSOS_ESPERADOS, (
        f"passos {sorted(numeros)}, esperava {sorted(PASSOS_ESPERADOS)}"
    )


def test_o_numero_do_passo_cresce_junto_com_a_fase():
    """A fase e o número contam a MESMA história, ou um dos dois mente.

    Este é o alarme do desenho de 2026-07-30: a entrega (BPC e Controle do
    Acervo) é a ÚLTIMA fase, e a documentação do ponto vem antes dela. Um passo
    de entrega numerado no meio, ou um passo de documentação numerado depois da
    entrega, passa despercebido na caixa de ferramentas e leva quem opera a rodar
    na ordem errada. Foi exatamente o que aconteceu com o croqui digital, que era
    o 15 e rodava depois da monografia que o consome."""
    fases = [FASES.index(grupo) for _, grupo, _ in _passos()]
    assert fases == sorted(fases), (
        "a ordem dos números não acompanha a ordem das fases: "
        + str([(n, g) for n, g, _ in _passos()])
    )


def test_todo_algoritmo_esta_numa_fase_conhecida():
    for _, classe in ALGORITMOS:
        grupo = _retorno_constante(classe, "groupId")
        assert grupo in FASES + [GRUPO_AUXILIAR], (
            f"{classe.name}: groupId {grupo!r} nao e fase do fluxo nem auxiliar"
        )


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
