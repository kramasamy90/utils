#!/bin/bash

# chmod all the bash files in current directory to executables.
chmod +x *.sh

# copy all the bash files in the directory from which this script is executed to ~/.local/bin without .sh extension
for file in *.sh
do
    cp $file ~/.local/bin/$(echo $file | cut -d'.' -f1)
done