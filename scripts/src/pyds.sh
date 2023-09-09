#!/bin/bash

set -e
set -o pipefail
set -u

cd /mnt/e/Documents/Cheatsheets/Python
cmd.exe /C start SumatraPDF.exe numpy_cheatsheet.pdf
cmd.exe /C start SumatraPDF.exe matplotlib_cs.pdf
cd /mnt/e/Documents/Cheatsheets/my_sheets/Programming/python_for_DS/ver_2
cmd.exe /C start SumatraPDF.exe python_for_DS.pdf
cd /mnt/e/Documents/Cheatsheets/my_sheets/Programming/python_libs
cmd.exe /C start SumatraPDF.exe python_libs.pdf
