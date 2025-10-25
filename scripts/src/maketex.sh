#!/bin/bash
set -euo pipefail

# choose main file
if [[ $# -eq 1 ]]; then MAIN_FILE="$1"
else
  shopt -s nullglob
  TEX_FILES=(*.tex)
  [[ ${#TEX_FILES[@]} -eq 1 ]] && MAIN_FILE="${TEX_FILES[0]}" || { echo "Specify main .tex"; exit 1; }
fi

latexmk -pdf -interaction=nonstopmode -halt-on-error "$MAIN_FILE"

# optional: clean auxiliaries but keep PDF
latexmk -c

