#!/usr/bin/python3
import os
import sys

FILE_DIR = os.path.realpath(os.path.dirname(__file__))

sys.path.append(os.path.realpath(os.path.join(FILE_DIR, '..', '..')))
from global_vars import INSTALL_DIR, DATA_DIR

# preamble.
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

# Back open related data.
OPEN_DIR = os.path.realpath(os.path.join(INSTALL_DIR, 'open'))
OPEN_DATA_DIR_BAK = os.path.realpath(os.path.join(DATA_DIR, 'open'))
OPEN_DATA_FILE = os.path.realpath(os.path.join(INSTALL_DIR, 'open',\
                                                            'data', 'dirs.csv'))

if not os.path.exists(OPEN_DATA_DIR_BAK):
    os.makedirs(OPEN_DATA_DIR_BAK)
if not os.path.exists(OPEN_DIR):
    print(f"Open dir: {OPEN_DIR} does not exist.")
else:
    os.system(f"rsync -av {OPEN_DATA_FILE} {OPEN_DATA_DIR_BAK}")

# TODO: vimrc. 