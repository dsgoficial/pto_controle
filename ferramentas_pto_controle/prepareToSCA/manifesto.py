# -*- coding: utf-8 -*-
"""Monta o manifesto da missão: o corpo que o Controle do Acervo (SCA) espera.

O SCA importa em DUAS FASES, como faz com o resto do acervo:

1. `POST /api/ponto_controle/prepare-upload/missao` recebe este manifesto,
   confere tudo e devolve, por arquivo, PARA ONDE copiá-lo;
2. quem importa transfere os arquivos ao volume;
3. `POST /api/ponto_controle/confirm-upload` faz o servidor RELER cada arquivo,
   recalcular o SHA-256 e só então gravar.

Daí duas decisões deste módulo:

- **O checksum é calculado aqui, sobre o arquivo que vai viajar.** Ele não é
  prova (o servidor recalcula no destino); é o que permite ao servidor detectar
  a transferência que corrompeu.
- **O arquivo vai INDIVIDUAL, e não num zip por ponto.** O SCA registra arquivo
  a arquivo, com tipo próprio e limite por ponto (`maximo_por_ponto`). Um zip
  chegaria como um arquivo só, de tipo nenhum, e o acervo perderia justamente o
  que a estrutura de pastas carrega hoje.

A pasta de origem some no caminho, e é de propósito: o que `3_Foto_Rastreio` e
`7_Imagens_Monografia` significam vira `tipo_arquivo_id` no manifesto. É para
isso que o domínio existe do outro lado.
"""
import hashlib
import re

# Códigos de ponto_controle.tipo_arquivo, no er/ponto_controle.sql do SCA.
# Mudou lá, muda aqui: o servidor RECUSA tipo que não existe, o que é melhor do
# que gravar com o tipo errado.
FOTO_RASTREIO = 1
FOTO_AEREA = 2
CROQUI_MANUAL = 3
CROQUI_DIGITAL = 4
MONOGRAFIA = 5
RINEX = 6
BRUTO_COLETORA = 7
RELATORIO_PROCESSAMENTO = 8
FOTO_AUXILIAR = 9

# A subpasta diz o tipo. Onde uma pasta guarda mais de um tipo, o nome do
# arquivo desempata (ver `tipo_do_arquivo`).
TIPO_POR_PASTA = {
    "1_Formato_Nativo": BRUTO_COLETORA,
    "2_RINEX": RINEX,
    "3_Foto_Rastreio": FOTO_RASTREIO,
    "4_Croqui": CROQUI_MANUAL,
    "5_Croqui": CROQUI_MANUAL,
    "6_Processamento": RELATORIO_PROCESSAMENTO,
    "7_Imagens_Monografia": FOTO_AUXILIAR,
    "8_Monografia": MONOGRAFIA,
}

# O SCA valida o código com este padrão. Conferir AQUI, na geração, é o que
# evita descobrir um `SC-Base-07` no fim de uma transferência de 300 MB.
RE_COD_PONTO_SCA = re.compile(r"^[A-Z]{2}-(HV|BASE)-[1-9][0-9]{0,3}$")

LIXO = {".DS_Store", "Thumbs.db", "desktop.ini"}


def tipo_do_arquivo(caminho, raiz_ponto):
    """Código de tipo_arquivo para um arquivo dentro da pasta de um ponto.

    Devolve None para arquivo que não está em nenhuma subpasta conhecida. Quem
    chama RELATA esses, em vez de descartá-los calado: arquivo solto na raiz do
    ponto costuma ser coisa que o medidor deixou para trás, e ninguém quer
    descobrir isso depois da importação.
    """
    relativo = caminho.relative_to(raiz_ponto)
    if len(relativo.parts) < 2:
        return None

    pasta = relativo.parts[0]
    tipo = TIPO_POR_PASTA.get(pasta)
    if tipo is None:
        return None

    nome = caminho.stem.upper()

    # 4_Croqui guarda os dois: o desenhado em campo e o que o P15 gera por
    # atlas, com o sufixo _CROQUI_DIGITAL.
    if tipo == CROQUI_MANUAL and "CROQUI_DIGITAL" in nome:
        return CROQUI_DIGITAL

    # 7_Imagens_Monografia guarda a vista aérea do ponto (que o BPC pede como
    # tal) ao lado das vistas de município e estado, que são auxiliares.
    if tipo == FOTO_AUXILIAR and nome.endswith("_AEREA"):
        return FOTO_AEREA

    return tipo


def sha256_de(caminho, bloco=1024 * 1024):
    """SHA-256 e tamanho em MB, lendo por bloco.

    Por bloco, e não `read()`: um RINEX de rastreio longo passa de centenas de
    MB, e o QGIS roda no mesmo processo da interface.
    """
    h = hashlib.sha256()
    total = 0
    with open(caminho, "rb") as f:
        for pedaco in iter(lambda: f.read(bloco), b""):
            h.update(pedaco)
            total += len(pedaco)
    return h.hexdigest(), total / (1024 * 1024)


def arquivos_do_ponto(raiz_ponto):
    """Lista (caminho, tipo) dos arquivos de um ponto, e os que ficaram de fora.

    Devolve (aceitos, ignorados). Nada some em silêncio.
    """
    aceitos = []
    ignorados = []
    for caminho in sorted(raiz_ponto.rglob("*")):
        if not caminho.is_file():
            continue
        if caminho.name in LIXO or "__MACOSX" in caminho.parts:
            continue
        tipo = tipo_do_arquivo(caminho, raiz_ponto)
        if tipo is None:
            ignorados.append(caminho)
            continue
        aceitos.append((caminho, tipo))
    return aceitos, ignorados


def entrada_de_arquivo(caminho, tipo):
    """Um item de `arquivos` no manifesto, como o schema do SCA o espera."""
    checksum, tamanho_mb = sha256_de(caminho)
    return {
        "tipo_arquivo_id": tipo,
        # O SCA remonta o caminho como <nome_arquivo>.<extensao>, então os dois
        # saem separados. `SC-HV-69.22o.pdf` vira nome 'SC-HV-69.22o' e 'pdf'.
        "nome_arquivo": caminho.stem,
        "extensao": caminho.suffix.lstrip(".").lower() or None,
        "tamanho_mb": round(tamanho_mb, 6),
        "checksum": checksum,
    }


def cod_ponto_invalido(cod_ponto):
    """Mensagem de recusa, ou None se o código serve ao SCA."""
    if not cod_ponto:
        return "ponto sem cod_ponto no GeoPackage"
    if not RE_COD_PONTO_SCA.match(cod_ponto):
        return (
            f"{cod_ponto}: o Controle do Acervo aceita UF-HV-N ou UF-BASE-N, "
            "com a UF e BASE em maiúsculas e sem zero à esquerda"
        )
    return None
