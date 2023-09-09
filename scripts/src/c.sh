#!/bin/bash

set -e
set -o pipefail
set -u


cd /mnt/d/projects/notes/programming/C
cmd.exe /C start SumatraPDF.exe C_language.pdf

cd /mnt/d/projects/notes/programming/Cpp
cmd.exe /C start SumatraPDF.exe Cpp_language.pdf

