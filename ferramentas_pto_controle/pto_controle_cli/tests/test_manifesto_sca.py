# -*- coding: utf-8 -*-
"""
Prova que o manifesto do P17 é o que o Controle do Acervo (SCA) espera.

O manifesto é um CONTRATO entre dois repositórios que não se conhecem: o
`prepare-upload/missao` do SCA valida por Joi, e o que ele recusa aqui não custa
nada, enquanto o que ele recusa depois custa a transferência inteira da missão.

Roda sobre a AMOSTRA do repositório (`arquivos/depois_processamento`), e não
sobre uma pasta inventada: a estrutura de subpastas é justamente o que se está
traduzindo em tipo_arquivo_id, e uma pasta fabricada provaria só que o código
concorda consigo mesmo.

Não depende do QGIS: `manifesto.py` é python puro, de propósito. O que precisa
de QGIS é o algoritmo em volta dele, que é coberto pelo teste de integração.

Rodar:
    pytest ferramentas_pto_controle/pto_controle_cli/tests/test_manifesto_sca.py -v
"""
import hashlib
import importlib.util
import re
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
    """Espelha ponto_controle.tipo_arquivo. Mudou lá, tem de mudar aqui.

    O servidor RECUSA tipo que não existe, então o erro de código novo aparece.
    O erro caro é o código TROCADO: a foto de rastreio entraria como monografia,
    o `maximo_por_ponto` valeria sobre o tipo errado, e nada disso dá erro.
    """
    assert manifesto.FOTO_RASTREIO == 1
    assert manifesto.FOTO_AEREA == 2
    assert manifesto.CROQUI_MANUAL == 3
    assert manifesto.CROQUI_DIGITAL == 4
    assert manifesto.MONOGRAFIA == 5
    assert manifesto.RINEX == 6
    assert manifesto.BRUTO_COLETORA == 7
    assert manifesto.RELATORIO_PROCESSAMENTO == 8
    assert manifesto.FOTO_AUXILIAR == 9


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


# --- A tradução de pasta para tipo, sobre a amostra --------------------------

@pytest.fixture(scope="module")
def ponto():
    pasta = AMOSTRA / "SC-HV-69"
    if not pasta.is_dir():
        pytest.skip(f"amostra ausente: {pasta}")
    return pasta


def test_cada_subpasta_da_amostra_vira_o_tipo_certo(ponto):
    aceitos, ignorados = manifesto.arquivos_do_ponto(ponto)
    por_pasta = {}
    for caminho, tipo in aceitos:
        por_pasta.setdefault(caminho.relative_to(ponto).parts[0], set()).add(tipo)

    assert por_pasta["1_Formato_Nativo"] == {manifesto.BRUTO_COLETORA}
    assert por_pasta["2_RINEX"] == {manifesto.RINEX}
    assert por_pasta["3_Foto_Rastreio"] == {manifesto.FOTO_RASTREIO}
    assert por_pasta["6_Processamento"] == {manifesto.RELATORIO_PROCESSAMENTO}
    assert por_pasta["8_Monografia"] == {manifesto.MONOGRAFIA}

    # 7_Imagens_Monografia guarda dois tipos: a vista AEREA, que o BPC pede como
    # tal, e as vistas de município e estado, que são auxiliares.
    assert por_pasta["7_Imagens_Monografia"] == {
        manifesto.FOTO_AEREA, manifesto.FOTO_AUXILIAR
    }

    assert ignorados == [], f"arquivo fora da estrutura: {ignorados}"


def test_a_vista_aerea_nao_entra_como_auxiliar(ponto):
    aceitos, _ = manifesto.arquivos_do_ponto(ponto)
    tipos = {c.name: t for c, t in aceitos}
    assert tipos["SC-HV-69_AEREA.jpg"] == manifesto.FOTO_AEREA
    assert tipos["SC-HV-69_ESTADO.jpg"] == manifesto.FOTO_AUXILIAR
    assert tipos["SC-HV-69_MUNICIPIO.jpg"] == manifesto.FOTO_AUXILIAR


def test_o_croqui_digital_se_distingue_do_manual(tmp_path):
    """4_Croqui guarda os dois: o desenhado em campo e o que o P15 gera."""
    pasta = tmp_path / "SC-HV-69"
    (pasta / "4_Croqui").mkdir(parents=True)
    manual = pasta / "4_Croqui" / "SC-HV-69_CROQUI.jpeg"
    digital = pasta / "4_Croqui" / "SC-HV-69_CROQUI_DIGITAL.jpg"
    manual.write_bytes(b"a")
    digital.write_bytes(b"b")

    tipos = {c.name: t for c, t in manifesto.arquivos_do_ponto(pasta)[0]}
    assert tipos["SC-HV-69_CROQUI.jpeg"] == manifesto.CROQUI_MANUAL
    assert tipos["SC-HV-69_CROQUI_DIGITAL.jpg"] == manifesto.CROQUI_DIGITAL


def test_arquivo_fora_da_estrutura_e_relatado_e_nao_descartado(tmp_path):
    pasta = tmp_path / "SC-HV-69"
    (pasta / "2_RINEX").mkdir(parents=True)
    (pasta / "2_RINEX" / "SC-HV-69.22o").write_bytes(b"obs")
    (pasta / "anotacao.txt").write_bytes(b"deixado na raiz")
    (pasta / "9_Desconhecida").mkdir()
    (pasta / "9_Desconhecida" / "x.bin").write_bytes(b"?")

    aceitos, ignorados = manifesto.arquivos_do_ponto(pasta)
    assert len(aceitos) == 1
    assert sorted(c.name for c in ignorados) == ["anotacao.txt", "x.bin"]


def test_lixo_de_sistema_nao_conta_como_ignorado(tmp_path):
    pasta = tmp_path / "SC-HV-69"
    (pasta / "2_RINEX").mkdir(parents=True)
    (pasta / "2_RINEX" / "SC-HV-69.22o").write_bytes(b"obs")
    (pasta / "2_RINEX" / "Thumbs.db").write_bytes(b"lixo")
    (pasta / ".DS_Store").write_bytes(b"lixo")

    aceitos, ignorados = manifesto.arquivos_do_ponto(pasta)
    assert [c.name for c, _ in aceitos] == ["SC-HV-69.22o"]
    assert ignorados == []


# --- A entrada de arquivo, campo a campo -------------------------------------

def test_o_checksum_e_o_sha256_do_arquivo_que_vai_viajar(tmp_path):
    """O servidor recalcula este mesmo SHA-256 no volume. Divergir aqui faria a
    importação inteira ser recusada, e o motivo não estaria neste repositório."""
    arquivo = tmp_path / "SC-HV-69.22o"
    conteudo = b"RINEX 3.04 OBSERVATION DATA\n" * 1000
    arquivo.write_bytes(conteudo)

    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.RINEX)
    assert entrada["checksum"] == hashlib.sha256(conteudo).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", entrada["checksum"])


def test_o_nome_e_a_extensao_saem_separados(tmp_path):
    """O SCA remonta o caminho como <nome_arquivo>.<extensao>. Nome com ponto no
    meio (SC-HV-69.22o.pdf) é o caso que quebra a divisão ingênua."""
    arquivo = tmp_path / "SC-HV-69.22o.pdf"
    arquivo.write_bytes(b"pdf")

    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.RELATORIO_PROCESSAMENTO)
    assert entrada["nome_arquivo"] == "SC-HV-69.22o"
    assert entrada["extensao"] == "pdf"
    assert f"{entrada['nome_arquivo']}.{entrada['extensao']}" == arquivo.name


def test_a_extensao_sai_em_minuscula(tmp_path):
    arquivo = tmp_path / "SC-HV-69.JPG"
    arquivo.write_bytes(b"jpg")
    assert manifesto.entrada_de_arquivo(arquivo, 1)["extensao"] == "jpg"


def test_a_entrada_tem_exatamente_os_campos_do_schema_do_sca(tmp_path):
    """models.arquivo em ponto_controle_schema.js.

    `volume_armazenamento_id` NÃO entra: quem escolhe o volume é o servidor, pelo
    volume primário do tipo de produto 10. Mandá-lo daqui seria tentar escrever
    onde se quer, e o stripUnknown do SCA o descartaria em silêncio.
    """
    arquivo = tmp_path / "x.jpg"
    arquivo.write_bytes(b"j")
    entrada = manifesto.entrada_de_arquivo(arquivo, manifesto.FOTO_RASTREIO)

    assert set(entrada) == {
        "tipo_arquivo_id", "nome_arquivo", "extensao", "tamanho_mb", "checksum"
    }


def test_a_amostra_respeita_o_maximo_por_ponto_do_sca(ponto):
    """maximo_por_ponto em ponto_controle.tipo_arquivo. O prepare-upload recusa
    a missão inteira quando estoura, então vale conferir contra a amostra."""
    maximos = {
        manifesto.FOTO_RASTREIO: 4,
        manifesto.FOTO_AEREA: 1,
        manifesto.CROQUI_MANUAL: 1,
        manifesto.CROQUI_DIGITAL: 1,
        manifesto.MONOGRAFIA: 1,
    }
    aceitos, _ = manifesto.arquivos_do_ponto(ponto)
    contagem = {}
    for _, tipo in aceitos:
        contagem[tipo] = contagem.get(tipo, 0) + 1

    for tipo, maximo in maximos.items():
        assert contagem.get(tipo, 0) <= maximo, (
            f"tipo {tipo}: {contagem[tipo]} arquivos, máximo {maximo}"
        )
