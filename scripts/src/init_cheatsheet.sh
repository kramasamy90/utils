#!/bin/bash

# This script is used to initialize the cheatsheet
template_dir="/home/kramasamy/Documents/Templates/LaTeX Templates/Cheatsheet/"

rsync -av "$template_dir"  ./
