#!/bin/bash

# Create directory ~/.local/opt
if [ ! -d ~/.local/opt ]; then
    mkdir -p ~/.local/opt
fi

# Create directory ~/.local/opt/openweb
if [ ! -d ~/.local/opt/openweb ]; then
    mkdir -p ~/.local/opt/openweb
fi

# Create directory ~/.local/opt/open/data
if [ ! -d ~/.local/opt/openweb/data ]; then
    mkdir -p ~/.local/opt/openweb/data
fi

# Create directory ~/.local/opt/open/src
if [ ! -d ~/.local/opt/openweb/src ]; then
    mkdir -p ~/.local/opt/openweb/src
fi

# Copy files to ~/.local/opt/open
rsync -av ./src/ ~/.local/opt/openweb/src/
rsync -av ./data/ ~/.local/opt/openweb/data/


# Add the path to .bashrc
if [ -f ~/.bashrc ]; then
    if ! grep -q "export PATH=\$PATH:~/.local/opt/openweb/src" ~/.bashrc; then
        echo "export PATH=\$PATH:~/.local/opt/openweb/src" >> ~/.bashrc
    fi
fi