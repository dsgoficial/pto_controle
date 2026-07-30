# -*- coding: utf-8 -*-
"""Resolucao do formato de imagem do `native:atlaslayouttoimage`.

Por que isto existe, e por que num arquivo so:

O parametro EXTENSION daquele algoritmo e um ENUM, e o valor que se passa e o
INDICE. A lista muda de uma versao do QGIS para outra, e mudou duas vezes:

- QGIS 3.x e 4.0.0: rotulos em minuscula, 'jpeg' no indice 5 e 'jpg' no 6;
- QGIS 4.2.0: rotulos em MAIUSCULA, 'JPEG' no indice 6 e 'JPG' no 7.

O codigo original fixava 5, e as imagens saiam .jpeg enquanto o distribuidor
procurava .jpg. O conserto de 2026-07-29 passou a resolver pelo NOME, mas
comparava minuscula com minuscula e, no QGIS 4.2, nao achava 'jpg': caia num
fallback numerico 6, que naquela versao e JPEG. O defeito voltou pela porta do
fallback, medido em 2026-07-30.

Duas regras que este modulo faz valer:

1. A comparacao e CASE-INSENSITIVE, porque o rotulo do enum e texto de interface.
2. Nao existe fallback numerico. Indice chutado escreve um formato que o
   distribuidor nao acha, e o unico sinal e uma pasta vazia. Melhor parar aqui,
   com a lista das opcoes vivas na mensagem.
"""
from qgis.core import QgsApplication, QgsProcessingException

ALG_ATLAS = 'native:atlaslayouttoimage'


def indice_da_extensao(nome='jpg', alg_id=ALG_ATLAS):
    """O indice do formato `nome` no enum EXTENSION, lido do algoritmo VIVO."""
    alg = QgsApplication.processingRegistry().algorithmById(alg_id)
    if alg is None:
        raise QgsProcessingException(
            'O algoritmo {} nao esta registrado. Sem ele nao ha como exportar '
            'o atlas.'.format(alg_id)
        )
    for definicao in alg.parameterDefinitions():
        if definicao.name() != 'EXTENSION':
            continue
        opcoes = list(definicao.options())
        for indice, opcao in enumerate(opcoes):
            if str(opcao).lower() == nome.lower():
                return indice
        raise QgsProcessingException(
            'O formato {!r} nao esta nas opcoes de EXTENSION do {}. '
            'Opcoes vivas: {}. Escolher indice por chute escreveria outro '
            'formato, e a pasta de saida apareceria vazia sem erro.'.format(
                nome, alg_id, opcoes)
        )
    raise QgsProcessingException(
        'O {} nao tem o parametro EXTENSION nesta versao do QGIS.'.format(alg_id)
    )
