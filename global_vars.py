import os

# Set the below variables.
_INSTALL_DIR = '~/.local/opt/utils'
_DATA_DIR = '~/Code/data'

# Don't touch the below code.
INSTALL_DIR = os.path.realpath(os.path.expanduser(_INSTALL_DIR))
DATA_DIR = os.path.realpath(os.path.expanduser(_DATA_DIR))