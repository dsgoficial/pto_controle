---
title: 'Atualizar Banco de Dados'
sidebar_position: 4
---
Carrega previamente as informações não-processadas pelo PPP, apenas para estruturação.

# Objetivo
Esta rotina busca na pasta definida e nas suas subpastas pelos arquivos .csv padrões de medição e atualiza o banco de dados de pontos de controle.

Todos os campos do .csv e todos os atributos definidos pelo usuário no campo default do .json serão utilizados. Caso o mesmo atributo exista no .json e no .csv, a prioridade será do .csv. O campo **tipo_situacao_id** será atualizado com o valor 4 (Aguardando Avaliação).

Verifique o preenchimento do objeto default no arquivo .json antes de executar esta rotina.

# Requisitos Mínimos
Possuir a [Validação de Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md) retornando zero erros.

## Preenchimento dos Dados
* O modelo de pasta a ser seguido é o mesmo da [Validação de Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
* O arquivo .json é o mesmo utilizado na Validação da Estrutura de Pastas.
* IP do Computador a Senha do PostgreSQL: mesmas informações usadas para a [criação do banco de dados](/guia_pto_controle/criar_banco_dados.md).

| ![img7](./img/image5.png)|
|:--:|
| *Atualização do Banco de Dados* |
