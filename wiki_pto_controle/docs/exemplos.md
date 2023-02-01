---
title: 'Exemplos'
sidebar_position: 3
---
# Arquivos

Acessando [neste link](https://github.com/dsgoficial/pto_controle/tree/main/arquivos), o usuário encontrará os seguintes arquivos, detalhados abaixo.
## bpc

Modelo de arquivo gerado pela Rotina de Ponto de Controle, em condições de ser colocada no Banco de Pontos de Controle.

# eliomar_2022-07-03

Uma pasta com preenchimento padrão, contendo os arquivos necessários que o medidor deve elaborar após realizar a coleta dos pontos, isto é: conjunto das pastas de 1 a 5 conforme o [Manual do Medidor](/docs/manual_medidor).

Além do arquivo das pastas, do arquivo de metadados preenchido corretamente, também se faz necessário:
* Fotos de quatro quadrantes distintos da localização do ponto, com a nomenclatura correta.
* Arquivo bruto baixado da coletora (.t01 para TRIMBLE e .tps para TOPCON).
* Arquivos RINEX processados (.o, .g e/ou .n).
* Foto do Croqui, com a nomenclatura correta, na orientação retrato.

## eliomar_2022-07-03_processada

Uma pasta já processada, com os arquivos criados ao utilizar a Rotina de Pontos de Controle por completo.

## processamento_rte.csv

Um CSV com modelagem padrão caso o usuário deseje realizar o processamento via RTE.
## qpt_pto_controle.qml

Um QML padrão, contendo apenas a **Simbologia** e os **Rótulos** para serem carregados na camada de Pontos de Controle antes de executar a [Distribuição de Vistas Aéreas](/guia_pto_controle/distribuir_vistas.md).