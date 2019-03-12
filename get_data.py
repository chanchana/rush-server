import os
from fnmatch import fnmatch
import route
import json

SPLITTER = ';'

def get_map_list():
    # list
    map_list = []
    # go to current dir
    cwd = os.getcwd()
    path = cwd + '/map/data'
    pattern = "*.rd.json"
    # walk all files
    for path, subdirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, pattern):
                # matched
                found = str(os.path.join(path, name))
                print(found)
                # set group , map name
                data = {}
                x = found.split('/')
                group = x[-2]
                map_name = x[-1].split('.')[0]
                data['group'] = group
                data['name'] = map_name
                # insert to list
                map_list.append(data)
    # return
    print(map_list)
    return map_list

def get_map_data(group_name, map_name):
    # go to current dir
    cwd = os.getcwd()
    path = '{}/map/data/{}/{}.rd.json'.format(cwd, group_name, map_name)
    # return json data
    data = {}
    with open(path) as f:
        imported = json.load(f)
        data = imported['nodes']
    return data

def get_map_point(group_name, map_name):
    # go to current dir
    cwd = os.getcwd()
    path = '{}/map/data/{}/{}.rm.json'.format(cwd, group_name, map_name)
    # return json data
    data = {}
    with open(path) as f:
        imported = json.load(f)
        data = imported['nodes']
    return data

def get_route(group_name, map_name, item_string):
    items = item_string.split(SPLITTER)
    return route.get(group_name, map_name, items)

def get_route_from_id(group_name, map_name, item_id_string):
    print(item_id_string)
    item_id_string = item_id_string.strip()
    if item_id_string[0] == ';':
        item_id_string = item_id_string[1:]
    print(item_id_string)
    items = item_id_string.split(SPLITTER)
    return route.get_from_id(group_name, map_name, items)

if __name__ == '__main__':
    get_map_list() 
    get_map_data('sample', 'sample')