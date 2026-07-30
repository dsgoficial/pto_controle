#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pto-controle-cli — executa os algoritmos de Processing do plugin Ponto de Controle
por linha de comando, headless, encapsulando o `qgis_process` do QGIS.

Permite descobrir os algoritmos do plugin, inspecionar os parâmetros de cada um e
executa-los, sem abrir o QGIS Desktop. A fonte da verdade e sempre o próprio
`qgis_process`, consultado ao vivo: a lista e os parâmetros estão sempre corretos e
um algoritmo novo aparece sozinho, sem nenhum catálogo pré-gerado. O arquivo
opcional `annotations.json` só acrescenta conhecimento de domínio (a ordem do fluxo,
o que precisa rodar antes) que não da para extrair do qgis_process.

Comandos
--------
  list                      Lista os algoritmos do plugin.
  describe <alg>            Mostra os parâmetros de um algoritmo.
  run <alg> [KEY=VALUE ...] Valida e executa um algoritmo.
  doctor                    Diagnostica o ambiente (qgis_process, provider carregado).
  cache                     Mostra ou limpa o cache local do contrato.

O id pode vir com ou sem o prefixo "ptocontrole:", e um prefixo do nome basta quando
identifica um algoritmo só (`describe criarbanco` ou `describe criar`).

Antes de executar, o `run` válida os parâmetros contra o contrato do próprio
algoritmo (nome inexistente, obrigatório ausente, índice de enum fora da faixa) e,
quando reprova, imprime o contrato dos parâmetros citados. O contrato vem de uma
chamada ao qgis_process, que custa segundos, então fica em cache em disco,
invalidado pela impressão digital do ambiente (ver `cache`). Escapes: `--no-check`
pula a validação e `--refresh-cache` forca reler o contrato ao vivo.

Exemplos
--------
  python pto_controle_cli.py doctor --fix
  python pto_controle_cli.py list
  python pto_controle_cli.py describe validarestrutura
  python pto_controle_cli.py run validarestrutura --dry-run \\
      FOLDER=D:\\pontos JSON=D:\\pontos\\json_validacao_estrutura_pasta.json
  python pto_controle_cli.py run criarbanco SAIDA=D:\\missoes\\missão.gpkg

Códigos de saida: 0 sucesso, 2 reprovado na validação local (nada foi executado),
qualquer outro e o código do próprio qgis_process.
"""
import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

PROVIDER = "ptocontrole"
# Nome da PASTA do plugin no perfil do QGIS, que e como o `qgis_process plugins`
# se refere a ele (não confundir com o nome de exibicao do metadata.txt).
PLUGIN_NAME = "ferramentas_pto_controle"
HERE = Path(__file__).resolve().parent
ANNOTATIONS_PATH = HERE / "annotations.json"
# Este CLI vive DENTRO do pacote do plugin, então o pacote e a pasta de cima. Como
# não tem __init__.py, o QGIS não importa esta pasta ao carregar o plugin; ela só
# viaja junto na instalação, que é o que faz o CLI estar onde o plugin estiver.
PLUGIN_DIR = HERE.parent
# Muda quando o FORMATO do arquivo de cache muda, para invalidar entradas antigas
# sem precisar limpar o cache na mao.
CACHE_FORMAT = 1
WIDTH = 92

_qgis_process_path = None  # cache (apenas resultados positivos)
_fingerprint = None  # cache em memória (o stat e barato, mas o run chama varias vezes)


# ---------------------------------------------------------------------------
# qgis_process
# ---------------------------------------------------------------------------
def _version_key(path):
    """Chave de ordenacao por versão extraida do caminho, p.ex. 'QGIS 3.40.0' deve
    vir DEPOIS de 'QGIS 3.8' (a ordenacao lexicografica de string erraria isso)."""
    return tuple(int(n) for n in re.findall(r"\d+", path)[:4])


def find_qgis_process():
    """Retorna o caminho do executavel/bat do qgis_process, ou None.

    Memoiza apenas resultados positivos: se não encontrar, volta a procurar na
    próxima chamada (evita cachear um None permanente — relevante para uso como
    módulo/testes que definem PTOCONTROLE_QGIS_PROCESS depois do import).
    """
    global _qgis_process_path
    if _qgis_process_path is not None:
        return _qgis_process_path

    # 1. Override explícito
    env = os.environ.get("PTOCONTROLE_QGIS_PROCESS")
    if env and Path(env).exists():
        _qgis_process_path = env
        return env

    # 2. PATH
    for name in ("qgis_process", "qgis_process.bin", "qgis_process-qgis.bat"):
        found = shutil.which(name)
        if found:
            _qgis_process_path = found
            return found

    # 3. Locais de instalação mais comuns
    candidates = []
    if sys.platform.startswith("win"):
        program_dirs = {
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramW6432", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        }
        for pf in filter(None, program_dirs):
            candidates += glob.glob(os.path.join(pf, "QGIS *", "bin", "qgis_process-qgis.bat"))
        for root in (r"C:\OSGeo4W", r"C:\OSGeo4W64"):
            candidates += glob.glob(os.path.join(root, "bin", "qgis_process*.bat"))
    elif sys.platform == "darwin":
        candidates += glob.glob("/Applications/QGIS*.app/Contents/MacOS/bin/qgis_process")
    else:
        candidates += ["/usr/bin/qgis_process", "/usr/local/bin/qgis_process"]
        candidates += glob.glob("/usr/lib/qgis/qgis_process*")

    # Prefere a versão mais nova (por número de versão real, não lexicografico).
    for path in sorted(set(candidates), key=_version_key, reverse=True):
        if Path(path).exists():
            _qgis_process_path = path
            return path
    return None


def _build_command(qgis_process, args):
    """Monta o comando, tratando .bat/.cmd no Windows via cmd /c."""
    if os.name == "nt" and qgis_process.lower().endswith((".bat", ".cmd")):
        return ["cmd", "/c", qgis_process, *args]
    return [qgis_process, *args]


def _qgis4_config_path():
    """Diretorio de configuracao do QGIS 4 (que contem 'profiles'), se existir.

    O qgis_process 4.0 ainda resolve o perfil legado QGIS/QGIS3 por padrão,
    enquanto o QGIS 4 Desktop usa QGIS/QGIS4 — sem redirecionar via
    QGIS_CUSTOM_CONFIG_PATH, o plugin instalado no perfil real fica invisível
    para o qgis_process (lista vazia / provider não carregado).
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA", "")
        cand = os.path.join(base, "QGIS", "QGIS4")
    elif sys.platform == "darwin":
        cand = os.path.expanduser("~/Library/Application Support/QGIS/QGIS4")
    else:
        cand = os.path.expanduser("~/.local/share/QGIS/QGIS4")
    return cand if os.path.isdir(os.path.join(cand, "profiles")) else None


def _raiz_do_qgis(qgis_process):
    """A pasta de instalacao do QGIS, deduzida do caminho do qgis_process."""
    if not qgis_process:
        return None
    return os.path.dirname(os.path.dirname(os.path.abspath(qgis_process)))


def ambiente_de_layout(qgis_process):
    """As variaveis que os passos de LAYOUT (P08, P09, P10) exigem headless.

    Sao tres, e cada uma vem de um defeito medido. Antes de 2026-07-30 elas eram
    conhecimento fora da banda: quem rodasse o P08 pelo CLI sem saber delas via a
    imagem sair errada ou a monografia estourar a celula, sem nenhuma mensagem
    dizendo o motivo. Isso quebra o padrao agent-first, que exige que o contrato
    esteja NA ferramenta.

    - `QT_QPA_PLATFORM=windows`: com `offscreen`, o Windows nao carrega a base de
      fontes. Times New Roman vira uma substituta mais larga e o texto estoura as
      celulas da monografia. So no Windows: em Linux o offscreen e o certo.
    - `PROJ_DATA` e `GDAL_DATA` apontando para o `share/` do QGIS: um `proj.db` de
      outra instalacao no PATH (o do PostgreSQL 18, no caso medido) sombreia o do
      QGIS e a reprojecao passa a errar calada.

    Devolve o dicionario a aplicar. Quem ja definiu a variavel no ambiente MANDA:
    isto e padrao, e nao imposicao.
    """
    extra = {}
    if sys.platform.startswith("win"):
        extra["QT_QPA_PLATFORM"] = "windows"
    raiz = _raiz_do_qgis(qgis_process)
    if raiz:
        # Os dois NAO ficam no mesmo lugar, e isso muda entre instalacoes. No QGIS
        # 4.2.0 do Windows o proj esta em `share/proj` e o gdal em
        # `apps/gdal/share/gdal`. Por isso a busca e por candidatos, e a chave so
        # entra quando a pasta EXISTE: apontar PROJ_DATA para pasta inexistente e
        # pior do que nao apontar, porque o proj para de achar o proprio banco.
        candidatos = {
            "PROJ_DATA": ("share/proj", "apps/proj/share/proj", "share/proj9"),
            "GDAL_DATA": ("apps/gdal/share/gdal", "share/gdal"),
        }
        for chave, opcoes in candidatos.items():
            for relativo in opcoes:
                caminho = os.path.join(raiz, *relativo.split("/"))
                if os.path.isdir(caminho):
                    extra[chave] = caminho
                    break
    return extra


def call_qgis_process(args, stdin_text=None, extra_env=None):
    """Executa o qgis_process e retorna (returncode, stdout, stderr).

    O `extra_env` traz o ambiente extra que ALGUNS passos exigem (ver
    ambiente_de_layout). Ele entra por `setdefault`: quem definiu a variavel no
    proprio ambiente continua mandando.
    """
    qgis_process = find_qgis_process()
    if qgis_process is None:
        raise SystemExit(
            "ERRO: nao encontrei o 'qgis_process'.\n"
            "  - Garanta que o QGIS 4.0+ esta instalado, ou\n"
            "  - Aponte a variavel de ambiente PTOCONTROLE_QGIS_PROCESS para o\n"
            "    caminho do qgis_process (ex.: \"C:\\\\Program Files\\\\QGIS 4.0.0\\\\bin\\\\qgis_process-qgis.bat\").\n"
            "  Rode `pto_controle_cli.py doctor` para diagnosticar."
        )

    env = dict(os.environ)
    for chave, valor in (extra_env or {}).items():
        env.setdefault(chave, valor)
    # Necessario para rodar sem servidor grafico (headless / servidores).
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    # Aponta o qgis_process para o perfil do QGIS 4 (ver _qgis4_config_path).
    if "QGIS_CUSTOM_CONFIG_PATH" not in env:
        cfg = _qgis4_config_path()
        if cfg:
            env["QGIS_CUSTOM_CONFIG_PATH"] = cfg

    proc = subprocess.run(
        _build_command(qgis_process, args),
        input=stdin_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _parse_json_stdout(stdout):
    """qgis_process imprime o JSON no stdout; o stderr leva ruido de outros plugins."""
    stdout = stdout.strip()
    if not stdout:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def full_id(alg):
    """Normaliza para 'ptocontrole:nome', SEM consultar o qgis_process."""
    alg = alg.strip()
    return alg if ":" in alg else f"{PROVIDER}:{alg}"


def _help_json(alg):
    """Retorna (help_parseado, returncode) de `qgis_process help <id> --json`."""
    code, out, _err = call_qgis_process(["help", full_id(alg), "--json"])
    return _parse_json_stdout(out), code


def load_annotations():
    """Conhecimento de domínio opcional (regras/exemplos) por id de algoritmo."""
    if not ANNOTATIONS_PATH.exists():
        return {}
    with open(ANNOTATIONS_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _summarize_help(data):
    """Reduz a saida verbosa do `qgis_process help --json` a um resumo útil."""
    details = data.get("algorithm_details", {})
    params = []
    for name, p in sorted(data.get("parameters", {}).items()):
        item = {
            "name": name,
            "type": p.get("raw_definition", {}).get("parameter_type", p.get("type", {}).get("id")),
            "description": p.get("description"),
            "required": not p.get("optional", False),
            "advanced": p.get("is_advanced", False),
            "is_output": p.get("is_destination", False),
            "default": p.get("default_value"),
        }
        if "available_options" in p:
            item["options"] = p["available_options"]
            item["note"] = "passe o indice numerico da opcao (ex.: 2)"
        params.append(item)
    outputs = [
        {"name": k, "type": v.get("type"), "description": v.get("description")}
        for k, v in data.get("outputs", {}).items()
    ]
    return {
        "id": details.get("id"),
        "display_name": details.get("name"),
        "short_description": details.get("short_description"),
        "group": details.get("group"),
        "parameters": params,
        "outputs": outputs,
    }


# ---------------------------------------------------------------------------
# Cache do contrato (help --json) e da lista, em disco
#
# Uma chamada ao qgis_process custa segundos (o QGIS inteiro sobe a cada vez),
# então validar o `run` contra o contrato ao vivo dobraria o custo de toda
# execução. O contrato só muda quando o QGIS ou o plugin mudam, logo cabe em
# cache com uma impressão digital barata (stat, sem ler arquivo).
# ---------------------------------------------------------------------------
def _stat_token(path):
    """Assinatura barata de um caminho: mtime + tamanho, ou '-' se não existir."""
    try:
        st = os.stat(path)
    except OSError:
        return "-"
    return f"{st.st_mtime_ns}.{st.st_size}"


def env_fingerprint():
    """Impressão digital do ambiente que produz o contrato.

    Cobre o executavel do qgis_process (troca de versão do QGIS) e a pasta do
    plugin com o metadata.txt (troca de versão/instalação do plugin). NÃO cobre a
    edicao de um .py de algoritmo lá dentro, porque varrer a árvore a cada `run`
    custaria mais do que economiza: em desenvolvimento do plugin, use
    `--refresh-cache` ou `cache --clear` depois de mexer na assinatura de um
    algoritmo.
    """
    global _fingerprint
    if _fingerprint is not None:
        return _fingerprint
    qp = find_qgis_process() or "-"
    parts = [
        str(CACHE_FORMAT),
        qp,
        _stat_token(qp),
        str(PLUGIN_DIR),
        _stat_token(PLUGIN_DIR),
        _stat_token(PLUGIN_DIR / "metadata.txt"),
    ]
    _fingerprint = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return _fingerprint


def cache_dir():
    """Pasta do cache; PTOCONTROLE_CLI_CACHE permite isolar (testes, CI, tmp read-only)."""
    override = os.environ.get("PTOCONTROLE_CLI_CACHE")
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / "pto_controle_cli_cache"


def _cache_file(chave):
    # O id tem ':', que não é nome de arquivo válido no Windows.
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", chave)
    return cache_dir() / f"{safe}.json"


def cache_read(chave):
    """Entrada em cache e ainda válida, ou None."""
    try:
        with open(_cache_file(chave), encoding="utf-8") as fh:
            entry = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None
    if entry.get("fingerprint") != env_fingerprint():
        return None
    return entry.get("help")


def cache_write(chave, data):
    """Grava a entrada. Falha de escrita nunca derruba o comando: o cache e
    otimização, e um /tmp somente-leitura não pode impedir de rodar o algoritmo."""
    path = _cache_file(chave)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Escrita atômica: dois `run` simultaneos não podem deixar um JSON pela metade.
        tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(
                {"fingerprint": env_fingerprint(), "chave": chave, "help": data},
                fh,
                ensure_ascii=False,
            )
        os.replace(tmp, path)
    except OSError:
        pass


def help_json_cached(alg, refresh=False):
    """Contrato do algoritmo. Retorna (help, returncode, veio_do_cache)."""
    chave = full_id(alg)
    if not refresh:
        cached = cache_read(chave)
        if cached is not None:
            return cached, 0, True
    data, code = _help_json(alg)
    if data is not None:
        cache_write(chave, data)
    return data, code, False


# ---------------------------------------------------------------------------
# Resolucao do id do algoritmo
#
# Os ids seguem a regra do QGIS (alfanumerico minusculo, sem separador), o que os
# deixa compridos e grudados. Em vez de manter um mapa de apelidos (que seria um
# catálogo copiado, exatamente o que este desenho existe para evitar), a
# resolucao por prefixo consulta a LISTA VIVA: um nome novo entra sozinho.
# ---------------------------------------------------------------------------
def list_algorithms(refresh=False):
    """{id_curto: nome_de_exibicao} do provider, ao vivo (com cache)."""
    chave = f"{PROVIDER}__list"
    if not refresh:
        cached = cache_read(chave)
        if cached is not None:
            return cached
    code, out, _err = call_qgis_process(["list", "--json"])
    data = _parse_json_stdout(out)
    if data is None:
        raise SystemExit(f"Falha ao listar os algoritmos (exit {code}).")
    algs = data.get("providers", {}).get(PROVIDER, {}).get("algorithms", {})
    tabela = {k.split(":", 1)[-1]: v.get("name", "") for k, v in algs.items()}
    if tabela:
        cache_write(chave, tabela)
    return tabela


def resolve_alg(alg, refresh=False):
    """Resolve o que o usuário digitou para um id completo 'ptocontrole:nome'.

    Ordem: id exato (não custa consulta), depois prefixo único contra a lista viva,
    depois substring única. Ambiguidade e erro, nunca escolha silenciosa.
    """
    alg = alg.strip()
    if ":" in alg:
        return alg

    # Caminho feliz: o contrato já esta em cache com esse nome exato, então nem
    # precisa da lista (que custaria mais uma subida do QGIS).
    if cache_read(full_id(alg)) is not None:
        return full_id(alg)

    tabela = list_algorithms(refresh=refresh)
    if not tabela:
        # Sem lista não da para resolver; deixa o qgis_process dar o erro dele.
        return full_id(alg)
    if alg in tabela:
        return full_id(alg)

    alvo = alg.lower()
    for criterio, casa in (
        ("prefixo", lambda n: n.startswith(alvo)),
        ("trecho", lambda n: alvo in n),
    ):
        achados = sorted(n for n in tabela if casa(n))
        if len(achados) == 1:
            print(f"[{criterio}] {alg} -> {achados[0]}", file=sys.stderr)
            return full_id(achados[0])
        if len(achados) > 1:
            raise SystemExit(
                f"ERRO: '{alg}' casa com {len(achados)} algoritmos: {', '.join(achados)}.\n"
                "  Desambigue passando mais letras."
            )

    perto = difflib.get_close_matches(alvo, list(tabela), n=3, cutoff=0.5)
    msg = f"ERRO: nao achei o algoritmo '{alg}' no provider {PROVIDER}."
    if perto:
        msg += f"\n  Talvez: {', '.join(perto)}"
    msg += "\n  Lista completa: pto_controle_cli.py list"
    raise SystemExit(msg)


# ---------------------------------------------------------------------------
# Contrato: formatacao legível e validação local
# ---------------------------------------------------------------------------
def _param_type(param):
    return (
        param.get("raw_definition", {}).get("parameter_type")
        or param.get("type", {}).get("id")
        or "?"
    )


def _param_marks(param):
    marks = ["opcional" if param.get("optional", False) else "obrigatorio"]
    if param.get("is_destination"):
        marks.append("saida")
    if param.get("is_advanced"):
        marks.append("avancado")
    return ",".join(marks)


def _options_line(param):
    """'0=Paisagem  1=Retrato' para enum por índice, ou os rótulos aceitos quando o
    enum usa string estatica. None se o parâmetro não for enumerado."""
    options = param.get("available_options")
    if not options:
        return None
    if param.get("raw_definition", {}).get("uses_static_strings"):
        return "valores: " + "  ".join(str(v) for v in options.values())
    pairs = "  ".join(f"{k}={v}" for k, v in sorted(options.items(), key=_option_sort_key))
    return f"opcoes (passe o indice): {pairs}"


def _option_sort_key(item):
    key = item[0]
    return (int(key), "") if str(key).lstrip("-").isdigit() else (0, str(key))


def _tem_padrao(param):
    """O contrato traz um padrao UTILIZAVEL para este parametro?

    String vazia NAO conta. Varios algoritmos deste plugin declaram
    `defaultValue=''` em parametro de pasta ou de camada, e o motor nao consegue
    fazer nada com isso: tratar como padrao valido deixaria passar a invocacao que
    falharia adiante, com mensagem pior. O `"C:"` do P08 conta como padrao, e e
    ruim por outro motivo, mas ai a escolha e de quem escreveu o algoritmo.
    """
    default = param.get("default_value")
    if default is None:
        return False
    if isinstance(default, str) and not default.strip():
        return False
    return True


def format_param(name, param, indent="  "):
    """Uma linha por parâmetro (mais continuacoes para padrão e opcoes)."""
    head = f"{indent}{name:<26} {_param_type(param):<10} {_param_marks(param):<22}"
    desc = param.get("description") or ""
    lines = [f"{head} {desc}".rstrip()]
    default = param.get("default_value")
    if default is not None:
        lines.append(f"{indent}      padrao: {json.dumps(default, ensure_ascii=False)}")
    options = _options_line(param)
    if options:
        lines += textwrap.wrap(
            options,
            width=WIDTH,
            initial_indent=indent + "      ",
            subsequent_indent=indent + "              ",
        )
    return "\n".join(lines)


def _param_sort_key(item):
    """Obrigatorios de entrada primeiro, depois as saidas obrigatórias, depois os
    opcionais: e a ordem em que um chamador precisa decidir o que passar."""
    name, param = item
    return (bool(param.get("optional", False)), bool(param.get("is_destination")), name)


def _enum_indices(value):
    """Indices de um valor de enum ('1', 1, '1,3', [1, 3]) ou None se não for índice."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return [value]
    if isinstance(value, (list, tuple)):
        items = value
    elif isinstance(value, str):
        items = value.split(",")
    else:
        return None
    out = []
    for item in items:
        text = str(item).strip()
        if not re.fullmatch(r"-?\d+", text):
            return None
        out.append(int(text))
    return out or None


def validate_inputs(inputs, help_data):
    """Confere os parâmetros contra o contrato do algoritmo, sem executar nada.

    Devolve uma lista de {"message", "params"}. Só checa o que da para afirmar com
    certeza a partir do contrato; um enum de string estatica, por exemplo, fica de
    fora, porque reprovar por engano e pior do que deixar o qgis_process reclamar.
    """
    params = help_data.get("parameters", {})
    errors = []

    # 1. Nome que não existe. E o modo de falha mais traicoeiro: o qgis_process
    # IGNORA a chave desconhecida em silêncio, aplica o padrão do parâmetro que o
    # chamador queria setar e o erro só aparece lá na frente, com outra cara.
    for key in inputs:
        if key in params:
            continue
        close = difflib.get_close_matches(key, list(params), n=2, cutoff=0.6)
        message = f"parametro inexistente: {key}"
        if close:
            message += f" (talvez: {', '.join(close)})"
        errors.append({"message": message, "params": close})

    # 2. Obrigatorio ausente. Vale também para saidas (sink/fileDestination): o
    # qgis_process não inventa destino temporario, ele aborta.
    #
    # Obrigatorio COM padrao no contrato não se cobra: o motor aplica o padrao
    # sozinho quando a chave falta. Cobrar era ser mais estrito do que o motor sem
    # ganho nenhum, e obrigava quem invoca a repetir 'dpi=300 escala_satelite=500'
    # em todo comando, valores que o proprio contrato ja anuncia. Medido em
    # 2026-07-30: o P09 tem dois parametros avancados assim, e a validacao local
    # reprovava a invocacao minima que o motor aceitaria.
    for name, param in sorted(params.items(), key=_param_sort_key):
        if param.get("optional", False):
            continue
        if _tem_padrao(param) and not param.get("is_destination"):
            continue
        if name not in inputs or inputs[name] is None:
            errors.append({
                "message": f"parametro obrigatorio ausente: {name}",
                "params": [name],
            })

    # 3. Enum por índice: fora da faixa, ou rótulo passado no lugar do índice.
    for name, value in inputs.items():
        param = params.get(name)
        if not param:
            continue
        options = param.get("available_options")
        if not options or param.get("raw_definition", {}).get("uses_static_strings"):
            continue
        valid = {int(k) for k in options if str(k).lstrip("-").isdigit()}
        indices = _enum_indices(value)
        if indices is None:
            label = {str(v).lower(): k for k, v in options.items()}.get(str(value).lower())
            message = f"{name}: valor {value!r} nao e indice de opcao"
            if label is not None:
                message += f" (o indice de {value!r} e {label})"
            errors.append({"message": message, "params": [name]})
            continue
        fora = [i for i in indices if i not in valid]
        if fora:
            errors.append(
                {
                    "message": f"{name}: indice {', '.join(map(str, fora))} fora da faixa",
                    "params": [name],
                }
            )
    return errors


def format_validation_errors(alg, errors, help_data):
    """Mensagem de reprovação: o contrato dos parâmetros citados vem JUNTO, para
    o chamador poder corrigir sem uma segunda chamada (que custaria segundos)."""
    params = help_data.get("parameters", {})
    out = [f"ERRO: {len(errors)} problema(s) de validacao em {alg} (nada foi executado).", ""]
    for n, err in enumerate(errors, 1):
        out.append(f"  [{n}] {err['message']}")
        for name in err.get("params") or []:
            if name in params:
                out.append(format_param(name, params[name], indent="      "))
    known = ", ".join(sorted(params))
    out.append("")
    out += textwrap.wrap(
        f"Parametros de {alg}: {known}",
        width=WIDTH,
        initial_indent="  ",
        subsequent_indent="    ",
    )
    out.append(f"  Contrato completo: describe {alg}")
    out.append("  Para pular esta checagem: --no-check")
    return "\n".join(out) + "\n"


def render_describe(help_data, annotation):
    """Saida compacta do describe: uma linha por parâmetro, mais o que só a prosa
    curada sabe (regra de domínio e exemplo)."""
    details = help_data.get("algorithm_details", {})
    params = help_data.get("parameters", {})
    alg = details.get("id") or "?"
    out = [f"{alg}  |  {details.get('name', '')}  |  grupo: {details.get('group', '')}"]

    # A descrição VIVA, que sai do shortDescription() do próprio algoritmo. Ela vem
    # antes da prosa curada porque é a que acompanha o plugin sozinha. Atenção: o
    # `qgis_process help --json` NÃO expoe o shortHelpString(), que é o help longo
    # do painel do QGIS, então o único canal vivo de descrição e este.
    if details.get("short_description"):
        out += ["", textwrap.fill(details["short_description"], width=WIDTH)]
    if annotation.get("description"):
        out += ["", textwrap.fill(annotation["description"], width=WIDTH)]

    required = sum(1 for p in params.values() if not p.get("optional", False))
    out += ["", f"Parametros ({required} obrigatorio(s), {len(params) - required} opcional(is)):"]
    for name, param in sorted(params.items(), key=_param_sort_key):
        out.append(format_param(name, param))

    # Só as saidas que NÃO são parâmetro (a saida-destino já saiu acima, marcada
    # como 'saida'; repeti-lá aqui seria dizer duas vezes a mesma coisa).
    extras = {k: v for k, v in help_data.get("outputs", {}).items() if k not in params}
    if extras:
        out += ["", "Saidas adicionais (nao sao parametro):"]
        for name, info in sorted(extras.items()):
            out.append(f"  {name:<26} {info.get('type', ''):<16} {info.get('description', '')}".rstrip())

    rules = annotation.get("constraints") or []
    if rules:
        out += ["", "Regras (curadas):"]
        for rule in rules:
            out += textwrap.wrap(rule, width=WIDTH, initial_indent="  - ", subsequent_indent="    ")

    example = annotation.get("example")
    if example:
        out += ["", "Exemplo:", f"  python pto_controle_cli.py run {alg} {_example_args(example)}"]
    return "\n".join(out)


def _example_args(example):
    """Transforma o exemplo curado ({'KEY': valor}) em tokens KEY=VALUE prontos."""
    tokens = []
    for key, value in example.items():
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        tokens.append(f'"{key}={text}"' if " " in text else f"{key}={text}")
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------
def _quote(path):
    return f'"{path}"' if " " in str(path) else str(path)


def _print_enable_fix(qp):
    """Imprime o conserto do plugin desabilitado.

    O comando só vale se rodar no MESMO perfil que este CLI usa: o qgis_process
    resolve o perfil legado (QGIS3) por padrão, enquanto o CLI redireciona para o
    perfil do QGIS 4. Rodar o enable sem essa variavel habilita o plugin no perfil
    errado e o CLI continua sem provider, sem sinal nenhum de que nada mudou.
    """
    cfg = os.environ.get("QGIS_CUSTOM_CONFIG_PATH") or _qgis4_config_path()
    print(f"    conserto: {_quote(qp)} plugins enable {PLUGIN_NAME}")
    if cfg:
        setter = f'set QGIS_CUSTOM_CONFIG_PATH={cfg}' if os.name == "nt" \
            else f'export QGIS_CUSTOM_CONFIG_PATH="{cfg}"'
        print(f"              (antes, no mesmo terminal: {setter})")
    print("    ou, ja no perfil certo: python pto_controle_cli.py doctor --fix")


def _check_provider(qp, fix=False):
    """Confere se o provider ptocontrole esta carregado NO qgis_process e, quando
    não esta, devolve o conserto exato.

    Este e o modo de falha real: o qgis_process mantem a própria lista de plugins
    habilitados, separada da do QGIS Desktop. Com o plugin ativo no Desktop e
    inativo aqui, `list` retorna zero algoritmos com exit 0 e stderr vazio, ou
    seja, o CLI fica inútil sem reclamar de nada.
    """
    problems = []
    code, out, err = call_qgis_process(["plugins", "--json"])
    plugins = (_parse_json_stdout(out) or {}).get("plugins")
    if plugins is None:
        print(f"  plugins         : nao consegui ler (exit {code})")
        if err.strip():
            print(f"    stderr: {err.strip().splitlines()[0]}")
        problems.append("nao foi possivel consultar os plugins do qgis_process")
        return problems
    entry = plugins.get(PLUGIN_NAME)
    if entry is None:
        print(f"  plugin {PLUGIN_NAME}: NAO INSTALADO no perfil visto pelo qgis_process")
        print(f"    plugins vistos: {', '.join(sorted(plugins)) or '(nenhum)'}")
        print("    conserto: instale o plugin no perfil (ver QGIS_CUSTOM_CONFIG_PATH acima);")
        print(f"              em desenvolvimento, um link de {PLUGIN_DIR}")
        print("              para <perfil>/python/plugins.")
        problems.append(f"plugin {PLUGIN_NAME} ausente")
        return problems
    if not entry.get("loaded"):
        print(f"  plugin {PLUGIN_NAME}: instalado, mas NAO habilitado para o qgis_process")
        print("    (o qgis_process tem lista de plugins propria, independente do QGIS Desktop)")
        _print_enable_fix(qp)
        if not fix:
            problems.append(f"plugin {PLUGIN_NAME} nao habilitado no qgis_process")
            return problems
        print("    --fix: habilitando agora...")
        code, _out, err = call_qgis_process(["plugins", "enable", PLUGIN_NAME])
        if code != 0:
            print(f"    falhou (exit {code}): {err.strip().splitlines()[:1]}")
            problems.append("nao consegui habilitar o plugin")
            return problems
        print("    habilitado.")
    else:
        print(f"  plugin {PLUGIN_NAME}: habilitado e carregado")

    code, out, err = call_qgis_process(["list", "--json"])
    algs = (_parse_json_stdout(out) or {}).get("providers", {}).get(PROVIDER, {}).get("algorithms", {})
    if not algs:
        print(f"  provider {PROVIDER}: CARREGOU 0 ALGORITMOS (exit {code})")
        print("    o plugin subiu mas nao registrou o provider: quase sempre um erro de import.")
        print(f"    conserto: rode {_quote(qp)} list e leia o stderr, que traz o traceback.")
        if err.strip():
            print(f"    stderr (1a linha): {err.strip().splitlines()[0]}")
        problems.append("provider carregou 0 algoritmos")
    else:
        print(f"  provider {PROVIDER}: {len(algs)} algoritmos")
    return problems


def cmd_doctor(args):
    qp = find_qgis_process()
    print("pto-controle-cli doctor")
    print("-----------------------")
    print(f"  qgis_process    : {qp or 'NAO ENCONTRADO'}")
    print(f"  pasta do plugin : {PLUGIN_DIR} ({'existe' if PLUGIN_DIR.is_dir() else 'AUSENTE'})")
    print(f"  annotations.json: {'ok' if ANNOTATIONS_PATH.exists() else 'ausente (opcional)'}")
    print(f"  QT_QPA_PLATFORM (sera definido como) : "
          f"{os.environ.get('QT_QPA_PLATFORM', 'offscreen')}")
    cfg = os.environ.get("QGIS_CUSTOM_CONFIG_PATH") or _qgis4_config_path()
    print(f"  QGIS_CUSTOM_CONFIG_PATH (sera definido como) : {cfg or '(padrao do qgis_process)'}")
    if qp is None:
        print(f"\n  Defina PTOCONTROLE_QGIS_PROCESS apontando para o qgis_process.")
        return 1
    code, out, err = call_qgis_process(["--version"])
    first = (out or err).strip().splitlines()
    print(f"  versao          : {first[0] if first else '??'} (exit {code})")
    print(f"  cache do contrato: {cache_dir()} ({_cache_counts()[0]} entrada(s) validas)")

    # O ambiente EXTRA dos passos de layout (P08, P09, P10). O CLI o aplica
    # sozinho, e o doctor o mostra porque, quando a monografia sai com texto
    # estourando a celula ou a reprojecao erra, e aqui que se olha primeiro.
    extra = ambiente_de_layout(qp)
    if extra:
        print("  ambiente dos passos de layout (aplicado so no P08, P09 e P10):")
        for chave in sorted(extra):
            fixado = os.environ.get(chave)
            origem = ' (ja fixado no ambiente, este manda)' if fixado else ''
            print(f"    {chave} = {fixado or extra[chave]}{origem}")
    else:
        print("  ambiente dos passos de layout: NADA A APLICAR")
        print("    sem o share/proj e o share/gdal ao lado do qgis_process, um proj.db")
        print("    de outra instalacao no PATH pode sombrear o do QGIS.")

    problems = _check_provider(qp, fix=args.fix)
    if problems:
        print("\n  RESULTADO: o CLI NAO vai funcionar. " + "; ".join(problems) + ".")
        return 1
    print("\n  RESULTADO: ambiente ok.")
    return 0


def _cache_counts():
    """(válidas, obsoletas) no cache, sem falhar se a pasta nem existir."""
    valid = stale = 0
    try:
        files = sorted(cache_dir().glob("*.json"))
    except OSError:
        return 0, 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                entry = json.load(fh)
        except (OSError, json.JSONDecodeError):
            stale += 1
            continue
        if entry.get("fingerprint") == env_fingerprint():
            valid += 1
        else:
            stale += 1
    return valid, stale


def cmd_cache(args):
    directory = cache_dir()
    if args.clear:
        removed = 0
        for path in directory.glob("*.json"):
            try:
                path.unlink()
                removed += 1
            except OSError:
                pass
        print(f"Cache limpo: {removed} entrada(s) removida(s) de {directory}")
        return 0
    valid, stale = _cache_counts()
    print("Cache do contrato (help --json) e da lista de algoritmos")
    print(f"  pasta           : {directory}")
    print(f"  existe          : {'sim' if directory.is_dir() else 'nao (sera criada no 1o uso)'}")
    print(f"  impressao digital: {env_fingerprint()}")
    print(f"  entradas        : {valid} validas, {stale} obsoletas")
    print("\nLimpar: cache --clear   |   Atualizar um algoritmo: describe <alg> --refresh-cache")
    return 0


def cmd_list(args):
    tabela = list_algorithms(refresh=args.refresh_cache)
    rows = sorted(tabela.items())
    if args.json:
        print(json.dumps({"algorithms": [k for k, _ in rows]}, indent=2, ensure_ascii=False))
        return 0
    if not rows:
        # Zero algoritmos com exit 0 e o sintoma de provider não carregado, não de
        # um plugin sem algoritmos: aponta o diagnostico em vez de calar.
        print("Nenhum algoritmo do Ponto de Controle disponivel (o provider nao carregou).")
        print("Rode `pto_controle_cli.py doctor` para ver o conserto exato.")
        return 1
    print(f"Algoritmos do Ponto de Controle — {len(rows)} disponiveis:\n")
    for nome, rotulo in rows:
        print(f"  {PROVIDER}:{nome:<24} {rotulo}")
    print("\nUse `describe <id>` para ver os parametros, ou `run <id> KEY=VALUE ...` para executar.")
    print("Um prefixo do nome basta, desde que identifique um algoritmo so.")
    return 0


def cmd_describe(args):
    alg = resolve_alg(args.algorithm, refresh=args.refresh_cache)
    data, code, _cached = help_json_cached(alg, refresh=args.refresh_cache)
    if data is None:
        raise SystemExit(f"Falha ao descrever {alg} (exit {code}).")
    annotation = load_annotations().get(data.get("algorithm_details", {}).get("id"), {})
    if not args.json:
        print(render_describe(data, annotation))
        return 0
    summary = _summarize_help(data)
    # Enriquece com o conhecimento de domínio curado, se houver para este id.
    for key in ("description", "constraints", "example"):
        if key in annotation:
            summary[key] = annotation[key]
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


_INT_RE = re.compile(r"^-?[1-9][0-9]*$|^0$")
_FLOAT_RE = re.compile(r"^-?[0-9]+\.[0-9]+$")


def _coerce(value):
    """Converte tokens 'KEY=VALUE' em número apenas quando e seguro; senao, string.

    Só coage inteiros "limpos" (sem zero a esquerda, sem '_', sem 'inf'/'nan', sem
    notacao exponencial ou hex) e floats decimais simples — assim não corrompe
    strings numericas como '007', '1_000', 'inf' ou identificadores. Para forcar
    um valor numérico a permanecer string, use --params/--stdin (o JSON preserva os tipos).
    """
    if _INT_RE.match(value):
        return int(value)
    if _FLOAT_RE.match(value):
        return float(value)
    return value


_BOOL_VERDADE = {"true", "1", "yes", "sim", "t", "y"}
_BOOL_FALSIDADE = {"false", "0", "no", "nao", "não", "f", "n"}


def coagir_por_contrato(inputs, help_data):
    """Ajusta os tokens KEY=VALUE ao TIPO que o contrato declara.

    O `_coerce` roda antes de existir contrato, então ele só sabe distinguir número
    de texto. Booleano fica de fora, e um `IGN_PROC=false` viraria a string 'false',
    que e não-vazia e portanto VERDADEIRA. O parâmetro faria o oposto do pedido, sem
    erro nenhum. E o mesmo modo de falha da chave desconhecida: silencioso.

    Só mexe em string. Quem passou o valor por --params/--stdin já tem o tipo JSON
    nativo e não precisa de adivinhacao.
    """
    erros = []
    params = (help_data or {}).get("parameters", {})
    for nome, valor in list(inputs.items()):
        param = params.get(nome)
        if not param or not isinstance(valor, str):
            continue
        if _param_type(param) != "boolean":
            continue
        texto = valor.strip().lower()
        if texto in _BOOL_VERDADE:
            inputs[nome] = True
        elif texto in _BOOL_FALSIDADE:
            inputs[nome] = False
        else:
            erros.append(
                {
                    "message": f"{nome}: {valor!r} nao e booleano (use true ou false)",
                    "params": [nome],
                }
            )
    return erros


def _unwrap_inputs(data):
    """Aceita {"inputs": {...}} ou {...} diretamente; exige um objeto JSON (dict)."""
    if not isinstance(data, dict):
        raise SystemExit("JSON de parametros invalido: esperado um objeto JSON.")
    if "inputs" in data:
        inner = data["inputs"]
        if not isinstance(inner, dict):
            raise SystemExit('JSON de parametros invalido: a chave "inputs" deve ser um objeto.')
        return inner
    return data


def _load_json_file(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise SystemExit(f"Arquivo de parametros nao encontrado: {path}")
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Falha ao ler JSON de '{path}': {exc}")


def _collect_inputs(args):
    inputs = {}
    if args.params:
        inputs.update(_unwrap_inputs(_load_json_file(args.params)))
    if args.stdin:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Falha ao ler JSON do stdin: {exc}")
        inputs.update(_unwrap_inputs(data))
    for token in args.params_kv:
        if "=" not in token:
            raise SystemExit(f"Parametro invalido '{token}'. Use KEY=VALUE.")
        key, value = token.split("=", 1)
        inputs[key.strip()] = _coerce(value)
    return inputs


def render_dry_run(alg, inputs, help_data):
    """Mostra exatamente o que seria executado, sem executar."""
    payload = json.dumps({"inputs": inputs}, ensure_ascii=False)
    out = [
        f"[dry-run] {alg} (nada foi executado)",
        f"  comando : qgis_process run {alg} -   (parametros pelo stdin)",
        f"  binario : {find_qgis_process() or 'NAO ENCONTRADO'}",
        "  stdin   : " + payload,
        "",
        f"  Parametros ({len(inputs)}):",
    ]
    params = (help_data or {}).get("parameters", {})
    for key in sorted(inputs):
        value = json.dumps(inputs[key], ensure_ascii=False)
        rotulo = ""
        param = params.get(key)
        if param and param.get("available_options"):
            # Traduz o índice de volta ao rótulo: e a checagem que o chamador
            # não tem como fazer de cabeca, e o erro silencioso mais comum.
            rotulo = param["available_options"].get(str(inputs[key]), "")
            rotulo = f"   -> {rotulo}" if rotulo else ""
        out.append(f"    {key:<26} = {value}{rotulo}")
    if params:
        omitidos = [n for n, p in params.items() if n not in inputs]
        if omitidos:
            out.append(f"  Omitidos (opcionais): {', '.join(sorted(omitidos))}")
        out.append("  Validacao: ok")
    else:
        out.append("  Validacao: NAO conferida (sem contrato disponivel)")
    return "\n".join(out)


def cmd_run(args):
    inputs = _collect_inputs(args)
    alg = resolve_alg(args.algorithm, refresh=args.refresh_cache)

    # Valida ANTES de gastar a execução. O contrato sai do cache em disco, então o
    # custo tipico e de milissegundos, não de uma segunda subida do QGIS.
    help_data = None
    if not args.no_check:
        help_data, code, _cached = help_json_cached(alg, refresh=args.refresh_cache)
        if help_data is None:
            # Sem contrato não da para validar. Abortar aqui esconderia o erro real
            # do qgis_process, então avisa e segue: a validação e rede, não portao.
            print(
                f"AVISO: nao consegui obter o contrato de {alg} (exit {code}); "
                "seguindo sem validar. Se repetir, rode `pto_controle_cli.py doctor`.",
                file=sys.stderr,
            )

    if help_data is not None:
        # A coerção por tipo vem ANTES da validação: e ela que transforma a string
        # 'false' no booleano false, é o que for validado tem de ser o que será enviado.
        errors = coagir_por_contrato(inputs, help_data)
        errors += validate_inputs(inputs, help_data)
        if errors:
            sys.stderr.write(format_validation_errors(alg, errors, help_data))
            return 2

    if args.dry_run:
        print(render_dry_run(alg, inputs, help_data))
        return 0

    payload = json.dumps({"inputs": inputs})
    # O passo que monta LAYOUT precisa de tres variaveis de ambiente proprias (ver
    # ambiente_de_layout). Quem decide se este e um desses passos e o GRUPO do
    # contrato vivo, e nao uma lista de ids escrita aqui: lista copiada apodrece no
    # dia em que outro passo de layout entrar.
    extra_env = None
    if (help_data or {}).get("group", "").lower().find("documentar") >= 0:
        extra_env = ambiente_de_layout(find_qgis_process())
        if extra_env:
            print("Passo de layout: aplicando " + ", ".join(sorted(extra_env)),
                  file=sys.stderr)
    code, out, err = call_qgis_process(["run", alg, "-"], stdin_text=payload,
                                       extra_env=extra_env)
    data = _parse_json_stdout(out)

    if args.raw or data is None:
        if out:
            print(out)
        if err.strip():
            sys.stderr.write(err)
        return code

    # O returncode do qgis_process e a fonte da verdade de sucesso/falha.
    results = data.get("results")
    if results is not None:
        print(json.dumps({"results": results, "inputs": inputs}, indent=2, ensure_ascii=False))
        if code == 0:
            for key, value in results.items():
                print(f"\n[OK] {key} -> {value}", file=sys.stderr)
    else:
        # Sucesso sem 'results' (ex.: algoritmos de efeito colateral) também e válido.
        print(json.dumps(data, indent=2, ensure_ascii=False))
    if err.strip():
        sys.stderr.write(err)
    return code


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pto_controle_cli.py",
        description="Executa os algoritmos do plugin Ponto de Controle por linha de comando (headless).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="Lista os algoritmos disponiveis.")
    p_list.add_argument("--json", action="store_true", help="Saida em JSON.")
    p_list.add_argument("--refresh-cache", action="store_true",
                        help="Rele a lista ao vivo, ignorando o cache.")
    p_list.set_defaults(func=cmd_list)

    p_desc = sub.add_parser("describe", help="Mostra os parametros de um algoritmo.")
    p_desc.add_argument("algorithm", help="Id ou prefixo do nome (com ou sem 'ptocontrole:').")
    p_desc.add_argument("--json", action="store_true", help="Saida em JSON (para encadear).")
    p_desc.add_argument("--refresh-cache", action="store_true",
                        help="Rele o contrato ao vivo, ignorando o cache.")
    p_desc.set_defaults(func=cmd_describe)

    p_run = sub.add_parser("run", help="Valida e executa um algoritmo.")
    p_run.add_argument("algorithm", help="Id ou prefixo do nome (com ou sem 'ptocontrole:').")
    p_run.add_argument("params_kv", nargs="*", metavar="KEY=VALUE", help="Parametros de entrada.")
    p_run.add_argument("--params", metavar="FILE", help="Arquivo JSON com os parametros.")
    p_run.add_argument("--stdin", action="store_true", help="Le os parametros (JSON) do stdin.")
    p_run.add_argument("--raw", action="store_true", help="Imprime o JSON cru do qgis_process.")
    p_run.add_argument("--dry-run", action="store_true",
                       help="Valida e mostra o que seria executado, sem executar.")
    p_run.add_argument("--no-check", action="store_true",
                       help="Pula a validacao local dos parametros.")
    p_run.add_argument("--refresh-cache", action="store_true",
                       help="Rele o contrato ao vivo antes de validar.")
    p_run.set_defaults(func=cmd_run)

    p_doc = sub.add_parser("doctor", help="Diagnostica o ambiente.")
    p_doc.add_argument("--fix", action="store_true",
                       help="Habilita o plugin no qgis_process quando for esse o problema.")
    p_doc.set_defaults(func=cmd_doctor)

    p_cache = sub.add_parser("cache", help="Mostra ou limpa o cache do contrato.")
    p_cache.add_argument("--clear", action="store_true", help="Apaga as entradas do cache.")
    p_cache.set_defaults(func=cmd_cache)

    return parser


def main(argv=None):
    # Garante saída UTF-8 (descrições e rótulos têm acentos) independentemente da
    # codificação padrão do console/plataforma.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
