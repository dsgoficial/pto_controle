---
title: 'PPP'
sidebar_position: 2
---
Executada fora do QGIS, processamento de PPP pelo IBGE.

# Requisitos Mínimos
Instalar o **node.js** na máquina, lembrar de autorizar a colocação do NODE no PATH da máquina.

Instalar o **testcafe**, responsável por automatizar o processo de upload/download das informações do PPP-IBGE.
```
npm install -g testcafe@0.17.2
```

# Procedimento
* Na pasta **rotinas_complementares_pto_controle**, procure a pasta **ppp** e abra do **cmd** dentro dessa pasta.
* Execute o comando:
```
testcafe -c 1 chrome ppp.js "pasta_3" "pasta_ppp_existentes" seuemail@provedor.com.br --proxy username:senha@proxy:porta
```
* Os atributos a serem preenchidos são:
    * "pasta_3", conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
    * "pasta_ppp_existentes": caso já existam arquivos PPP processados do projeto, evitando duplicatas.
    * -c 1: altere o valor para abrir mais navegadores, de preferência chrome ou firefox.
    * --proxy: caso seja necessário autenticação por proxy.

* Para o pleno funcionamento, principalmente em **múltiplos donwloads**, é necessário autorizar o navegador de internet a realizar vários downloads sequenciais e desabilitar a opção de Escolher Local de Salvamento, já selecionando uma pasta padrão para download dos arquivos.

| ![img8](../../img/image10.png)|
|:--:|
| *Seleção pasta donwloads* |
