---
title: 'Validar Estrutura de Pastas'
sidebar_position: 3
---

Detecta inconsistências nas pastas dos pontos medidos.

# Objetivo

Deverá ser utilizado pelo medidor do Ponto de Controle, esse passo verifica possíveis inconsistências relativas a falta de arquivos, incorreto preenchimento de metadados, ausência de fotos para monografia, tempo de medição incorreto, etc.

## Preenchimento dos Dados
Preencher os dados solicitados conforme descrito abaixo.
* Pasta com a estrutura de pontos de controle: essa pasta deve ser uma pasta **externa** à pasta com o nome do operador, conforme imagem abaixo:

| ![img6](./img/image1.png)|
|:--:|
| *Localização das Pastas* |

Nesse caso, a pasta escolhida deverá ser a **"pasta_3"**, pois é anterior a pasta que contém a pasta do **medidor_AAAA_MM_DD** (Cuidado para que não ocorra troca entre **_** e **-**)
* Nome dos operadores: utilizado para percorrer as pastas internas a **"pasta_3"**, caso existam diversos medidores.
    * Exemplo: Se os medidores André, João e Lucas mediram pontos no dia 06/05/2022, as pastas deverão possuir a seguinte nomenclatura:
        * joao_2022-05-06
        * lucas_2022-05-06
        * andre_2022-05-06
* Caso existam várias medições em dias distintos, com vários operadores, a pasta escolhida no passo acima deverá ser a **"pasta_2"**, sendo agora a **"pasta_3"** uma pasta com os arquivos do referido dia.
* Data no formato YYYY-MM-DD: de acordo com a data do levantamento do ponto.
* Insira o fuso horário: utilizado na correção do arquivo RINEX e comparação com o .csv. Isso permite a verificação do tempo de medição dos pontos.
* Inserir JSON com parâmetros: esse arquivo conterá as informações que são fixas para a atividade, conforme exemplo abaixo:
```
{
    "validacao": {
        "alt_max_ant" : 9,
        "dur_min" : 38
    },

    "default": {
        "modelo_gps" : "TRIMBLE 5700II",
        "modelo_antena" : "TRM39105.00",
        "tipo_ref" : 3,
        "sistema_geodesico" : 2,
        "referencial_altim" : 2,
        "referencial_grav" : 97
        \\ Outros atributos ...
    }
}
```

* Os atributos de **"validacao"** devem ser preenchidos:
    * **alt_max_ant**: altura máxima da antena
    * **dur_min**: duração mínima da medição

* Os atributos **"default"** podem ser pré-definidos para compartilhar informações comuns aos pontos. De modo geral, são as informações compartilhadas em cada atividade de medição. As informações sinalizadas com **(*)** devem ser preenchidas de acordo com o [code_list](https://github.com/dsgoficial/pto_controle/blob/main/ferramentas_pto_controle/createDB/new_db.sql), disponível nas tabelas de domínio do banco de pontos de controle. 

Atributo | Atributo no JSON | Características / Exemplos
| ------ | ------ | ------ |
Modelo do GPS | modelo_gps | Ex: Trimble 5800
Modelo da antena | modelo_antena | Ex: Trimble CFX-750
Tipo de referência | tipo_ref | Ver (*)
Sistema geodésico | sistema_geodesico | Ver (*)
Referencial altimétrico | referencial_alt | Ver (*)
Referencial gravimétrico | referencial_grav | Ver (*)
Meridiano central | meridiano_central | Meridiano em relação ao globo. Ex: 51
Fuso | fuso | Fuso da região de medição do ponto. Ex: 23S
Outra referência planimétrica | outra_ref_plan | Caso exista uma segunda referência planimétrica
Fuso horário | fuso_horario | Ex: -3
Precisão vertical esperada | precisao_vertical_esperada | Em metros. Ex: 0.08
Precisão horizontal esperada | precisao_horizontal_esperada | Em metros. Ex: 0.03
Referencial altimétrico | referencial_altim (*) | Ex: Imbituba
Outro referencial altimétrico | outro_ref_alt | Caso exista uma segunda referência altimétrica
Lote | lote | Ex: 1, A, Lote 2, etc
Método de posicionamento | metodo_posicionamento | Ver (*)
Ponto base | ponto_base | Base em caso de posicionamento relativo. Ex: AC-HV-1
Máscara de elevação | mascara_elevacao | Em graus, sem o símbolo °. Ex: 10
Taxa de gravação | taxa_gravacao | Em segundos. Ex: 5
Modelo geoidal | modelo_geoidal | Ver (*)
Órgão executante | orgao_executante | OM responsável pela medição. Ex: 1CGEO
Projeto | projeto | Ex: Projeto A, Medição B, etc
Engenheiro responsável | engenheiro_responsavel | Ex: Cap Engenheiro Responsável
CREA do engenheiro responsável | crea_engenheiro_responsavel | Ex: RJ00000
CPF do engenheiro responsável | cpf_engenheiro_responsavel | Ex: 000.000.000-00
Geometria aproximada | geometria_aproximada | Booleano (True ou False)
Tipo de referência geodésica | tipo_pto_ref_geod_topo | Ver (*)
Rede de referência | rede_referencia | Ver (*)
Referencial gravimétrico | referencial_grav | (*)

* O campo de **"validacao"** é de preenchimento obrigatório, caso não esteja preenchido, a rotina não será executada. No caso do campo **"default"**, ele pode não estar preenchido, a rotina pesquisará as informações no .csv do medidor do ponto. Opte sempre por definir os valores repetidos no **"default"**, isso reduzirá a chances de erros no preenchimento do .csv, que depende de cada medidor. Em casos específicos, se a mesma chave for preenchida no .json e no .csv, o .csv terá prioridade.

* Caminho do relatório: salva um arquivo de texto com as informações sobre a pasta e suas inconsistências.
* Após clicar em **Executar**, o arquivo salvo e a mensagem em tela retornarão todos os erros, corrija-os até obter a seguinte mensagem:
```
'A pasta [...] não contém erros.
```