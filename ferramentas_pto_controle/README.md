# Conjunto de ferramentas para medição
Conjunto de ferramentas em Python que automatizam o processamento e controle de qualidade da medição de pontos de controle.
As ferramentas estão disponibilizadas como *processing*, logo não se esqueça de ativar a aba processing do QGIS!
Para funcionalidade completa, deverá ser utilizado com o repositório localizado em https://github.com/1cgeo/rotinas_complementares_pto_controle.

## Instalação
Realize o download deste repositório e o extraia na pasta de plugins do QGIS, geralmente situada em (windows) C:\Users\$(user)\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins

## 1- Criar banco de dados
Esta ferramenta cria o banco de dados de pontos de controle necessário para a gerência do projeto.
Certifique-se que o usuário utilizado possui permissão para criar e alterar bancos no PostGgreSQL!
Os parâmetros necessários são:
- *IP da máquina* (se trabalhando localmente utilizar localhost)
- *Porta* (geralmente 5432 para PostgreSQL)
- *Nome* do banco a ser gerado
- *Usuário* do PostgreSQL
- *Senha* do PostgreSQL

Caso já exista um banco de dados com o mesmo nome a ferramenta não irá sobrescrevê-lo.

## 2- Valida estrutura de pontos de controle
Esta rotina verifica se a pasta definida atende as padronizações determinadas no Manual Técnico de Medição de Pontos de Controle do 1º Centro de Geoinformação.

### Execução
A rotina possui os seguintes parâmetros:
* *pasta da estrutura de pontos de controle*: Pasta com a estrutura de pontos de controle
* *operadores*: Nome dos operadores separados por ;
* *data*: Data de realização da medição, no formato YYYY-MM-DD
* *fuso horário*: Fuso horário dos tempos informados
* *ignora_processamento*: Valor booleano que informa se deve ignorar as pastas e arquivos de processamento na avaliação.
* *log*: Arquivo com o relatório de erros
* *JSON* com parâmetros default e parâmetros de validação: Arquivo no formato JSON que possui regras default e regras de validação. Seu formato é o seguinte:
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
Os seguintes atributos do objeto **validacao** *precisam* ser definidos para uma validação completa da estrutura de pastas:
- Altura máxima da antena: alt_max_ant
- Duração mínima do rastreio: dur_min

Os seguintes atributos do objeto **default** podem ser pré-definidos para compartilhar informações comuns aos pontos. Os seguintes atributos podem ser utilizados:

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

Valores em __(*)__ devem usar code_list, disponível nas tabelas de domínio do banco de pontos de controle. (Ou na [sql](createDB/new_db.sql) do banco)

Notas:
- O campo __validação__ é de preenchimento obrigatório. Caso não esteja preenchido corretamente a rotina não será executada
- Caso o atributo não seja definido no objeto __default__, ele será pesquisado no CSV. Opte por definir valores default no JSON caso os pontos de controle compartilhem o mesmo valor de atributo, mas em casos específicos a definição dos valores poderá ser feita diretamente no CSV.
- Cuidado com a tipologia do arquivo JSON (uso de aspas duplas, uso de ':' para definir um atributo/objeto, chaves devem estar fechadas, etc)

### Notas sobre o preenchimento do arquivo csv
A grande maioria das informações sobre os pontos de controle são extraídas do arquivo .csv (coluna cujo cabeçalho é o nome do atributo) e do campo "default" do arquivo .json (que compartilha informações de um conjunto de pontos). Todos os campos utilizáveis são definidos em [Campos Utilizáveis](https://github.com/1cgeo/ferramentas_pto_controle/blob/master/validatePoints/evaluateStructure.py#L213-L220). Para o correto funcionamento da rotina 2, todos os atributos definidos em [Campos necessários no CSV](https://github.com/1cgeo/ferramentas_pto_controle/blob/master/validatePoints/evaluateStructure.py#L223-L224) precisam estar no arquivo csv. São eles:

Atributo | Atributo no CSV (nome da coluna) | Características / Exemplos
| ------ | ------ | ------ |
Código do ponto | cod_ponto | (Estado)-(Tipo de precisão)-(Código sem zero à esquerda). Exemplo: RS-HV-1
Medidor | medidor | Ex: 3° Sgt Medidor
Data do rastreio | data_rastreio | Data no formato AAAA-MM-DD. Ex: 2020-02-23
Inicio do rastreio | inicio_rastreio | Horário no formato HH:MM. Ex: 13:34
Fim do rastreio | fim_rastreio | Horário no formato HH:MM. Ex: 14:26
Materializado | materializado | Booleano (True/False) que informa se o ponto é / foi materualizado. Ex: True
Altura da antena | altura_antena | Altura da antena em metros em relação ao solo. Ex: 1.3
Tipo de medição da altura | tipo_medicao_altura | Ver (*)
Referência de medição de altura | referencia_medicao_altura | Ver (*)
Altura do objeto | altura_objeto | Altura do objeto (muro, cercas, telhados, etc) em metros, caso medição ocorra acima dele. Ex: 1.8
Número de série do GPS | numero_serie_gps | Ex: 293441023
Número de série da antena | numero_serie_antena | Ex: 039441923

## 3- Atualiza banco de dados de controle
Esta rotina busca na pasta definida e nas suas subpastas pelos arquivos .CSV padrão de medição e atualiza o banco de dados de pontos de controle.

Todos os campos do CSV e todos os atributos definidos pelo usuário no campo _default_ do JSON serão utilizados. Caso o mesmo atributo exista no JSON e no CSV, a prioridade será do CSV. O campo *tipo_situacao_id* será atualizado com o valor 4 (Aguardando avaliação).

É essencial que seja executada a rotina **2- Valida estrutura de pontos de controle** antes da execução desta rotina.
Verifique o preenchimento do objeto __default__ no arquivo JSON antes de executar esta rotina

### Execução
Os parâmetros necessários são:
- *pasta da estrutura de pontos de controle*: Pasta com a estrutura de pontos de controle
- *IP da máquina* (se trabalhando localmente utilizar localhost)
- *Porta* (geralmente 5432 para PostgreSQL)
- *Nome* do banco de pontos de controle
- *Usuário* do PostgreSQL
- *Senha* do PostgreSQL
- *JSON* (o mesmo utilizado na ferramenta anterior)

## 4- Preparar para PPP
Esta rotina cria a pasta 6_Processamento_PPP na estrutura de pastas e compacta os arquivos RINEX no formato zip.

### Execução
Os parâmetros necessários são:
- *pasta da estrutura de pontos de controle*: Pasta com a estrutura de pontos de controle

## 5- PPP
Disponível em https://github.com/1cgeo/rotinas_complementares_pto_controle

## 6- Procedimento pós PPP
Esta rotina descompacta os arquivos PPP no formato zip e distribui os arquivos na estrutura padrão de pastas de ponto de controle.
Os arquivos da pasta 6_Processamento_PPP serão deletados e substituídos pelos novos arquivos contidos no zip
Os parâmetros necessários são:
- *Pasta com a estrutura de pontos de controle*
- *Pasta com os arquivos PPP no formato zip* : Pasta que possui os arquivos gerados pelo processamento PPP (gerados pela ferramenta 5- PPP)

## 7- Atualizar o banco com resultados do PPP
Disponível em https://github.com/1cgeo/rotinas_complementares_pto_controle

## 8- Distribuir as imagens aéreas na estrutura de pastas
Esta rotina distribui as imagens aéreas na estrutura de pastas. Para gerar imagens aéreas verificar tutorial disponível em https://github.com/1cgeo/rotinas_complementares_pto_controle. As imagens deverão estara em formato jpg e seu nome deverá coincidir com o nome do ponto (Ex: RS-HV-3452.jpg) Os parâmetros necessários são:
- *Pasta com a(s) estrutura(s) de pasta*
- *Pasta com as imagens aéreas*
- *Pasta com as imagens aéreas nível município*
- *Pasta com as imagens aéreas nível estado*

## 9- Gerar monografias
Disponível em https://github.com/1cgeo/rotinas_complementares_pto_controle

## 10- Preparar insumos para carregamento no BPC
Esta rotina gera os insumos necessários para carregamento no BPC: o arquivo GeoPackage, e o(s) arquivo(s) zipados.
Note que é necessário a execução da rotina 8- Gerar monografias, uma vez que a monografia é necessária no zip a ser gerado.
Os parâmetros necessários são:
- *pasta da estrutura de pontos de controle*: Pasta com a estrutura de pontos de controle
- *pasta de destino*: Pasta naa qual o Geopackage e os arquivos zipados serão extraídos
- *IP da máquina* (se trabalhando localmente utilizar localhost)
- *Porta* (geralmente 5432 para PostgreSQL)
- *Nome* do banco de pontos de controle
- *Usuário* do PostgreSQL
- *Senha* do PostgreSQL
