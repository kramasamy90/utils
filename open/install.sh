#!/bin/bash

# Create directory ~/.local/opt
if [ ! -d ~/.local/opt ]; then
    mkdir -p ~/.local/opt
fi

# Create directory ~/.local/opt/open
if [ ! -d ~/.local/opt/open ]; then
    mkdir -p ~/.local/opt/open
fi

# Create directory ~/.local/opt/open/data
if [ ! -d ~/.local/opt/open/data ]; then
    mkdir -p ~/.local/opt/open/data
fi

# Create directory ~/.local/opt/open/src
if [ ! -d ~/.local/opt/open/src ]; then
    mkdir -p ~/.local/opt/open/src
fi

# Copy files to ~/.local/opt/open
cp ./src/o.sh ~/.local/opt/open/src/o
cp ./src/open.py ~/.local/opt/open/src/open.py
cp ./data/dirs.csv ~/.local/opt/open/data/dirs.csv 
cp ./data/help.txt ~/.local/opt/open/data/help.txt


# Add the path to .bashrc
if [ -f ~/.bashrc ]; then
    if ! grep -q "export PATH=\$PATH:~/.local/opt/open/src" ~/.bashrc; then
        echo "export PATH=\$PATH:~/.local/opt/open/src" >> ~/.bashrc
    fi
fi