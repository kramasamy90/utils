import os
import sys

#%%
## Set directories
working_dir = "/home/kramasamy90/.local/opt/open/src"
calling_dir = os.getcwd()
os.chdir(working_dir)
os.getcwd()

#%%
## Create functions

def import_relation(filename):
	"""
	filename is name of file that contains directory alias and full directory path as a tsv file.
	This function read from this file and creates a library.
	"""
	output = dict()
	with open(filename) as file:
		for line in file:
			line = line.split('\t')[0:2]
			line[1] = line[1].split('\n')[0]
			output.update({line[0]: line[1]})

	return(output)

def open_dir(dir_name):
	explorer = 'explorer.exe'
	os.chdir(dir_name)
	os.system('explorer.exe .')
	os.chdir(working_dir)

def escape_spaces(dir_name):
	dir_name_split_list = dir_name.split(" ")
	dir_name = ''
	for dir_name_fragment in dir_name_split_list:
		dir_name += dir_name_fragment + '\ '
	dir_name = dir_name[0:len(dir_name)-2]
	return(dir_name)

def get_new_alias(string, sep, basename, keys, values):
	'''
	NOTE: keys and values should be list, not 'dict_keys' or 'dict_values'.
	'''
	string = string.split(sep)
	alias = string[0]
	if (len(string) == 1):
		path = basename
	if (len(string) == 2):
		path = string[1]
		if (path == '.'):
			path = basename
		if (path[0:2] == './'):
			path = basename + path[1:]
		elif (path[0:2] == '..'):
			basename = basename.split('/')
			basename = '/'.join(basename[0:len(basename)-1])
			path = basename + path[2:]
		elif (path[0] != '/'):
			path = basename + '/' + path

	if (alias in keys):
		print('ERROR: This alias is already taken')
		return(-1)
	elif (path in values):
		index = values.index(path)
		print('ERROR: This path is already associated with: ', keys[index])
		return(-1)
	else:
		return(alias + '\t' + path)

#%%

## Import relations and arguments

rels = import_relation('../data/dirs.csv')

flags = []
flag_args = []
args = []

for i in range(1,len(sys.argv)):
	if sys.argv[i][0] == '-':
		flag = sys.argv[i][1:]
		flags.append(flag[0])
		flag_args.append(flag[1:])
	else:
		args.append(sys.argv[i])



#%%
## Act on arguments
dir = sys.argv[1]

if (len(flags) == 0):
	missing_alias = []
	for arg in args:
		if (arg in rels.keys()):
			open_dir(rels[arg])
		else:
			missing_alias.append(arg)
	if (len(missing_alias) > 0):
		print('WARNING: The following do(es) not exist.')
		for alias in missing_alias:
			print(alias)
else:
	if (flags[0] == 't'):
		arg = args[0]
		if (arg in rels.keys()):
			print(rels[arg])
		else:
			print('WARNING: The following do(es) not exist.')
			print(arg)
			
	if (flags[0] == 'a'):
		if ('d' in flags):
			index = flags.index('d')
			sep = flag_args[index]
		else:
			sep = ','

		arg = ' '.join(args)
		new_alias = get_new_alias(arg, sep, calling_dir, list(rels.keys()), list(rels.values()))

		if (new_alias != -1):
			command = 'echo "' + new_alias + '" >> ' + working_dir + '/../data/dirs.csv'
			os.system(command)
