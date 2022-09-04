---
title: 'Introdução'
sidebar_position: 1
---

# Introdução

Existe uma demanda contínua por Pontos de Controle, principalmente para utilização em Controle de Qualidade, que requer o acesso rápido a pontos já levantados pelas OMDS/DSG.

Conforme a necessidade de armazenamento da coleta de Pontos de Controle, se fez necessário o desenvolvimento de rotinas que possibilitassem que a padronização das informações levantadas.  

As rotinas que aqui serão descritas visam uniformizar os arquivos que são disponibilizados no BPC e utilizados em processos pelas OMDS/DSG.

## Organograma Atual

A rotina implementada é construída de forma sequencial, utilizando processos dentro do QGIS e fora do QGIS (IBGE) e necessita ser seguida.


### Metodologia em campo
Cabe ao medidor do Ponto de Controle possuir conhecimento detalhado das Rotinas de Pontos de Controle, principalmente na [Estruturação das Pastas](/guia_pto_controle/validar_estrutura_pastas.md), visto que é o próprio medidor que deve entregar a estrutura mínima a DGEO, visando facilitar as operações.

Maiores informações para o medidor podem ser encontradas no [Manual do Medidor](/docs/manual_medidor).

### Processings do QGIS
São as rotinas que realizarão a integração dos pontos medidos em campo, um banco de dados com as informações e a geração de monografias e arquivos para o Banco de Pontos de Controle.

### Rotinas Externas
Passos além dos previstos no QGIS, resumem-se a processamento dos arquivos RINEX no [PPP-IBGE](https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados).

## Arquivos necessários

Antes de prosseguirmos para a instalação das ferramentas, seguem os links de referência:
* [Rotinas Ponto de Controle DSG](https://github.com/dsgoficial/pto_controle)
* [PPP-IBGE](https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados)
* [Shapefiles para Monografia](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html?=&t=acesso-ao-produto)
