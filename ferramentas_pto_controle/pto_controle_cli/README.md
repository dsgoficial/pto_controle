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

O plugin resolve o fluxo inteiro do ponto de controle (P01 a P16 do manual), mas so
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

## Senha do PostgreSQL

Seis dos quinze algoritmos falam com o banco e recebem a senha como parametro comum.
Na caixa de ferramentas do QGIS isso vira um campo mascarado. Na linha de comando
viraria historico do shell e linha de processo visivel a outros usuarios da maquina.

**Deixe a senha fora da linha de comando.** O CLI le a variavel de ambiente
`PTOCONTROLE_DB_PASSWORD` quando o parametro de senha nao foi informado:

```
set PTOCONTROLE_DB_PASSWORD=...
python pto_controle_cli.py run criarbanco SERVERIP=localhost PORT=5432 BDNAME=bpc USER=postgres
```

Quando a senha vem na linha de comando mesmo assim, o CLI avisa. Em toda saida
(dry-run, eco de parametros, mensagem de erro) o valor sai como `***`. O `describe`
marca esses parametros como `segredo`.

Isto e guardrail da interface, nao do plugin: o plugin continua recebendo a senha
como parametro, e quem usa a GUI nao ve diferenca.

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

- **`test_cli_contract.py`**: validacao, coercao, cache, segredo e renderizacao. Nao
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

| id | passo | rotulo no QGIS |
|---|---|---|
| `criarbanco` | P01 | 01 - Criar banco de dados |
| `validarestrutura` | P02 | 02 - Validar a estrutura de pastas |
| `atualizarbanco` | P03 | 03 - Atualizar banco de dados |
| `prepararprocessamento` | P04 | 04 - Preparar para processamento |
| `posppp` | P06 | 06 - Procedimento pos PPP |
| `atualizarbancoppprte` | P07 | 07 - Atualizar banco com dados do PPP/RTE |
| `distribuirvistas` | P08 | 08 - Distribuir vistas aereas na estrutura de pasta |
| `distribuirmonografia` | P09 | 09 - Gerar e distribuir monografias nas pastas |
| `prepararbpc` | P10 | 10 - Preparar insumos para carregamento no BPC |
| `caminhosnosatributos` | P11 | 11 - Inserir nos atributos os caminhos dos arquivos |
| `baixararquivos` | P12 | 12 - Download dos arquivos |
| `corrigirdatatrimble` | P13 | 13 - Corrigir ToW para TRIMBLE |
| `verificarcodigos` | P14 | 14 - Verificar codigos de pontos disponiveis |
| `distribuircroqui` | P15 | 15 - Distribuir croqui digital na estrutura de pasta |
| `compactarpastas` | P16 | 16 - Compactar as pastas dos pontos de controle |

Nao existe P05: e o passo externo, no site do PPP-IBGE ou num software de RTE.

## annotations.json

Conhecimento de dominio curado, por id, opcional. Entra so o que a introspecao NAO
alcanca: a ordem do fluxo, o que precisa ter rodado antes, e a armadilha que o
contrato do parametro nao conta (por exemplo, que o `atualizarbanco` APAGA a pasta
`3_Foto_Rastreio` original depois de recomprimir as fotos, ou que so se gera
monografia com orbita PPP final).

Nome, tipo e obrigatoriedade de parametro **nao entram**, porque o `describe` ja le
isso ao vivo e uma copia aqui apodreceria. Um teste faz isso valer.

## Limites conhecidos

- **Um algoritmo dos 15 foi exercitado headless de ponta a ponta** (2026-07-28): o
  `validarestrutura` (P02) rodou sobre os dados de exemplo de
  `arquivos/antes_processamento`, com exit 0 e a mensagem canonica "nao contem erros",
  conferida no arquivo de relatorio e nao so no retorno da ferramenta. Os outros 14
  seguem sem prova de execucao.
- **`distribuircroqui` e `distribuirmonografia` sao o par de maior risco.** Montam
  atlas de layout em `QgsProject.instance()` e trocam o estilo da camada durante a
  execucao. Layout headless costuma funcionar, mas nao esta provado aqui.
- **`baixararquivos` depende de selecao interativa** na camada, no canvas do QGIS.
  Sem selecao nao baixa nada, e headless nao existe canvas. Provavelmente exige
  mudanca no algoritmo para ser util por CLI.
- **`prepararbpc` chama `ogr2ogr` por subprocesso**: ele tem de estar no PATH.
- **Seis algoritmos exigem PostgreSQL alcancavel.** O `psycopg2` ja vem no Python do
  QGIS 4.0.0 (confirmado na versao 2.9.11).
