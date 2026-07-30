# pto-controle-cli

Executa os algoritmos de Processing do plugin **Ponto de Controle** por linha de
comando, headless, sem abrir o QGIS Desktop. E uma camada fina sobre o
`qgis_process` oficial do QGIS.

Irmao do `dsgtools_cli` do DsgTools, no padrao agent-first da DGEO: cada aplicacao
nossa entrega, alem da interface para humanos, uma interface desenhada para agentes,
versionada no repositorio da propria aplicacao.

Ele mora DENTRO do pacote do plugin (`ferramentas_pto_controle/pto_controle_cli/`),
e nao ao lado dele. Assim o CLI viaja junto na instalacao: onde o plugin estiver
instalado, o CLI esta. A pasta nao tem `__init__.py`, entao o QGIS nao a importa ao
carregar o plugin.

## Por que ele existe

O plugin resolve o fluxo inteiro do ponto de controle (P01 a P12 do manual), mas so
pela caixa de ferramentas do QGIS. Um lote de pontos, uma re-execucao depois de
corrigir metadado, ou qualquer automacao exigia clique. O CLI tira isso do caminho.

A fonte da verdade e sempre o proprio `qgis_process`, consultado ao vivo. Nao existe
catalogo de algoritmos nem de parametros dentro deste CLI: um algoritmo novo no
provider aparece sozinho, sem editar uma linha aqui. **Contrato copiado apodrece**, e
o desenho existe para nao ter copia.

## Instalar

O CLI e Python puro, so biblioteca padrao. Roda com qualquer `python`. O que ele
exige e o QGIS e o plugin habilitado.

1. **QGIS 4.0 ou superior** instalado (e ele que traz o `qgis_process`).
2. **O plugin instalado no perfil do QGIS 4.** Em desenvolvimento, o caminho e um
   link da pasta `ferramentas_pto_controle` deste repositorio para
   `<perfil>/python/plugins`.
3. **O plugin habilitado PARA O `qgis_process`**, que e uma habilitacao SEPARADA da
   do QGIS Desktop. Este e o modo de falha mais caro, porque e silencioso: o plugin
   pode estar ativo no Desktop e o `list` vir com zero algoritmos e stderr vazio.

Confirme tudo de uma vez:

```
python pto_controle_cli.py doctor --fix
```

O `--fix` habilita o plugin no perfil certo. Nao cole `qgis_process plugins enable`
num terminal comum: o `qgis_process` resolve o perfil legado `QGIS/QGIS3` por padrao,
enquanto o QGIS 4 usa `QGIS/QGIS4`. O enable "da certo" e o `list` continua vazio. O
CLI redireciona sozinho via `QGIS_CUSTOM_CONFIG_PATH`.

Se o CLI nao achar o `qgis_process`, aponte:

```
set PTOCONTROLE_QGIS_PROCESS=C:\Program Files\QGIS 4.0.0\bin\qgis_process-qgis.bat
```

## Comandos

| Comando | O que faz |
|---|---|
| `doctor [--fix]` | Diagnostica o ambiente. Distingue plugin ausente, instalado-mas-nao-habilitado e carregado-com-zero-algoritmos, cada um com o conserto exato. Sai 1 quando ha problema. |
| `list [--json]` | Lista os algoritmos do provider `ptocontrole`, ao vivo. Com zero algoritmos ele avisa que o provider nao carregou e sai 1, em vez de mentir "0 disponiveis". |
| `describe <alg> [--json]` | Contrato do algoritmo: uma linha por parametro, com o mapa de indice para rotulo dos enums, mais as regras curadas. Fonte da verdade dos parametros: nunca decore, consulte aqui. |
| `run <alg> [KEY=VALUE ...]` | Valida localmente e executa. Reprovacao sai com codigo 2, sem executar. |
| `cache [--clear]` | Estado e limpeza do cache de contrato. |

**A ordem dos argumentos importa**: as flags vao ANTES dos `KEY=VALUE`
(`run <alg> --dry-run K=V`, e nao `run <alg> K=V --dry-run`). E limitacao do
`argparse` com posicional variadico.

### Nomear o algoritmo

O id segue a regra do QGIS: so minuscula e digito, sem separador. Pode vir com ou sem
o prefixo `ptocontrole:`. Um **prefixo do nome** basta, desde que identifique um
algoritmo so:

```
python pto_controle_cli.py describe ptocontrole:criarbanco
python pto_controle_cli.py describe criarbanco
python pto_controle_cli.py describe criarban
```

Prefixo ambiguo e ERRO, com a lista dos candidatos, nunca uma escolha silenciosa. A
resolucao consulta a lista viva, entao um algoritmo novo entra sozinho.

### As tres formas de passar parametros

Equivalentes e combinaveis, mescladas nesta ordem: `--params`, depois `--stdin`,
depois os tokens `KEY=VALUE`.

- **Tokens `KEY=VALUE`** na linha de comando.
- **`--params arq.json`**: aceita `{"inputs": {...}}` ou o objeto `{...}` direto.
- **`--stdin`**: o mesmo JSON, por pipe.

Regras de tipo: **enum recebe o indice numerico**, nunca o rotulo (veja o mapa no
`describe`). A coercao dos tokens e conservadora: so viram numero os inteiros limpos
e os floats simples. Permanecem string `007`, `1_000`, `inf`, `nan`, `1e3` e
`SP-HV-0042`. Quem precisa do tipo JSON nativo usa `--params` ou `--stdin`.

**Booleano se coage contra o CONTRATO.** Um token e sempre texto, e a string `'false'`
e nao-vazia, portanto verdadeira: `IGN_PROC=false` faria o OPOSTO do pedido, calado.
Depois de ler o contrato, o CLI converte a string para booleano JSON nos parametros
declarados `boolean`, aceita `true/false`, `1/0`, `sim/nao`, `yes/no`, e REPROVA o que
nao souber ler, em vez de chutar um valor.

## Nao ha segredo neste CLI

Enquanto o plugin usava PostgreSQL, seis algoritmos recebiam a senha como
parametro comum, e o CLI tinha um guardrail para ela: leitura do ambiente,
mascara na saida e aviso quando o valor vinha na linha de comando.

Desde 2026-07-28 a missao e um arquivo GeoPackage e **nenhum algoritmo recebe
credencial**. O guardrail foi REMOVIDO junto com o PostgreSQL, em vez de ficar
como codigo morto protegendo o que nao existe.

O que ficou no lugar dele e um teste: `test_nenhum_algoritmo_pede_segredo` varre
o contrato vivo dos algoritmos e reprova se aparecer parametro com cara de senha
ou token. Se isso acontecer, alguem reintroduziu credencial na linha de comando, e
o guardrail precisa voltar junto. O alarme custa uma regex, e nao um modulo.

## Validacao antes de executar

O `run` confere os parametros contra o contrato do proprio algoritmo antes de gastar
a execucao. Ele pega:

- **nome de parametro inexistente**, com sugestao do parecido;
- **obrigatorio ausente**, inclusive as saidas;
- **indice de enum fora da faixa**, e rotulo passado no lugar do indice.

O primeiro e o que mais importa. O `qgis_process` **ignora a chave desconhecida em
silencio** e aplica o padrao do parametro que voce queria setar; o erro so aparece la
na frente, com outra cara, ou nao aparece nunca e o resultado sai errado calado. E a
mesma doenca do `stripUnknown` do Joi e do `z.object` do Zod, e nao e bug de
biblioteca: e propriedade da validacao permissiva.

Reprovacao sai com **codigo 2 e nada executado**, imprimindo o contrato dos
parametros citados, para corrigir sem uma segunda consulta (que custaria segundos).

Escapes: `--no-check` pula a validacao, `--dry-run` valida e mostra o que seria
executado sem executar.

## Cache do contrato

Buscar o contrato custa segundos, porque cada chamada sobe o QGIS inteiro. Validar
todo `run` de forma ingenua dobraria o custo, entao o contrato (e a lista de
algoritmos) ficam em cache em disco, em `%TEMP%/pto_controle_cli_cache`
(override por `PTOCONTROLE_CLI_CACHE`).

A impressao digital combina mtime e tamanho do `qgis_process`, da pasta do plugin e
do `metadata.txt`.

**Limite conhecido**: a impressao digital NAO detecta edicao de um `.py` de algoritmo
dentro do plugin. Varrer a arvore a cada `run` custaria mais do que economiza. Ao
desenvolver o plugin, use `--refresh-cache` ou `cache --clear`.

## Saida e codigo de retorno

O `run` respeita o `returncode` do subprocesso como verdade de sucesso ou falha (0
sucesso, nao-zero falha). O JSON sai no **stdout** nos dois casos, com o **stderr**
separado. Quem orquestra deve checar o **codigo de saida**, nunca inferir sucesso do
conteudo.

O stderr pode trazer ruido de outros plugins do perfil. O CLI le so o stdout, entao o
ruido nao contamina os dados.

Codigos: **0** sucesso, **2** reprovado na validacao local (nada executado), qualquer
outro e o codigo do proprio `qgis_process`.

## Testes

```
pytest ferramentas_pto_controle/pto_controle_cli/tests -v
```

Tres grupos:

- **`test_cli_contract.py`**: validacao, coercao, cache e renderizacao. Nao
  precisa de QGIS: o contrato entra como fixture. A validacao existe para poupar a
  chamada cara, entao testa-la nao pode custar essa chamada.
- **`test_ids_do_plugin.py`**: guarda dos ids, lida do fonte do plugin por `ast`, sem
  importar QGIS. E o alarme contra a regressao que motivou este CLI (ver abaixo).
  Amarra tambem as anotacoes curadas aos ids reais.
- **`test_integracao_qgis.py`**: roda contra o provider REAL. Pula sozinho sem QGIS.
  Nunca usa mock: o valor do desenho e nao ter copia, e mock testaria a copia. Quando
  o plugin mudar, estes quebram, e e esse o alarme.

## O conserto de 2026-07-28 nos ids

Ate esta data o plugin era inutilizavel pelo `qgis_process`, por dois defeitos:

- o provider devolvia `id() == 'provider'`, o generico do template, que colide com
  qualquer outro plugin gerado do mesmo molde;
- os quinze algoritmos devolviam o **titulo humano** no `name()`
  (`'01 - Criar banco de dados'`). Em um `QgsProcessingAlgorithm` o `name()` E o
  identificador, nao o rotulo. O id real virava
  `provider:01 - Criar banco de dados`, com espaco e acento dentro.

O conserto poe um slug no `name()` e desce o titulo para o `displayName()`. **A caixa
de ferramentas do QGIS nao mudou**: o rotulo numerado continua la, e continua
ordenando os passos na ordem do manual. O que mudou e que agora existe um id
invocavel.

Quebra modelo ou script salvo que cite o id antigo. Como o id antigo era impossivel
de escrever, o risco e baixo, mas nao e nulo.

| id | passo | rotulo no QGIS | fase |
|---|---|---|---|
| `criarbanco` | P01 | 01 - Criar a missao (GeoPackage) | 1. Preparar a missao |
| `validarestrutura` | P02 | 02 - Validar a estrutura de pastas | 1. Preparar a missao |
| `atualizarbanco` | P03 | 03 - Atualizar a missao | 1. Preparar a missao |
| `prepararprocessamento` | P04 | 04 - Preparar para processamento | 1. Preparar a missao |
| `posppp` | P06 | 06 - Procedimento pos PPP | 2. Incorporar o processamento |
| `atualizarbancoppprte` | P07 | 07 - Atualizar a missao com dados do PPP/RTE | 2. Incorporar o processamento |
| `distribuirvistas` | P08 | 08 - Distribuir vistas aereas na estrutura de pasta | 3. Documentar o ponto |
| `distribuircroqui` | P09 | 09 - Gerar e distribuir croqui digital na estrutura de pasta | 3. Documentar o ponto |
| `distribuirmonografia` | P10 | 10 - Gerar e distribuir monografias nas pastas | 3. Documentar o ponto |
| `prepararbpc` | P11 | 11 - Preparar insumos para carregamento no BPC | 4. Entregar |
| `prepararsca` | P12 | 12 - Preparar a missao para o Controle do Acervo | 4. Entregar |
| `corrigirdatatrimble` | (sem numero) | Corrigir ToW para TRIMBLE | Auxiliares |

A numeracao mudou em 2026-07-30, e os IDS NAO: quem invoca pelo CLI nao muda nada.
Sairam tres algoritmos (P11 caminhos nos atributos, P12 download dos arquivos e P16
compactar as pastas), o croqui digital subiu de 15 para 09 e a entrega foi para o fim.
A auxiliar perdeu o numero, porque numero e posto no fluxo e ela roda antes do P02.

Nao existe P05: e o passo externo, no site do PPP-IBGE ou num software de RTE.

## Onde mora o help

O `qgis_process help --json` **nao expoe o `shortHelpString()`**, que e o help longo
do painel do QGIS. Quem escreve so ali deixa o CLI mudo, e nao percebe, porque ve o
texto na GUI. O canal que chega ao headless e o `shortDescription()`.

| Onde | O que carrega | Quem ve |
|---|---|---|
| `shortDescription()` | uma linha: o passo e o que faz | painel do QGIS e `describe` |
| `shortHelpString()` | help longo: pre-requisito, passo seguinte, armadilha | so o painel do QGIS |
| `annotations.json` | regra de dominio e exemplo de invocacao | so o `describe` |

Um teste de integracao reprova algoritmo sem `shortDescription()`.

## annotations.json

Conhecimento de dominio curado, por id, opcional. Entra so o que nem a introspecao
nem o proprio plugin dizem: a regra de dominio e o exemplo de invocacao.

Nome, tipo e obrigatoriedade de parametro **nao entram**, porque o `describe` ja le
isso ao vivo e uma copia aqui apodreceria. Um teste faz isso valer. A `description`
tambem saiu, quando o `shortDescription()` de cada algoritmo passou a dar esse texto
ao vivo.

## Limites conhecidos

- **O fluxo inteiro foi exercitado headless de ponta a ponta** (2026-07-30, QGIS
  4.2.0), pelo proprio CLI, sobre os dados de exemplo de `arquivos/`: P01, P02, P03,
  P04, P07, P08, P09, P10, P11 e P12, com o resultado conferido NO DESTINO (a missao
  no disco, as imagens nas pastas, o PDF, o gpkg do BPC e o manifesto do acervo), e
  nao no retorno da ferramenta. Falta prova de execucao do P06 (`posppp`), que exige o
  arquivo devolvido pelo PPP do IBGE, e da auxiliar do ToW, que exige RINEX da coletora
  TRIMBLE.
- **O ramo RTE do P07 nao foi exercitado.** A prova usou o ramo PPP, porque a amostra
  do repositorio tem o resultado do PPP e o `processamento_rte.csv` de exemplo cobre
  outros pontos.
- **O P11 PARA quando nenhum ponto passa nos criterios do BPC** (desde 2026-07-30).
  Antes ele avisava e devolvia exit 0, com um GeoPackage vazio: quem orquestra pelo
  codigo de saida lia sucesso. O criterio que mais reprova e o ponto que ainda nao
  esta APROVADO (`tipo_situacao` 3), e aprovar e decisao humana, fora do plugin.
- **Os passos de layout (P08, P09, P10) precisam de tres variaveis de ambiente**, e o
  CLI as aplica sozinho desde 2026-07-30 (ver `ambiente_de_layout`). O `doctor` mostra
  quais. Antes disso era conhecimento fora da banda: sem elas a monografia sai com
  texto estourando a celula, ou a reprojecao erra calada porque um `proj.db` de outra
  instalacao no PATH sombreia o do QGIS.
- **Parametro obrigatorio COM padrao no contrato nao precisa ser passado**, desde
  2026-07-30. O motor aplica o padrao sozinho, e cobrar era ser mais estrito do que
  ele sem ganho nenhum. Padrao de string VAZIA nao conta, e continua cobrado.
- **O `psycopg2` ja vem no Python do QGIS** (2.9.11 confirmado em 2026-07-28), mas
  nenhum algoritmo usa mais PostgreSQL: a missao e um GeoPackage desde 2026-07-28.
