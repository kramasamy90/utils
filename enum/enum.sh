#!/bin/bash

files=($(ls))
i=1

if [ $# -eq 1 ]
then
	for file in ${files[@]}
	do
		new_file_name=$(echo $i).$(echo $1)
		mv $file $new_file_name
		let i++
	done
fi
