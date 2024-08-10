#!/bin/bash

# Create directory ~/.local/opt
if [ ! -d ~/.local/opt ]; then
    mkdir -p ~/.local/opt
fi

# Create directory ~/.local/opt/open_website
if [ ! -d ~/.local/opt/open_website ]; then
    mkdir -p ~/.local/opt/open_website
fi

# Create directory ~/.local/opt/open/data
if [ ! -d ~/.local/opt/open_website/data ]; then
    mkdir -p ~/.local/opt/open_website/data
fi

# Create directory ~/.local/opt/open/src
if [ ! -d ~/.local/opt/open_website/src ]; then
    mkdir -p ~/.local/opt/open_website/src
fi

# Copy files to ~/.local/opt/open
rsync -av ./src/ ~/.local/opt/open_website/src/
rsync -av ./data/ ~/.local/opt/open_website/data/


# Add the path to .bashrc
if [ -f ~/.bashrc ]; then
    if ! grep -q "export PATH=\$PATH:~/.local/opt/open_website/src" ~/.bashrc; then
        echo "export PATH=\$PATH:~/.local/opt/open_website/src" >> ~/.bashrc
    fi
fi