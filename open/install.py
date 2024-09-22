#! /usr/bin/env python3

import os
import shutil
import sys

FILE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(FILE_DIR, '..'))

from global_vars import INSTALL_DIR

SOURCE_DIR = os.path.join(FILE_DIR, 'src')

# Create directories if they don't exist.
os.makedirs(INSTALL_DIR, exist_ok=True)
os.makedirs(os.path.join(INSTALL_DIR, 'open'), exist_ok=True)
os.makedirs(os.path.join(INSTALL_DIR, 'open', 'src'), exist_ok=True)
os.makedirs(os.path.join(INSTALL_DIR, 'open', 'data'), exist_ok=True)

print(FILE_DIR)

# Rsync files to INSTALL_DIR using os.system.
os.system(f'rsync -av {FILE_DIR}/src/ {INSTALL_DIR}/open/src')
os.system(f'mv {INSTALL_DIR}/open/src/o.sh {INSTALL_DIR}/open/src/o')
os.system(f'chmod +x {INSTALL_DIR}/open/src/o')

# Add INSTALL_DIR/open/src to PATH in .bashrc after 
# checking if it's already in PATH.
bashrc_path = os.path.expanduser('~/.bashrc')
with open(bashrc_path, 'r') as bashrc:
    content = bashrc.read()

path_to_add = f"export PATH=$PATH:{os.path.join(INSTALL_DIR, 'open', 'src')}"
if path_to_add not in content:
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write(f"\n{path_to_add}\n")
