#!/bin/bash

# set -e
# set -o pipefail
# set -u

# Usage:
# 	opend <alias>	        - Open <alias> in windows explorer.
# 	. opend -t <alias>	- Open <alias> in terminal.
# 	source opend -t <alias> - Open <alias> in terminal.
# 	opend -l 		- List dir path represented by <alias>.
# 	opend -h		- Show this list.

# Design:
# 	opend is bash wrapper around open.py script. 
# 	Flag '-t' is passed on to open.py.
# 	With this flag open.py prints the dir path of <alias> instead of opening it in windows explorer.
# 	This output is used by opend to change directory (cd).
# 	To use cd this script has to be sourced.
# 	With flag '-h' opend prints the contents of opend_help.txt.

# 	Script files are stored in /mnt/d/my_programs/open

py_file="$HOME/.local/opt/open/src/open.py"
dir_file="$HOME/.local/opt/open/data/dirs.csv"
src_dir="$HOME/.local/opt/open/src"
data_dir="$HOME/.local/opt/open/data"

# Open current directory in windows explorer.
if [ "$1" == "." ]
then
	explorer.exe .

# Open parent directory in windows explorer.
elif [ "$1" == ".." ]
then
    explorer.exe ..

elif [ "${1: 0:1}" != "-" ]
then
    # test if the $1 has the extension .pdf
    if [[ "${1: -4}" == ".pdf" ]]
    then
        # if it does, open it with SumatraPDF
        cmd.exe /C start SumatraPDF.exe "$1"
    else
        # otherwise, open it in explorer
        python3 $py_file $@
    fi
# Help.
elif [ "$1" == "-h" ]
then
	cd $data_dir
	cat help.txt

# List all aliases.
elif [ "$1" == "-l" ]
then
	cd $data_dir
	cat dirs.csv

# Open alias in terminal.
elif [ "$1" == "-t" ]
then
	dir=$(python3 $py_file $@)
    if [ -d "$dir" ]
    then
        cd "$dir"
    else
        echo "ERROR: the following directory does not exist!!!"
        echo "$dir"
    fi

# Add alias.
elif [ "$1" == "-a" ]
then
	python3 $py_file $@
	cd $src_dir
	cat dirs.csv | sort -k2 > temp.csv
	mv temp.csv dirs.csv

# Remove alias.
elif [ "$1" == "-r" ]
then 
    cd $data_dir
	cat dirs.csv | grep -vwE "^$2" > temp.csv
	mv temp.csv dirs.csv

# Rename alias.
elif [ "$1" == "-n" ]
then
    cd $data_dir
    cat dirs.csv | sed "s/^$2/$3/" > temp.csv
    mv temp.csv dirs.csv

# Remove alias in bulk.
# Usage: o -br <file>
# The file should contain one alias per line.
elif [ "$1" == "-br" ]
then
    CURRENT_DIR=$(pwd)
	cd $data_dir
    while read -r line
    do
        sed -i "/$line/d" dirs.csv
    done < "$CURRENT_DIR/$2"

# Open relative path in windows explorer.
elif [[ "${1:0:2}" == "./" || "${1: -1}" == "/" ]]
then
    cd "$1"
    explorer.exe .

# Open alias in windows explorer.
else
    echo "Invalid option"
    echo "Use -h for help"
fi