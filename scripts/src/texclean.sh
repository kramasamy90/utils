#!/bin/bash

# This script cleans up the temporary files created by LaTeX.
# Delete files with the following extensions:.aux, .bbl, .blg, .log, .out, .synctex.gz

# Usage-1: texclean.sh # Default current directory.
# Usage-2: texclean.sh <path>

if [ $# -ne 0 ]; then
    cd $1
fi

if [ -f *.aux ]; then
    rm *.aux
fi
if [ -f *.bbl ]; then
    rm *.bbl
fi
if [ -f *.blg ]; then
    rm *.blg
fi
if [ -f *.log ]; then
    rm *.log
fi
if [ -f *.out ]; then
    rm *.out
fi
if [ -f *.synctex.gz ]; then
    rm *.synctex.gz
fi
