#!/usr/bin/python3

import os
import yaml


'''
Creates $INSTALL_DIR (default:~/.local/opt/utils). Copies `config.yaml` to 
$INSTALL_DIR. To install each package use `install.sh` / `install.py` from that 
directory.
'''

# Get directory info. 
REPO_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(REPO_DIR, 'config.yaml')
with open(CONFIG_FILE, 'r') as file:
    configs = yaml.safe_load(file)
INSTALL_DIR = os.path.realpath(os.path.expanduser(configs['install_dir']))

# Save config.yaml.
configs['repo_dir'] = REPO_DIR
with open(CONFIG_FILE, 'w') as file:
    yaml.dump(configs, file)

# Create directories and move files.
if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)
os.system(f"cp config.yaml {INSTALL_DIR}/config.yaml")
