#!/usr/bin/python3
import os
import re
import sys
import yaml

# Get vars.
REPO_DIR = os.path.realpath(os.path.dirname(__file__))
_BASENAME = os.path.basename(REPO_DIR)
_CONFIG_FILE = os.path.realpath(os.path.join(REPO_DIR, '../config.yaml'))
BASHRC = os.path.realpath(os.path.expanduser('~/.bashrc'))

with open(_CONFIG_FILE, 'r') as file:
    configs = yaml.safe_load(file)
_INSTALL_DIR = os.path.realpath(os.path.expanduser(configs['install_dir']))
WORKING_DIR = os.path.realpath(os.path.join(_INSTALL_DIR, _BASENAME))


# Install.
source = os.path.realpath(os.path.join(REPO_DIR, 'src'))
target = os.path.realpath(os.path.join(WORKING_DIR, 'src'))

if not os.path.exists(target):
    os.makedirs(target)
os.system(f"rsync -av {source}/ {target}")

# Add to path.
pattern  = target
is_in_path = False
with open(BASHRC, 'r') as file:
    for line in file:
        match = re.search(pattern, line)
        if match:
            is_in_path = True
            break

if not is_in_path:
    new_path = f"export PATH=$PATH:{target}"
    print(new_path)
    with open(BASHRC, 'a') as file:
        file.write(new_path)

# TODO: Automate backup to HDDs.