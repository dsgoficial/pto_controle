#!/usr/bin/env bash
# Liga o plugin deste repositorio ao perfil do QGIS, para desenvolver sem copiar
# arquivo. O perfil e o QGIS4: o plugin declara qgisMinimumVersion=4.0, e apontar
# para o QGIS3 legado instala o plugin onde o QGIS 4 nao olha.
set -euo pipefail
PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins/ferramentas_pto_controle"

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
ln -s "$PLUGIN_DIR" "$DEST"

echo "Plugin ligado em $DEST"
echo "Falta habilita-lo PARA O qgis_process, que e uma habilitacao separada da do"
echo "QGIS Desktop:"
echo "    python \"$PLUGIN_DIR/pto_controle_cli/pto_controle_cli.py\" doctor --fix"
