#!/usr/bin/python3
import os
import sys
from global_vars import DATA_DIR 

# Preamble.
WORKING_DIR = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.realpath(os.path.join(WORKING_DIR, '../../config.yaml'))
CONFIG_DIR = os.path.realpath(os.path.join(DATA_DIR, 'configs'))
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)


# Backup vscode related settings.
VSCODE_DIR = os.path.realpath(os.path.join(CONFIG_DIR, 'vscode'))
if not os.path.exists(VSCODE_DIR):
    os.makedirs(VSCODE_DIR)
os.system(f"cp ~/.config/Code/User/keybindings.json {VSCODE_DIR}/")
os.system(f"cp ~/.config/Code/User/settings.json {VSCODE_DIR}/")
os.system(f"rsync -av ~/.config/Code/User/snippets {VSCODE_DIR}")

# TODO: vimrc. 