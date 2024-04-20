#!/bin/bash

set -e
set -o pipefail
set -u


cd /mnt/d/projects/cheatsheets/programming/c
cmd.exe /C start SumatraPDF.exe c.pdf

cd /mnt/d/projects/cheatsheets/programming/cpp
cmd.exe /C start SumatraPDF.exe cpp.pdf

