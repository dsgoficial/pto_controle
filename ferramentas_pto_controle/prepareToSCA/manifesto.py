# -*- coding: utf-8 -*-
"""Monta o manifesto da missão: o corpo que o Controle do Acervo (SCA) espera.

O SCA importa em DUAS FASES, como faz com o resto do acervo:

1. `POST /api/ponto_controle/prepare-upload/missao` recebe este manifesto,
   confere tudo e devolve, por arquivo, PARA ONDE copiá-lo;
2. quem importa transfere os arquivos ao volume;
3. `POST /api/ponto_controle/confirm-upload` faz o servidor RELER cada arquivo,
   recalcular o SHA-256 e só então gravar.

**Cada ponto vai em DOIS arquivos, e não um por arquivo** (decisão do chefe em
2026-07-29, refletida no SCA a partir da versão 1.7.0):

- o **pacote**, um zip com tudo o que só se lê junto (rastreio, RINEX, fotos,
  croqui, processamento, imagens da monografia);
- a **monografia**, o PDF que alguém procura sozinho.

São também os dois únicos downloads que a tela do acervo oferece. Por isso o
domínio `ponto_controle.tipo_arquivo` tem só estes dois códigos.

O zip guarda o caminho RELATIVO de cada arquivo, então a estrutura de pastas
sobrevive dentro dele. Duas consequências práticas: nada precisa ser renomeado
para caber num nome só por ponto, e arquivo fora da estrutura conhecida entra
junto em vez de ficar de fora.

O checksum é calculado aqui, sobre o arquivo que vai viajar. Ele não é prova (o
servidor recalcula no destino); é o que permite ao servidor detectar a
transferência que corrompeu.
"""
import hashlib
import re
import zipfile

# Códigos de ponto_controle.tipo_arquivo, no er/ponto_controle.sql do SCA.
# Mudou lá, muda aqui: o servidor RECUSA tipo que não existe, o que é melhor do
# que gravar com o tipo errado.
PACOTE = 1
MONOGRAFIA = 2

# A monografia sai do pacote e viaja sozinha. É a única subpasta com tratamento
# próprio; todo o resto entra no zip como está.
PASTA_MONOGRAFIA = "8_Monografia"

# O SCA valida o código com este padrão. Conferir AQUI, na geração, é o que
# evita descobrir um `SC-Base-07` no fim de uma transferência de 300 MB.
RE_COD_PONTO_SCA = re.compile(r"^[A-Z]{2}-(HV|BASE)-[1-9][0-9]{0,3}$")

LIXO = {".DS_Store", "Thumbs.db", "desktop.ini"}


def eh_lixo(caminho, relativo):
    return caminho.name in LIXO or "__MACOSX" in relativo.parts


def monta_pacote(raiz_ponto, destino_zip):
    """Zipa a pasta do ponto INTEIRA, menos a monografia.

    Devolve (incluidos, lixo). O caminho dentro do zip é o relativo à pasta do
    ponto, então `2_RINEX/SC-HV-69.22o` continua sendo `2_RINEX/SC-HV-69.22o` do
    outro lado. Nenhum arquivo é descartado por estar fora da estrutura
    conhecida: o pacote é a pasta como ela é.
    """
    incluidos = []
    lixo = []
    with zipfile.ZipFile(destino_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for caminho in sorted(raiz_ponto.rglob("*")):
            if not caminho.is_file():
                continue
            relativo = caminho.relative_to(raiz_ponto)
            if eh_lixo(caminho, relativo):
                lixo.append(caminho)
                continue
            if relativo.parts[0] == PASTA_MONOGRAFIA:
                continue
            z.write(caminho, relativo.as_posix())
            incluidos.append(caminho)
    return incluidos, lixo


def acha_monografia(raiz_ponto):
    """O PDF da monografia do ponto, ou None.

    Levanta se houver mais de um: o acervo guarda UMA monografia por ponto, e
    escolher uma delas calado seria decidir no lugar de quem mediu.
    """
    pasta = raiz_ponto / PASTA_MONOGRAFIA
    if not pasta.is_dir():
        return None
    pdfs = sorted(
        p for p in pasta.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf" and p.name not in LIXO
    )
    if not pdfs:
        return None
    if len(pdfs) > 1:
        raise ValueError(
            f"{raiz_ponto.name}: {pasta.name} tem {len(pdfs)} PDFs "
            f"({', '.join(p.name for p in pdfs)}); o acervo guarda um por ponto"
        )
    return pdfs[0]


def sha256_de(caminho, bloco=1024 * 1024):
    """SHA-256 e tamanho em MB, lendo por bloco.

    Por bloco, e não `read()`: o pacote de um ponto passa de dezenas de MB, e o
    QGIS roda no mesmo processo da interface.
    """
    h = hashlib.sha256()
    total = 0
    with open(caminho, "rb") as f:
        for pedaco in iter(lambda: f.read(bloco), b""):
            h.update(pedaco)
            total += len(pedaco)
    return h.hexdigest(), total / (1024 * 1024)


def entrada_de_arquivo(caminho, tipo):
    """Um item de `arquivos` no manifesto, como o schema do SCA o espera."""
    checksum, tamanho_mb = sha256_de(caminho)
    return {
        "tipo_arquivo_id": tipo,
        # O SCA remonta o caminho como <nome_arquivo>.<extensao>, então os dois
        # saem separados. `SC-HV-69_pacote.zip` vira nome 'SC-HV-69_pacote' e
        # extensão 'zip'.
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
