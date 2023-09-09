#!/bin/bash

# Function to compile C and C++ code
compile_code() {
    local file="$1"
    local extension="${file##*.}"
    local base_name="${file%.*}"

    if [[ "$extension" == "c" ]]; then
        gcc "$file" -o "$base_name"
    elif [[ "$extension" == "cpp" ]]; then
        g++ "$file" -o "$base_name"
    fi
}

# Iterate over all .c and .cpp files in the current directory
# if there are no command line argument
if [[ $# -eq 0 ]]; then
    for source_file in *.c *.cpp; do
        # Check if the file exists (in case no .c or .cpp files are present)
        if [[ -f "$source_file" ]]; then
            # If the $source_file has .cpp extension then compile using g++
            if [[ "${source_file##*.}" == "cpp" ]]; then
                g++ "$source_file" -o "${source_file%.*}"
            elif [[ "${source_file##*.}" == "c" ]]; then
                gcc "$source_file" -o "${source_file%.*}"
            fi
        fi
    done
fi

# Check if the first command line argument begins with '-'.
# If so, do something.
if [[ "$1" == -* ]]; then
    if [[ "$1" == "-clean" ]]; then
        # Remove all files with .out extension
        rm -f *.out
        # Remove all files with basename derived from basename.cpp or basename.c
        for source_file in *.c *.cpp; do
            if [[ -f "${source_file%.*}" ]]; then
                rm -f "${source_file%.*}"
            fi
        done
    fi
else
    # Compile all the files passed as command line arguments
    for source_file in "$@"; do
        if [[ -f "$source_file" ]]; then
            compile_code "$source_file"
        fi
    done
fi

