#!/bin/bash

if [ ! -d ~/.local/opt/scripts ]; then
    mkdir -p ~/.local/opt/open
fi

rsync -av ./src/ ~/.local/opt/scripts/

# Add the path to .bashrc
if [ -f ~/.bashrc ]; then
    if ! grep -q "export PATH=\$PATH:~/.local/opt/scripts/src" ~/.bashrc; then
        echo "export PATH=\$PATH:~/.local/opt/scripts" >> ~/.bashrc
    fi
fi
