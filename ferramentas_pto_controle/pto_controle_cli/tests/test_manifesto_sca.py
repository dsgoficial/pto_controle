# -*- coding: utf-8 -*-
"""
Prova que o manifesto do P17 é o que o Controle do Acervo (SCA) espera.

O manifesto é um CONTRATO entre dois repositórios que não se conhecem: o
`prepare-upload/missao` do SCA valida por Joi, e o que ele recusa aqui não custa
nada, enquanto o que ele recusa depois custa a transferência inteira da missão.

Cada ponto vai em DOIS arquivos, o pacote e a monografia (chefe, 2026-07-29; SCA
a partir da 1.7.0). O que este teste guarda é isso: que o pacote leva a pasta
inteira menos a monografia, que a estrutura de subpastas atravessa dentro do zip,
e que os dois códigos de tipo são os do domínio do SCA.

Roda sobre a AMOSTRA do repositório (`arquivos/depois_processamento`), e não
sobre uma pasta inventada: é a estrutura de verdade que se está empacotando.

Não depende do QGIS: `manifesto.py` é python puro, de propósito. O que precisa
de QGIS é o algoritmo em volta dele.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_manifesto_sca.py -v
"""
import hashlib
import importlib.util
import re
import zipfile
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[3]
AMOSTRA = RAIZ / "arquivos" / "depois_processamento" / "eliomar_2022-07-03"


def carrega(nome, caminho):
    """Importa o módulo pelo caminho, sem passar pelo pacote do plugin.

    O `ferramentas_pto_controle/__init__.py` importa o QGIS, que não existe no
    python da suíte. Carregar o arquivo direto é o que mantém este teste rodando
    em qualquer máquina.
    """
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


manifesto = carrega(
    "manifesto",
    RAIZ / "ferramentas_pto_controle" / "prepareToSCA" / "manifesto.py",
)


# --- Os códigos, contra o er/ponto_controle.sql do SCA -----------------------

def test_os_codigos_de_tipo_sao_os_do_sca():
    """Espelha ponto_controle.tipo_arquivo, que tem SÓ estes dois desde a 1.7.0.

    O servidor recusa tipo que não existe, então código novo aparece. O erro caro
    é o código TROCADO: a monografia entraria como pacote, e nada disso dá erro.
    """
    assert manifesto.PACOTE == 1
    assert manifesto.MONOGRAFIA == 2


def test_o_padrao_de_codigo_e_o_mesmo_do_joi_do_sca():
    # server/src/ponto_controle/ponto_controle_schema.js
    assert manifesto.RE_COD_PONTO_SCA.pattern == r"^[A-Z]{2}-(HV|BASE)-[1-9][0-9]{0,3}$"


@pytest.mark.parametrize("codigo", ["SC-HV-69", "RS-HV-207", "SP-BASE-1", "MG-HV-9999"])
def test_codigo_valido_passa(codigo):
    assert manifesto.cod_ponto_invalido(codigo) is None


@pytest.mark.parametrize("codigo", [
    "sc-hv-69",       # minúscula
    "SC-Base-7",      # BASE em maiúscula é o que o SCA aceita
    "SC-HV-0",        # sem zero à esquerda
    "SC-HV-07",
    "SC-HV-12345",    # até quatro dígitos
    "SCHV69",
    "",
    None,
])
def test_codigo_que_o_sca_recusa_para_aqui(codigo):
    """Recusar na geração custa segundos; recusar na importação custa 300 MB."""
    assert manifesto.cod_ponto_invalido(codigo) is not None


# --- O pacote, sobre a amostra -----------------------------------------------

@pytest.fixture(scope="module")
def ponto():
    pasta = AMOSTRA / "SC-HV-69"
    if not pasta.is_dir():
        pytest.skip(f"amostra ausente: {pasta}")
    return pasta


def test_o_pacote_leva_a_pasta_inteira_menos_a_monografia(ponto, tmp_path):
    alvo = tmp_path / "SC-HV-69_pacote.zip"
    incluidos, lixo = manifesto.monta_pacote(ponto, alvo)

    na_pasta = {
        p.relative_to(ponto).as_posix()
        for p in ponto.rglob("*") if p.is_file() and p.name not in manifesto.LIXO
    }
    da_monografia = {n for n in na_pasta if n.startswith("8_Monografia/")}
    assert da_monografia, "a amostra precisa ter monografia para este teste valer"

    with zipfile.ZipFile(alvo) as z:
        no_zip = set(z.namelist())

    assert no_zip == na_pasta - da_monografia
    assert len(incluidos) == len(no_zip)
    assert lixo == []


def test_a_estrutura_de_subpastas_atravessa_dentro_do_zip(ponto, tmp_path):
    """É isto que dispensa renomear arquivo para caber num nome só por ponto."""
    alvo = tmp_path / "p.zip"
    manifesto.monta_pacote(ponto, alvo)
    with zipfile.ZipFile(alvo) as z:
        nomes = z.namelist()

    assert any(n.startswith("2_RINEX/") for n in nomes)
    assert any(n.startswith("3_Foto_Rastreio/") for n in nomes)
    assert all("/" in n for n in nomes), "arquivo achatado dentro do zip"


def test_dois_arquivos_de_mesmo_nome_em_subpastas_convivem_no_pacote(tmp_path):
    """O caso que antes fazia o P17 parar: <cod>.pdf no processamento e na
    monografia. Com o caminho relativo dentro do zip eles não colidem."""
    pasta = tmp_path / "SC-HV-69"
    (pasta / "6_Processamento").mkdir(parents=True)
    (pasta / "2_RINEX").mkdir(parents=True)
    (pasta / "6_Processamento" / "SC-HV-69.pdf").write_bytes(b"relatorio")
    (pasta / "2_RINEX" / "SC-HV-69.pdf").write_bytes(b"outro")

    alvo = tmp_path / "p.zip"
    incluidos, _ = manifesto.monta_pacote(pasta, alvo)
    with zipfile.ZipFile(alvo) as z:
        assert sorted(z.namelist()) == [
            "2_RINEX/SC-HV-69.pdf", "6_Processamento/SC-HV-69.pdf"
        ]
        assert z.read("6_Processamento/SC-HV-69.pdf") == b"relatorio"
    assert len(incluidos) == 2


def test_arquivo_fora_da_estrutura_entra_no_pacote(tmp_path):
    """No modelo de dois arquivos nada fica de fora por estar fora da estrutura:
    o pacote é a pasta como ela é."""
    pasta = tmp_path / "SC-HV-69"
    (pasta / "2_RINEX").mkdir(parents=True)
    (pasta / "2_RINEX" / "SC-HV-69.22o").write_bytes(b"obs")
    (pasta / "anotacao.txt").write_bytes(b"deixado na raiz")
    (pasta / "9_Desconhecida").mkdir()
    (pasta / "9_Desconhecida" / "x.bin").write_bytes(b"?")

    alvo = tmp_path / "p.zip"
    incluidos, lixo = manifesto.monta_pacote(pasta, alvo)
    with zipfile.ZipFile(alvo) as z:
        assert sorted(z.namelist()) == [
            "2_RINEX/SC-HV-69.22o", "9_Desconhecida/x.bin", "anotacao.txt"
        ]
    assert len(incluidos) == 3
    assert lixo == []


def test_lixo_de_sistema_fica_de_fora_do_pacote(tmp_path):
    pasta = tmp_path / "SC-HV-69"
    (pasta / "2_RINEX").mkdir(parents=True)
    (pasta / "2_RINEX" / "SC-HV-69.22o").write_bytes(b"obs")
    (pasta / "2_RINEX" / "Thumbs.db").write_bytes(b"lixo")
    (pasta / ".DS_Store").write_bytes(b"lixo")

    alvo = tmp_path / "p.zip"
    incluidos, lixo = manifesto.monta_pacote(pasta, alvo)
    with zipfile.ZipFile(alvo) as z:
        assert z.namelist() == ["2_RINEX/SC-HV-69.22o"]
    assert len(incluidos) == 1
    assert sorted(c.name for c in lixo) == [".DS_Store", "Thumbs.db"]


# --- A monografia -------------------------------------------------------------

def test_a_monografia_da_amostra_e_achada(ponto):
    achada = manifesto.acha_monografia(ponto)
    assert achada is not None
    assert achada.suffix.lower() == ".pdf"
    assert achada.parent.name == manifesto.PASTA_MONOGRAFIA


def test_ponto_sem_monografia_devolve_none(tmp_path):
    pasta = tmp_path / "SC-HV-69"
    (pasta / "2_RINEX").mkdir(parents=True)
    assert manifesto.acha_monografia(pasta) is None

    (pasta / manifesto.PASTA_MONOGRAFIA).mkdir()
    assert manifesto.acha_monografia(pasta) is None


def test_duas_monografias_param_o_passo(tmp_path):
    """Escolher uma delas calado seria decidir no lugar de quem mediu."""
    pasta = tmp_path / "SC-HV-69"
    (pasta / manifesto.PASTA_MONOGRAFIA).mkdir(parents=True)
    (pasta / manifesto.PASTA_MONOGRAFIA / "SC-HV-69.pdf").write_bytes(b"a")
    (pasta / manifesto.PASTA_MONOGRAFIA / "SC-HV-69_v2.pdf").write_bytes(b"b")

    with pytest.raises(ValueError, match="2 PDFs"):
        manifesto.acha_monografia(pasta)


# --- A entrada de arquivo, campo a campo -------------------------------------

def test_o_checksum_e_o_sha256_do_arquivo_que_vai_viajar(tmp_path):
    """O servidor recalcula este mesmo SHA-256 no volume. Divergir aqui faria a
    importação inteira ser recusada, e o motivo não estaria neste repositório."""
    arquivo = tmp_path / "SC-HV-69_pacote.zip"
    conteudo = b"PK\x03\x04" + b"conteudo do pacote\n" * 1000
    arquivo.write_bytes(conteudo)

    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.PACOTE)
    assert entrada["checksum"] == hashlib.sha256(conteudo).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", entrada["checksum"])


def test_o_nome_e_a_extensao_saem_separados(tmp_path):
    """O SCA remonta o caminho como <nome_arquivo>.<extensao>."""
    arquivo = tmp_path / "SC-HV-69_pacote.zip"
    arquivo.write_bytes(b"zip")

    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.PACOTE)
    assert entrada["nome_arquivo"] == "SC-HV-69_pacote"
    assert entrada["extensao"] == "zip"
    assert f"{entrada['nome_arquivo']}.{entrada['extensao']}" == arquivo.name


def test_a_extensao_sai_em_minuscula(tmp_path):
    arquivo = tmp_path / "SC-HV-69.PDF"
    arquivo.write_bytes(b"pdf")
    assert manifesto.entrada_de_arquivo(arquivo, manifesto.MONOGRAFIA)["extensao"] == "pdf"


def test_a_entrada_tem_exatamente_os_campos_do_schema_do_sca(tmp_path):
    """models.arquivo em ponto_controle_schema.js.

    `volume_armazenamento_id` NÃO entra: quem escolhe o volume é o servidor, pelo
    volume primário do tipo de produto 10. Mandá-lo daqui seria tentar escrever
    onde se quer, e o stripUnknown do SCA o descartaria em silêncio.
    """
    arquivo = tmp_path / "x.zip"
    arquivo.write_bytes(b"j")
    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.PACOTE)

    assert set(entrada) == {
        "tipo_arquivo_id", "nome_arquivo", "extensao", "tamanho_mb", "checksum"
    }


def test_o_ponto_gera_no_maximo_um_arquivo_de_cada_tipo(ponto, tmp_path):
    """maximo_por_ponto = 1 nos dois tipos. Aqui isso deixa de ser teto e passa a
    ser a forma do pacote: um zip e uma monografia, nunca mais."""
    alvo = tmp_path / "SC-HV-69_pacote.zip"
    manifesto.monta_pacote(ponto, alvo)
    monografia = manifesto.acha_monografia(ponto)

    entradas = [manifesto.entrada_de_arquivo(alvo, manifesto.PACOTE)]
    if monografia is not None:
        entradas.append(
            manifesto.entrada_de_arquivo(monografia, manifesto.MONOGRAFIA))

    contagem = {}
    for e in entradas:
        contagem[e["tipo_arquivo_id"]] = contagem.get(e["tipo_arquivo_id"], 0) + 1
    assert all(n == 1 for n in contagem.values())
    assert set(contagem) <= {manifesto.PACOTE, manifesto.MONOGRAFIA}
