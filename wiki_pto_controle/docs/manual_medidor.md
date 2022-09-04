---
title: 'Manual do Medidor'
sidebar_position: 3
---

Durante a coleta de pontos, o medidor deve possuir o conhecimento necessário para o preenchimento correto dos documentos, possibilitando a correta montagem das monografias.

## Procedimento físico
* Realizar o correto posicionamento da estação medidora.
* Coletar as quatro fotos (quatro quadrantes) necessárias para a monografia, todas na mesma orientação (retrato ou paisagem).

## Preenchimento do .csv
* O .csv é um formato padrão de preenchimento, apenas as informações previstas devem ir no .csv, as demais são preenchidas pelo gerente da equipe no arquivo .json
```
* cod_ponto: não devem existir 0 na frente do nome do ponto, o padrão seguido pelo 1º CGEO é: UF-HV-XXXX, sendo XXXX um número de 4 digitos
* medidor: nome completo do medidor
* data_rastreio: no formato YYYY-MM-DD
* inicio_rastreio: no formato HH:MM
* fim_rastreio: no formato HH:MM
* materializado:
    * 0 para não materializado
    * 1 para materalizado
* altura_antena: altura em metros da antena, utilizando **ponto** como separador
* tipo_medicao_altura: 
* referencia_medicao_altura:
* altura_objeto:
* numero_serie_gps: de acordo com o aparelho, será comparado com o RINEX gerado
* numero_serie_antena: de acordo com o aparelho, será comparado com o RINEX gerado
* observacao: observações diversas
```

A tabela abaixo detalha melhor o preenchimento do arquivo .csv.

Atributo | Atributo no CSV (nome da coluna) | Características / Exemplos
| ------ | ------ | ------ |
Código do ponto | cod_ponto | (Estado)-(Tipo de precisão)-(Código sem zero à esquerda). Exemplo: RS-HV-1
Medidor | medidor | Ex: Nome completo medidor
Data do rastreio | data_rastreio | Data no formato AAAA-MM-DD. Ex: 2020-02-23
Inicio do rastreio | inicio_rastreio | Horário no formato HH:MM. Ex: 13:34
Fim do rastreio | fim_rastreio | Horário no formato HH:MM. Ex: 14:26
Materializado | materializado | Booleano (True/False) que informa se o ponto é/foi materializado. Ex: True
Altura da antena | altura_antena | Altura da antena em metros em relação ao solo. Ex: 1.3
Tipo de medição da altura | tipo_medicao_altura | Ver (*)
Referência de medição de altura | referencia_medicao_altura | Ver (*)
Altura do objeto | altura_objeto | Altura do objeto (muro, cercas, telhados, etc) em metros, caso medição ocorra acima dele. Ex: 1.8
Número de série do GPS | numero_serie_gps | Ex: 293441023
Número de série da antena | numero_serie_antena | Ex: 039441923

## Demais informações
* Nas informações de **inicio_rastreio** e *fim_rastreio** devem ser informados o momento que o aparelho foi ligado e não o momento que ele começou a rastrear, bem como no fim do rastreio, deve ser informado o momento que o aparelho foi desligado. Cabe ao medidor medir o tempo úlil de rastreio, que varia de acordo com o aparelho utilizado.
* O arquivo bruto oriundo do aparelho, .t01 para TRIMBLE e .tps para a Topcon, deve possuir o mesmo nome do cod_ponto
* A codificação da pasta deve seguir a estrutura: nomemedidor_AAAA_MM_DD e dentro dessa pasta se colocam os pontos medidos, seguindo a estrutura dos nomes do cod_ponto
* O croqui deve ser salvo no formato .jpg e na orientação retrato
* A estrutura básica das pastas para cada cod_ponto é:
```
1_Formato_Nativo
2_RINEX
3_Foto_Rastreio
4_Croqui
5_Foto_Auxiliar
```
* O operador deve realizar o processamento do arquivo bruto e sua conversão em arquivos RINEX (.o, .g, .n), utilizando programas semelhantes ao Convert2RINEX da TRIMBLE