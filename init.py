#!/usr/bin/python3

import os
import yaml


'''
Creates $INSTALL_DIR (default:~/.local/opt/utils). Copies `config.yaml` to 
$INSTALL_DIR. To install each package use `install.sh` / `install.py` from that 
directory.
'''

# Get directory info. 
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(REPO_DIR, 'config.yaml')
with open(CONFIG_FILE, 'r') as file:
    configs = yaml.safe_load(file)
INSTALL_DIR = os.path.realpath(os.path.expanduser(configs['install_dir']))

# Create installation directory.
if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)

# Update and save config.yaml.
TARGET_CONFIG_FILE = os.path.join(INSTALL_DIR, 'config.yaml')
configs['repo_dir'] = REPO_DIR
with open(TARGET_CONFIG_FILE, 'w') as file:
    yaml.dump(configs, file)