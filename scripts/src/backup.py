#!/usr/bin/python3
import os
import sys

FILE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(FILE_DIR, '..', '..'))

from global_vars import data_dir 

# preamble.
CONFIG_DIR = os.path.realpath(os.path.join(data_dir, 'configs'))
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Backup vscode related settings.
VSCODE_DIR = os.path.realpath(os.path.join(CONFIG_DIR, 'vscode'))
if not os.path.exists(VSCODE_DIR):
    os.makedirs(VSCODE_DIR)
os.system(f"cp ~/.config/Code/User/keybindings.json {VSCODE_DIR}/")
os.system(f"cp ~/.config/Code/User/settings.json {VSCODE_DIR}/")
os.system(f"rsync -av ~/.config/Code/User/snippets {VSCODE_DIR}")

# Back open related data.
OPEN_DIR = os.path.realpath(os.path.join(CONFIG_DIR, 'open'))

# TODO: vimrc. 