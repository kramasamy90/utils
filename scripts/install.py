#!/usr/bin/python3
import os
import sys

FILE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(FILE_DIR, '..'))

from global_vars import INSTALL_DIR

# Define constants
BASHRC_FILE = os.path.realpath(os.path.expanduser('~/.bashrc'))

# Load configuration
INSTALL_DIR = os.path.realpath(os.path.join(INSTALL_DIR, \
                                                    os.path.basename(FILE_DIR)))

# Copy source to target directory
source_dir = os.path.realpath(os.path.join(FILE_DIR, 'src'))
target_dir = os.path.realpath(os.path.join(INSTALL_DIR, 'src'))

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
