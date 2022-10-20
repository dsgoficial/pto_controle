---
title: 'PPP'
sidebar_position: 2
---
Executada fora do QGIS, processamento de PPP pelo IBGE.

# Requisitos Mínimos
Instalar o **node.js** no shell do QGIS (no Linux é o mesmo do sistema, normal. No Windows é o 'OSGeo4W Shell').

No caso do Windows:

Adquira o npm em: https://nodejs.org/en/download/

Baixe o binário (.zip). Ao extrair terá uma pasta com vários arquivos. Você precisa dos seguintes:
- node_modules (pasta)
- node.exe
- nodevars.bat
- npm
- npm.cmd

Copie os arquivos mencionados e cole na pasta bin do QGIS (normalmente é 'C:\Program Files\QGIS 3.24.0\bin')

Instalar o **testcafe**, versão 0.17.2, responsável por automatizar o processo de upload/download das informações do PPP-IBGE. Ele deve ser instalado no Shell usado pelo QGIS.

No Windows, pesquise por 'OSGeo4W Shell' no menu iniciar. Abra o shell e digite o comando:
```
npm install -g testcafe@0.17.2
```
No Linux, basta rodar o mesmo comando no terminal normalmente.

# Procedimento
* Execute o Processing "Ferramentas para Pontos de Controle > 5- Gerar PPP"
* Leia as instruções na janela que aparecer, selecione os parâmetros e clique para rodar.
* Explicando os parâmetros:
    * "pasta da estrutura", conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
    * "pasta ppp existentes": caso já existam arquivos PPP processados do projeto, evitando duplicatas.

* Para o pleno funcionamento, principalmente em **múltiplos donwloads**, é necessário autorizar o navegador de internet a realizar vários downloads sequenciais e desabilitar a opção de Escolher Local de Salvamento, já selecionando uma pasta padrão para download dos arquivos.

| ![img8](../../img/image10.png)|
|:--:|
| *Seleção pasta donwloads* |
