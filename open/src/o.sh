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

# Get the directory of this o.sh file.
FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
INSTALL_DIR="$FILE_DIR/../.."
SRC_DIR="$( cd $INSTALL_DIR &> /dev/null && pwd )/open/src"
DATA_DIR="$( cd $INSTALL_DIR &> /dev/null && pwd )/open/data"
# 
# Read INSTALL_DIR and CACHE_DIR from yaml file.
CACHE_DIR=$(cat $INSTALL_DIR/config.yaml | grep "CACHE_DIR" | sed -E 's/CACHE_DIR:\s+(.*)/\1/')


py_file="$SRC_DIR/open.py"
src_dir="$SRC_DIR"
data_dir="$DATA_DIR"
dir_file="$DATA_DIR/dirs.csv"


# Open current directory in windows explorer.
if [ "$1" == "." ]
then
	xdg-open .

# Open parent directory in windows explorer.
elif [ "$1" == ".." ]
then
    xdg-open ..

elif [ "${1: 0:1}" != "-" ]
then
    # If the extension is .pdf it does, open it with SumatraPDF.
    if [[ "${1: -4}" == ".pdf" || "${1: -4}" == ".PDF" ]]
    then
        xdg-open "$1"
    # else if the extension is .txt or .md open it with notepad.
    elif [[ "${1: -4}" == ".txt" || "${1: -3}" == ".md" ]]
    then
        xdg-open "$1"
    # otherwise, open the folder alias it in explorer.
    else
        python3 $py_file $@
    fi
# Help.
elif [ "$1" == "-h" ]
then
	cd $data_dir
	cat ../data/help.txt

# List all aliases.
elif [ "$1" == "-l" ]
then
	cd $data_dir
	cat ../data/dirs.csv

# Search for a keyword.
elif [ "$1" == "-s" ]
then
	cd $data_dir
	cat ../data/dirs.csv | grep $2

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
    output=$(python3 $py_file $@)
    exit_code=$?
    echo "$output"
    if [ $exit_code -eq 1 ]
    then
        if echo "$output" | grep -q "already associated"
        then
            echo "Would you like to force rename?[yes/no]"
            read response
            if [ "$response" == "yes" ]
            then
                old_alias=$(echo "$output" | grep "already associated" | awk '{print $NF}')
                awk -F'\t' -v old="$old_alias" -v new="$2" \
                    'BEGIN{OFS="\t"} $1==old{$1=new}1' \
                    "$dir_file" > "$dir_file.tmp"
                mv "$dir_file.tmp" "$dir_file"
                echo "Renamed '$old_alias' to '$2'"
            fi
        fi
    fi
    sort -k2 "$dir_file" > "$dir_file.tmp"
    mv "$dir_file.tmp" "$dir_file"

elif [ "$1" == "-af" ]
then
    grep -vwE "^$2" "$dir_file" > "$dir_file.tmp"
    mv "$dir_file.tmp" "$dir_file"
    python3 $py_file -a "${@:2}"
    if [ $? -eq 0 ]
    then
        sort -k2 "$dir_file" > "$dir_file.tmp"
        mv "$dir_file.tmp" "$dir_file"
    fi

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
    xdg-open .

# Open alias in windows explorer.
else
    echo "Invalid option"
    echo "Use -h for help"
fi