#!/usr/bin/env bash
PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ferramentas_pto_controle"
rm -rf "$DEST"
ln -s "$PLUGIN_DIR" "$DEST"
