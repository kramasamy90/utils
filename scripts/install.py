#!/usr/bin/python3
import os
import re
import yaml

# Define constants
REPO_DIR = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.realpath(os.path.join(REPO_DIR, '../config.yaml'))
BASHRC_FILE = os.path.realpath(os.path.expanduser('~/.bashrc'))

# Load configuration
with open(CONFIG_FILE, 'r') as file:
    config = yaml.safe_load(file)

INSTALL_DIR = os.path.realpath(os.path.expanduser(config['install_dir']))
WORKING_DIR = os.path.realpath(os.path.join(INSTALL_DIR, os.path.basename(REPO_DIR)))

# Copy source to target directory
source_dir = os.path.realpath(os.path.join(REPO_DIR, 'src'))
target_dir = os.path.realpath(os.path.join(WORKING_DIR, 'src'))

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

os.chdir(source_dir)
print(f"Source dir: {source_dir}")
print(f"Target dir: {target_dir}")
os.system(f"chmod 755 *.sh *.py")
os.system(f"rsync -av {source_dir}/ {target_dir}")

# Update PATH in .bashrc if necessary
path_to_add = f"export PATH=$PATH:{target_dir}"
with open(BASHRC_FILE, 'r') as file:
    if path_to_add not in file.read():
        print(path_to_add)
        with open(BASHRC_FILE, 'a') as file:
            file.write(f"{path_to_add}\n")
