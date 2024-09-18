#!/usr/bin/python3
import os
import sys
import yaml

# Preamble.
WORKING_DIR = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.realpath(os.path.join(WORKING_DIR, '../../config.yaml'))
with open(CONFIG_FILE, 'r') as file:
    configs = yaml.safe_load(file)
DATA_DIR = os.path.realpath(os.path.expanduser(configs['data_dir']))
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