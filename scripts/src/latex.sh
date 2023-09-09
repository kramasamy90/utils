#!/bin/bash

set -e
set -o pipefail
set -u


cd /mnt/e/Documents/Cheatsheets/my_sheets/programming/latex

cmd.exe /C start SumatraPDF.exe latex.pdf

cd /mnt/e/Documents/Cheatsheets/Linux\ latex\ etc/

cmd.exe /C start SumatraPDF.exe latex_annotated.pdf
cmd.exe /C start SumatraPDF.exe latex.pdf
