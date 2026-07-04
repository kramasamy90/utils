#!/bin/bash

FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_DIR="$( cd "$FILE_DIR/.." &> /dev/null && pwd )"
CONFIG_FILE="$REPO_DIR/config.yaml"

INSTALL_DIR=$(grep "INSTALL_DIR" "$CONFIG_FILE" | sed -E 's/INSTALL_DIR:\s+(.*)/\1/')

cp "$FILE_DIR/src/o.sh" "$INSTALL_DIR/open/src/o"
cp "$FILE_DIR/src/open.py" "$INSTALL_DIR/open/src/open.py"
cp "$FILE_DIR/data/help.txt" "$INSTALL_DIR/open/data/help.txt"
