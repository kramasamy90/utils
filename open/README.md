**This tool helps to open directories using an alias.**

### Install
Run `bash install.sh`. Copies files to ~/.local/opt/open
Restart the terminal or execute `source ~/.bashrc`.
WARNING: `install.sh` resets the data stored locally.

### Update
Run `bash update.sh`.

### Usage:
	o <alias1> <alias2> ...     - Open <alias1>, <alias2>,... in windows explorer.

	o .				- Open current folder in windows explorer.

	. o -t <alias>		- Open <alias> in terminal.

	source o -t <alias> 	- Open <alias> in terminal.

	o -a -d"," <alias>,<path> 	- Append alias and path to the database file and sort the file.

					  The flag -d is optional. The default is ",".

					  If <path> is absent current directory is used.

	o -d			- Open database in vim.

	o -l 			- List dir path represented by <alias>.

	o -h			- Show this list.

	o -r <alias>	- Remove the alias <alias>.

    o -br <file>    - Remove all the aliases in file <file>.

### Design:
	o is bash wrapper around open.py script. 

	Flag '-t' is passed on to open.py.

	With this flag open.py prints the dir path of <alias> instead of opening it in windows explorer.

	This output is used by o to change directory (cd).

	To use cd this script has to be sourced.

	With flag '-h' o prints the contents of o.txt.

	Script files are stored in /mnt/d/my_programs/open

