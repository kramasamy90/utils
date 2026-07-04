#!/usr/bin/python3

import os
import shutil

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

from global_vars import INSTALL_DIR, CACHE_DIR


'''
Creates $INSTALL_DIR (default:~/.local/opt/utils). Copies `config.yaml` to
$INSTALL_DIR. To install each package use `install.sh` / `install.py` from that
directory.

Works on both Linux and Windows. On Windows run from PowerShell:
    python init.py
'''

# Get directory info.
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# Write INSTALL_DIR and CACHE_DIR to yaml file.
# Written as plain "KEY: value" lines (no yaml module needed) — the same
# format tools parse at runtime (open/src/o.sh, open_win/install.py).
with open(os.path.join(REPO_DIR, "config.yaml"), "w") as f:
    f.write(f"CACHE_DIR: {CACHE_DIR}\n")
    f.write(f"INSTALL_DIR: {INSTALL_DIR}\n")

# Create installation directory.
if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)

# Copy global_vars.py and config.yaml to target location.
shutil.copy2(os.path.join(REPO_DIR, "global_vars.py"),
             os.path.join(INSTALL_DIR, "global_vars.py"))
shutil.copy2(os.path.join(REPO_DIR, "config.yaml"),
             os.path.join(INSTALL_DIR, "config.yaml"))

# Create cache directory.
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
