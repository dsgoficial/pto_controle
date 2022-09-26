---
title: 'Atualizar Banco de Dados Pós-Processamento'
sidebar_position: 8
---
Executada fora do QGIS, leitura dos arquivos gerados no PPP ou RTE e inserção no banco.

## Requisitos Mínimos
Existência dos arquivos PPP processados pelo IBGE ou do arquivo .csv gerado pelo usuário durante o RTE.

## Atualização das Informações com PPP:
* Navege até a pasta **rotinas_complementares_pto_controle** e entre na pasta **refreshFromPPP**.
* Abra o **cmd** e execute o seguinte comando:
```
python refreshFromPPP_txt.py "pasta_3" host porta banco usuario senha
```
Utilize _txt.py caso o arquivo a ser lido do IBGE seja o arquivo de texto, utilize _pdf.py caso contrário.
* As informações da linha de comando devem ser:
    * "pasta_3": conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
    * host: localhost ou IP da máquina que armazena o banco.
    * porta: 5432 ou porta configurada.
    * banco: nome do banco criado em [Criar Banco de Dados](/guia_pto_controle/criar_banco_dados.md).
    * usuario: login de acesso ao banco de dados.
    * senha: senha de acesso ao banco de dados.

## Atualização das Informações com RTE:
* Navege até a pasta **rotinas_complementares_pto_controle** e entre na pasta **refreshFromPPP**.
* Abra o **cmd** e execute o seguinte comando:
```
python refreshFromCSV.py "pasta_3" host porta banco usuario senha arquivo_csv
```
* As informações da linha de comando devem ser:
    * "pasta_3": conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
    * host: localhost ou IP da máquina que armazena o banco.
    * porta: 5432 ou porta configurada.
    * banco: nome do banco criado em [Criar Banco de Dados](/guia_pto_controle/criar_banco_dados.md).
    * usuario: login de acesso ao banco de dados.
    * senha: senha de acesso ao banco de dados.
    * arquivo_csv: caminho do arquivo .csv gerado pelo usuário durante o processamento do posicionamento relativo estático.