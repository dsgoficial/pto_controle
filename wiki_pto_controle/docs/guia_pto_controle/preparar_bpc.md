---
title: 'Preparar para o BPC'
sidebar_position: 11
---

Gera arquivos para serem colocados no BPC.

# Preparar para o BPC

* Pasta com os pontos de controle: conforme [Validação da Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
* Pasta onde serão gerados os arquivos: definir a pasta onde serão salvos os arquivos a serem carregados no BPC.
* IP do Computador a Senha do PostgreSQL: mesmas informações usadas para a [criação do banco de dados](/guia_pto_controle/criar_banco_dados.md).

## SFTP do BPC

Para realizar o carregamento dos pontos no BPC, deve-se acessar o servidor para carregar os arquivos gerados pelo passo **10 - Preparar para BPC**. Cada Centro de Geoinformação possui seus dados de acesso. Ao logar no SFTP, utilizando, por exemplo, FileZilla ou WinSCP, o usuário deve:
* Buscar o repositório na pasta /home/sigweb/repositorio/Anexos
* Nessa pasta, o usuário realiza a transferência dos arquivos .zip gerados pelo passo 10 da rotina no QGIS.
* Em seguida, acessa a página Web do BPC, o usuário vai na opção Adicionar Geopackage, e carrega o .gpkg gerado pela rotina e equivalente aos .zip carregados no passo acima.
* Aguarda o processo ser finalizado, a própria página web do BPC retorna o feedback de conclusão ou caso tenha dado algum erro, o log de erro do usuário.