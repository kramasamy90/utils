#!/usr/bin/python3

import os
import sys
import yaml

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

from global_vars import INSTALL_DIR, CACHE_DIR


'''
Creates $INSTALL_DIR (default:~/.local/opt/utils). Copies `config.yaml` to 
$INSTALL_DIR. To install each package use `install.sh` / `install.py` from that 
directory.
'''

# Get directory info. 
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# Write INSTALL_DIR and CACHE_DIR to yaml file.
with open(f"{REPO_DIR}/config.yaml", "w") as f:
    yaml.dump({"INSTALL_DIR": INSTALL_DIR, "CACHE_DIR": CACHE_DIR}, f)

# Create installation directory.
if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)

# Copy global_vars.py to target location.
os.system(f"cp {REPO_DIR}/global_vars.py {INSTALL_DIR}/global_vars.py")
os.system(f"cp {REPO_DIR}/config.yaml {INSTALL_DIR}/config.yaml")

# Create cache directory.
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
