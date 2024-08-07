#!/bin/bash

# Function to clean up auxiliary files
cleanup() {
    rm -f *.aux *.toc *.lof *.lot *.out *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg *.nav *.snm *.vrb
}

# Check if an argument is given
if [ "$#" -eq 1 ]; then
    MAIN_FILE="$1"
elif [ "$#" -eq 0 ]; then
    # Find all .tex files in the current directory
    TEX_FILES=(*.tex)
    if [ "${#TEX_FILES[@]}" -eq 1 ]; then
        MAIN_FILE="${TEX_FILES[0]}"
    elif [ "${#TEX_FILES[@]}" -gt 1 ]; then
        echo "Error: Multiple .tex files found. Please specify the main file."
        exit 1
    else
        echo "Error: No .tex file found in the current directory."
        exit 1
    fi
else
    echo "Usage: $0 [mainfile.tex]"
    exit 1
fi

# Get the base name of the main file
BASENAME=$(basename "$MAIN_FILE" .tex)

# Compile the .tex file with pdflatex
pdflatex "$MAIN_FILE"

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    # Clean up auxiliary files
    cleanup
else
    echo "Compilation failed. Check the log file: $BASENAME.log"
fi
