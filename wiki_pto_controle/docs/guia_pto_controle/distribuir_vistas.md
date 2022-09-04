---
title: 'Distribuir Vistas Aéreas'
sidebar_position: 9
---
Compositor de Impressão para gerar imagens para a Monografia.

## Atlas QGIS
Utiliza-se a configuração de três escalas de imagens distintas, utilizando o Atlas do QGIS, gerando assim três imagens para cada ponto: local, municipal e estadual.

Visando padronizar informações, é desejável utilizar os shapefiles de malhas municipal e estadual do IBGE, disponível [aqui](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html?=&t=acesso-ao-produto).

Adicione uma Camada PostGIS no QGIS, entrando com as informações do banco de dados onde os pontos foram salvos, será criada uma camada com os pontos, verifique se a tabela de atributos encontra-se preenchida e se há a coluna **cod_ponto**.

Além disso, carregue o .qml no ponto, com o objetivo de padronizar a simbologia de ponto de controle.

### Local
* Deve-se configurar a simbologia da camada dos Pontos de Controle de forma que se exiba no Compositor de Impressão apenas um único ponto por Atlas
    * Defina a escala 1:1.000
    * Ative uma camada de imagem de satélite (Bing Maps ou similar, utilizando o QuickMapService)
    * Configure a **Simbologia** para **Baseado em Regra**
    * Edite a regra pelo filtro conforme figura abaixo:

    | ![img8](./img/image11.png)|
    |:--:|
    | *Configuração de Simbologia* |

    * Na configuração da expessão, insira:
    ```
    @atlas_pagename = "cod_ponto"
    ```

### Municipal
* Utiliza-se da mesma configuração acima, entretanto configura-se a escala para 1:25.000.
* Visando facilitar a visualização, desabilite a camada de imagem de satélite e habilite a Malha de Municípios baixada do IBGE.

### Estadual
* Nesse caso deve-se fixar a extensão do mapa, permitindo que todo o mapa do estado seja visto e apenas o ponto irá mudar de lugar
* Visando facilitar a visualização, desabilite a camada de imagem de satélite e habilite a Malha de Estados baixada do IBGE.

## Armazenamento
* Salvar cada Atlas em pastas distintas: local, municipal, estado.
