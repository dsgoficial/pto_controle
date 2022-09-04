---
title: 'Gerar Monografia'
sidebar_position: 10
---

Gera as monografias, com o preenchimento da documentação.

# Requisitos mínimos
Possuir instalado o LibreOffice

Instalação das bibliotecas do Python
* Na pasta **rotinas_complementares_pto_controle** abra o **cmd** e instale as bibliotecas necessárias:
```
pip install -r requirements.txt
```

## Execução
Esta rotina gera monografias baseadas no Modelo em formato .odt.  
Essa rotina espera que as imagens aéreas, as imagens do ponto e a assinatura estejam no formato horizontal (paisagem), e que a imagem do croqui e o brasão do CGEO estejam no formato vertical (retrato). Para as fotos do ponto (quatro imagens da vista do ponto) o usuário pode alterar o tipo de modelo a ser utilizado.
* Caso os medidores tenham coletado as fotos no formato retrato, utilizar modelo_retrato.odt
* Caso contrario, utulizar modelo_paisagem.odt

## JSON
Antes de executar essa rotina, verificar parâmetros adicionais no arquivo **settings.json**, onde serão definidos:
* signature: caminho da imagem .jpeg da assinatura do responsável técnico dos pontos de controle.
* pathImageCGEO: caminho da imagem .jpeg do brasão do CGEO.
* pathLibreOffice: caminho do arquivo **soffice.exe** no Windows.

## Procedimento
Dentro da pasta **rotinas_complementares_pto_controle/generateMono** abra o **cmd** e execute:
```
python generateMonograpy.py "pasta_3" host porta banco usuario senha
```

* As informações da linha de comando devem ser:
    * "pasta_3": conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
    * host: localhost ou IP da máquina que armazena o banco.
    * porta: 5432 ou porta configurada.
    * banco: nome do banco criado em [Criar Banco de Dados](/guia_pto_controle/criar_banco_dados.md).
    * usuario: login de acesso ao banco de dados.
    * senha: senha de acesso ao banco de dados.