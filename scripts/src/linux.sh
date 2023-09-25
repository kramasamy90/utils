#!/bin/bash

set -e
set -o pipefail
set -u

cd /mnt/d/projects/cheatsheets/programming/linux
cmd.exe /C start SumatraPDF.exe linux.pdf
