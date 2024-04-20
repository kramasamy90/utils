#!/bin/bash

set -e
set -o pipefail
set -u

cd /mnt/e/Documents/Cheatsheets/programming/Python
cmd.exe /C start SumatraPDF.exe mementopython3-english.pdf
cmd.exe /C start SumatraPDF.exe numpy_cheathseet.pdf
cmd.exe /C start SumatraPDF.exe matplotlib_cs.pdf
cmd.exe /C start SumatraPDF.exe pandas_basics_cheatsheet.pdf

cd /mnt/d/projects/cheatsheets_drafts/programming/python_oop
cmd.exe /C start SumatraPDF.exe python_oop.pdf

cd /mnt/e/Documents/Cheatsheets/my_sheets/Programming/python_libs
cmd.exe /C start SumatraPDF.exe python_libs.pdf

cd /mnt/e/Documents/Cheatsheets/my_sheets/Programming/python_for_DS/ver_2
cmd.exe /C start SumatraPDF.exe python_for_DS.pdf

