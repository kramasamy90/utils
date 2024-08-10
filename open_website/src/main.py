import os
import sys
import yaml

'''
    Usage:
        ow google
        ow mysite_1 mysite_2 ...
        ow -a iitm www.iitm.ac.in
'''


if __name__ == '__main__':

    ## Init.
    HOME_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = HOME_DIR + '/../data'
    DICT_FILE = DATA_DIR + '/maps.yaml'

    ## Read the map file.
    if not os.path.exists(DICT_FILE):
        map = {}
        with open(DICT_FILE, 'w') as file:
            yaml.dump(map, file)

    with open(DICT_FILE, 'r') as file:
        map = yaml.safe_load(file)
    
    ## Process the arguments.

    # Open sites.
    if len(sys.argv) > 1 and sys.argv[1][0] != '-':
        for i in range(1, len(sys.argv)):
            key = sys.argv[i]
            val = map.get(key)
            print(val)
            if val is None:
                print(f'Key not found {key}!')
            else:
                os.system('microsoft-edge ' + val)
    
    # Add a new key-val pair.
    if len(sys.argv) > 1 and sys.argv[1][0:2] == '-a':
        key = sys.argv[2]
        val = sys.argv[3]
        if map.get(key) is not None:
            print(f'This key {key} is already associated with {map[key]}.')
            response = input("Do you want to update the existing key with the new values? [yes/no]")
            if response == "yes" or response == "Yes":
                map[key] = val
        else:
            map[key] = val
            with open(DICT_FILE, 'w') as file:
                yaml.dump(map, file)

    # Print the value of input key.
    if len(sys.argv) > 1 and sys.argv[1][0:2] == '-p':
        key = sys.argv[2]
        val = map.get(key)
        if val is None:
            print(f'Key not found {key}!')
        else:
            print(val)

    # Print the maps.yamls file.
    if len(sys.argv) > 1 and sys.argv[1][0:2] == '-l':
        with open(DICT_FILE) as file:
            for line in file:
                print(line)
