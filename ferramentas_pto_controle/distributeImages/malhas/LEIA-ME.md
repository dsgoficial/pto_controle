# Malhas de municipio e de estado do P08

O P08 desenha duas vistas de localizacao de cada ponto: a municipal e a estadual.
As duas saem de `assets/municipios.gpkg` e `assets/estados.gpkg`, gerados por
`gerar_malhas.sh` a partir da malha municipal do IBGE.

## O que cada arquivo tem

| arquivo | feicoes | vertices | tamanho | campos |
|---|---|---|---|---|
| `assets/municipios.gpkg` | 5.572 | 1.315.650 | 25,0 MB | `CD_MUN`, `NM_MUN`, `SIGLA_UF` |
| `assets/estados.gpkg` | 27 | 44.256 | 0,80 MB | `CD_UF`, `SIGLA_UF`, `NM_UF`, `NM_REGIAO` |

SRC: SIRGAS 2000 (EPSG:4674). Origem: malha municipal do IBGE de 2022.

O `qml_municipio.qml` rotula por `NM_MUN` e o `qml_estado.qml` por `NM_UF`. A
malha do IBGE nao traz `NM_UF`, so a sigla, entao o script preenche o nome.

## Por que simplificar

A malha do IBGE tem 16.923.496 vertices e pesa 263 MB. Esse detalhe nao chega na
imagem: o quadro do P08 tem 100 x 60 mm a 300 dpi, ou 1.181 px de largura. As duas
camadas juntas cairam para 25,8 MB, ou um decimo do original.

## Como a tolerancia foi escolhida

Por medicao, e nao por gosto. Para cada um dos 5.572 municipios mediu-se o erro em
PIXEL DA IMAGEM FINAL: a largura media da faixa entre o poligono original e o
simplificado (area da diferenca simetrica dividida pelo perimetro), dividida pelo
tamanho do pixel daquele municipio.

Com tolerancia UNICA:

| tolerancia | vertices | MB | erro mediano | acima de 1 px | pior caso |
|---|---|---|---|---|---|
| original | 16.923.496 | 263 | - | - | - |
| 0,0005 grau (55 m) | 3.375.298 | 56 | 0,06 px | 2 | 1,3 px |
| 0,001 grau (111 m) | 2.031.010 | 36 | 0,17 px | 11 | 3,0 px |
| 0,002 grau (222 m) | 1.143.772 | 22 | 0,44 px | 540 | 8,4 px |

Com as SEIS FAIXAS que o script aplica: **1.315.650 vertices, 25,0 MB, erro
mediano 0,29 px, NENHUM municipio acima de 1 px, pior caso 0,8 px**. Ou seja, ao
mesmo tempo menor e mais fiel que a tolerancia unica de 0,001 grau.

O ganho vem de uma observacao simples: o quadro enquadra UMA feicao por vez, entao
o pixel no terreno muda de municipio para municipio. Altamira aparece com 1097 m
por pixel e Santa Cruz de Minas com 3,7 m. A faixa amarra a tolerancia ao pixel:

| faixa | pixel do quadro | tolerancia | municipios |
|---|---|---|---|
| 1 | ate 10 m | 0,0002 grau (22 m) | 14 |
| 2 | 10 a 20 m | 0,0005 grau (55 m) | 397 |
| 3 | 20 a 40 m | 0,001 grau (111 m) | 2.065 |
| 4 | 40 a 80 m | 0,002 grau (222 m) | 1.978 |
| 5 | 80 a 160 m | 0,004 grau (445 m) | 827 |
| 6 | acima de 160 m | 0,01 grau (1.112 m) | 291 |

Nos estados a tolerancia e 0,005 grau. O estado e visto com 200 a 2.400 km de
largura, entao o pior caso e o Distrito Federal, com 0,31 px.

## Como a adjacencia sobrevive

Duas garantias.

A primeira e usar `native:coveragesimplify` (GEOS CoverageSimplify), que trata o
conjunto como COBERTURA: a aresta compartilhada entre dois municipios e
simplificada uma vez so. O `native:simplifygeometries` trata feicao a feicao e
abriria fenda e sobreposicao entre vizinhos.

A segunda e o uso de `PRESERVE_BOUNDARY` para variar a tolerancia. Cada passada
roda sobre a subcobertura de uma faixa e das mais grossas, com a borda EXTERNA
daquela subcobertura presa. Essa borda e exatamente o conjunto de arestas que a
subcobertura divide com as faixas mais finas, ja fixadas na passada anterior. Por
isso as passadas vao da mais fina para a mais grossa, e nunca ao contrario.

Verificacao: `native:coveragevalidate` acusa 27 pontos de aresta que nao casa,
tanto na malha original do IBGE quanto no resultado. A simplificacao NAO criou
nenhum defeito novo. A area total tambem se manteve: 710,313314 graus quadrados na
origem e 710,313271 no resultado.

## O defeito que veio do IBGE

A malha de 2022 nao e uma cobertura valida na origem. 27 municipios tem aresta que
nao casa com o vizinho, somando 114 km, a maior com 30 km. Nao se corrigiu isso:
mexer ali muda limite municipal oficial. A simplificacao preserva esses pontos como
estao.

## Como gerar de novo

```
QGIS_PROCESS="/caminho/do/qgis_process-qgis.bat" \
  ./gerar_malhas.sh MALHA_MUNICIPAL_IBGE.gpkg ../assets
```

Leva cerca de 10 minutos. A malha do IBGE se baixa do portal de geociencias do
proprio IBGE (organizacao do territorio, malhas territoriais).
