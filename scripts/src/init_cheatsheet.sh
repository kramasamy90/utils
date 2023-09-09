#!/bin/bash

# This script is used to initialize the cheatsheet
template_dir="/mnt/e/Documents/Templates/LaTeX Templates/Cheatsheet"

if [ ! -d "src" ]; then
    mkdir src
fi


cp "$template_dir"/cheatsheet_main.tex main.tex
cp "$template_dir"/cheatsheet_preamble.tex src/preamble.tex