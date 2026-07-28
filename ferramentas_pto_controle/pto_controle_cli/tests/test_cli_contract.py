# -*- coding: utf-8 -*-
"""
Testes das camadas que ficam ENTRE o chamador e o qgis_process: validacao local
dos parametros, cache do contrato em disco, tratamento de segredo e formatacao do
`describe`.

Nenhum destes precisa de QGIS: o contrato entra como fixture, no formato que o
`qgis_process help --json` devolve. E de proposito, porque a validacao existe para
poupar a chamada cara, entao testa-la nao pode custar essa chamada.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_cli_contract.py -v
"""
import importlib.util
import json
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
CLI_PY = CLI_DIR / "pto_controle_cli.py"

_spec = importlib.util.spec_from_file_location("pto_controle_cli_under_test", CLI_PY)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)


# --------------------------------------------------------------------------
# Contrato de exemplo (formato real do `help --json`)
# --------------------------------------------------------------------------
def _param(ptype, optional=False, **extra):
    param = {
        "description": extra.pop("description", ""),
        "optional": optional,
        "is_advanced": extra.pop("is_advanced", False),
        "is_destination": extra.pop("is_destination", False),
        "default_value": extra.pop("default_value", None),
        "raw_definition": {"parameter_type": ptype, **extra.pop("raw_definition", {})},
    }
    param.update(extra)
    return param


HELP = {
    "algorithm_details": {
        "id": "ptocontrole:criarbanco",
        "name": "01 - Criar banco de dados",
        "group": "Pre-processamento",
    },
    "parameters": {
        "SERVERIP": _param("string", description="Insira o IP do computador"),
        "PORT": _param("number", description="Insira a porta", default_value=5432),
        "BDNAME": _param("string", description="Insira o nome do banco"),
        "USER": _param("string", description="Insira o usuario do PostgreSQL"),
        "PASSWORD": _param("string", description="Insira a senha do PostgreSQL"),
    },
    "outputs": {},
}

HELP_ENUM = {
    "algorithm_details": {"id": "ptocontrole:distribuirmonografia", "name": "09", "group": "g"},
    "parameters": {
        "PASTA_ESTRUTURA": _param("file", description="Pasta com estrutura"),
        "TIPO_MODELO": _param(
            "enum",
            description="Orientacao da pagina",
            default_value=1,
            available_options={"0": "Paisagem", "1": "Retrato"},
        ),
    },
    "outputs": {},
}


# --------------------------------------------------------------------------
# Normalizacao de id
# --------------------------------------------------------------------------
def test_full_id_acrescenta_o_provider():
    assert cli.full_id("criarbanco") == "ptocontrole:criarbanco"


def test_full_id_respeita_id_ja_completo():
    assert cli.full_id("ptocontrole:criarbanco") == "ptocontrole:criarbanco"
    # Outro provider precisa passar intacto: o CLI nao e dono do namespace.
    assert cli.full_id("native:buffer") == "native:buffer"


def test_version_key_ordena_por_numero_e_nao_por_texto():
    caminhos = [r"C:\QGIS 3.8\bin\x", r"C:\QGIS 3.40.0\bin\x", r"C:\QGIS 4.0.0\bin\x"]
    assert sorted(caminhos, key=cli._version_key)[-1] == r"C:\QGIS 4.0.0\bin\x"


# --------------------------------------------------------------------------
# Coercao de KEY=VALUE
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("5432", 5432),
        ("0", 0),
        ("-3", -3),
        ("0.11", 0.11),
        # Os que NAO podem virar numero, sob pena de corromper o valor:
        ("007", "007"),
        ("1_000", "1_000"),
        ("inf", "inf"),
        ("nan", "nan"),
        ("1e3", "1e3"),
        ("EPSG:31982", "EPSG:31982"),
        ("SP-HV-0042", "SP-HV-0042"),
    ],
)
def test_coerce(entrada, esperado):
    assert cli._coerce(entrada) == esperado


def test_unwrap_inputs_aceita_as_duas_formas():
    assert cli._unwrap_inputs({"inputs": {"A": 1}}) == {"A": 1}
    assert cli._unwrap_inputs({"A": 1}) == {"A": 1}


def test_unwrap_inputs_recusa_lista():
    with pytest.raises(SystemExit):
        cli._unwrap_inputs([1, 2])


def test_parse_json_stdout_devolve_none_em_lixo():
    assert cli._parse_json_stdout("") is None
    assert cli._parse_json_stdout("nao e json") is None
    assert cli._parse_json_stdout('{"a": 1}') == {"a": 1}


# --------------------------------------------------------------------------
# Validacao local
# --------------------------------------------------------------------------
def test_validacao_aprova_corpo_completo():
    inputs = {"SERVERIP": "localhost", "PORT": 5432, "BDNAME": "bpc",
              "USER": "postgres", "PASSWORD": "x"}
    assert cli.validate_inputs(inputs, HELP) == []


def test_validacao_pega_obrigatorio_ausente():
    erros = cli.validate_inputs({"SERVERIP": "localhost"}, HELP)
    faltando = {e["params"][0] for e in erros}
    assert {"BDNAME", "USER", "PASSWORD"} <= faltando


def test_validacao_pega_nome_inexistente_e_sugere():
    """O modo de falha mais caro: o qgis_process IGNORA a chave desconhecida em
    silencio e aplica o padrao. A validacao existe para pegar isso antes."""
    erros = cli.validate_inputs({"SERVER_IP": "localhost"}, HELP)
    mensagens = [e["message"] for e in erros]
    assert any("parametro inexistente: SERVER_IP" in m for m in mensagens)
    assert any("SERVERIP" in m for m in mensagens)


def test_validacao_pega_enum_fora_da_faixa():
    erros = cli.validate_inputs({"PASTA_ESTRUTURA": "/x", "TIPO_MODELO": 7}, HELP_ENUM)
    assert any("fora da faixa" in e["message"] for e in erros)


def test_validacao_pega_rotulo_no_lugar_do_indice():
    erros = cli.validate_inputs({"PASTA_ESTRUTURA": "/x", "TIPO_MODELO": "Retrato"}, HELP_ENUM)
    mensagens = " ".join(e["message"] for e in erros)
    assert "nao e indice" in mensagens
    # A mensagem tem de dizer QUAL e o indice, senao obriga uma segunda consulta.
    assert "1" in mensagens


def test_mensagem_de_erro_traz_o_contrato_do_parametro_citado():
    erros = cli.validate_inputs({"SERVER_IP": "x"}, HELP)
    texto = cli.format_validation_errors("ptocontrole:criarbanco", erros, HELP)
    assert "SERVERIP" in texto
    assert "describe" in texto


@pytest.mark.parametrize(
    "valor,esperado",
    [(1, [1]), ("1", [1]), ("1,3", [1, 3]), ([1, 3], [1, 3]),
     ("Retrato", None), (True, None)],
)
def test_enum_indices(valor, esperado):
    assert cli._enum_indices(valor) == esperado


# --------------------------------------------------------------------------
# Coercao por tipo do contrato
#
# Achado em 2026-07-28, no primeiro dry-run contra o plugin real: `IGN_PROC=false`
# virava a string 'false', que e nao-vazia e portanto verdadeira. O parametro faria
# o OPOSTO do pedido, sem erro nenhum.
# --------------------------------------------------------------------------
HELP_BOOL = {
    "algorithm_details": {"id": "ptocontrole:validarestrutura", "name": "02", "group": "g"},
    "parameters": {
        "FOLDER": _param("file", description="Pasta"),
        "IGN_PROC": _param("boolean", description="Ignorar processamento?", default_value=False),
    },
    "outputs": {},
}


@pytest.mark.parametrize("texto", ["false", "False", "FALSE", "0", "nao", "no", "n"])
def test_string_falsa_vira_booleano_falso(texto):
    inputs = {"FOLDER": "/x", "IGN_PROC": texto}
    assert cli.coagir_por_contrato(inputs, HELP_BOOL) == []
    assert inputs["IGN_PROC"] is False


@pytest.mark.parametrize("texto", ["true", "True", "1", "sim", "yes", "y"])
def test_string_verdadeira_vira_booleano_verdadeiro(texto):
    inputs = {"FOLDER": "/x", "IGN_PROC": texto}
    assert cli.coagir_por_contrato(inputs, HELP_BOOL) == []
    assert inputs["IGN_PROC"] is True


def test_booleano_ilegivel_e_erro_e_nao_chute():
    inputs = {"FOLDER": "/x", "IGN_PROC": "talvez"}
    erros = cli.coagir_por_contrato(inputs, HELP_BOOL)
    assert any("nao e booleano" in e["message"] for e in erros)
    # Nao pode ter chutado um valor: melhor reprovar do que enviar o oposto.
    assert inputs["IGN_PROC"] == "talvez"


def test_coercao_nao_toca_o_que_nao_e_booleano():
    inputs = {"FOLDER": "false", "IGN_PROC": True}
    assert cli.coagir_por_contrato(inputs, HELP_BOOL) == []
    assert inputs["FOLDER"] == "false"  # caminho chamado 'false' continua string
    assert inputs["IGN_PROC"] is True   # ja era booleano, veio de --params


# --------------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------------
def test_cache_ida_e_volta(tmp_path, monkeypatch):
    monkeypatch.setenv("PTOCONTROLE_CLI_CACHE", str(tmp_path))
    cli.cache_write("ptocontrole:criarbanco", HELP)
    assert cli.cache_read("ptocontrole:criarbanco") == HELP


def test_cache_invalida_quando_a_impressao_digital_muda(tmp_path, monkeypatch):
    monkeypatch.setenv("PTOCONTROLE_CLI_CACHE", str(tmp_path))
    cli.cache_write("ptocontrole:criarbanco", HELP)
    monkeypatch.setattr(cli, "_fingerprint", "outra-coisa")
    assert cli.cache_read("ptocontrole:criarbanco") is None


def test_cache_nao_derruba_o_comando_quando_a_escrita_falha(tmp_path, monkeypatch):
    """O cache e otimizacao. Um destino que nao da para escrever nao pode impedir
    de rodar o algoritmo. Aqui o destino e uma pasta DENTRO de um arquivo, que faz
    o mkdir falhar do jeito que um /tmp somente-leitura falharia."""
    arquivo = tmp_path / "isto_e_um_arquivo"
    arquivo.write_text("x", encoding="utf-8")
    monkeypatch.setenv("PTOCONTROLE_CLI_CACHE", str(arquivo / "cache"))
    cli.cache_write("ptocontrole:criarbanco", HELP)  # nao levanta
    assert cli.cache_read("ptocontrole:criarbanco") is None


# --------------------------------------------------------------------------
# Renderizacao
# --------------------------------------------------------------------------
def test_describe_mostra_o_mapa_do_enum():
    saida = cli.render_describe(HELP_ENUM, {})
    assert "0=Paisagem" in saida
    assert "1=Retrato" in saida


def test_describe_com_anotacao_curada():
    anotacao = {"description": "P01. Cria o banco.", "constraints": ["Nao sobrescreve."]}
    saida = cli.render_describe(HELP, anotacao)
    assert "P01. Cria o banco." in saida
    assert "Nao sobrescreve." in saida


def test_dry_run_traduz_o_indice_do_enum_para_rotulo():
    saida = cli.render_dry_run(
        "ptocontrole:distribuirmonografia",
        {"PASTA_ESTRUTURA": "/x", "TIPO_MODELO": 1},
        HELP_ENUM,
    )
    assert "Retrato" in saida
