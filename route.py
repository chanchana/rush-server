import data_importer
import itertools
import lib.Pointr
import database as db

MAX = 999999999.9
START_NAME = 'START'
END_NAME = ['CASH1', 'CASH2', 'CASH3', 'CASH4', 'CASH5', 'CASH6'] 

# make travel from path
def travel(dvalue, path):
    result = []
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        result += dvalue[start][end][1]
    result += [path[-1]]
    return result

# find distance from nodes
def distance(dvalue, path):
    total = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        total += dvalue[start][end][0]
    return total

# RUSH - Nearest Neighbor
def nearest(dvalue, nodes):
    path = [START_NAME]
    free = nodes.copy()

    while free:
        start = path[-1]
        min_distance = MAX
        min_node = None
        # find the nearest node
        for node in free:
            if dvalue[start][node][0] < min_distance:
                min_distance = dvalue[start][node][0]
                min_node = node
        # append to path and remove from free
        path += [min_node]
        free.remove(min_node)

    # find the nearest casheir
    start = path[-1]
    min_distance = MAX
    min_node = None
    for end in END_NAME:
        if dvalue[start][end][0] < min_distance:
            min_distance = dvalue[start][end][0]
            min_node = end
    path += [end]

    # end
    trav = travel(dvalue, path)
    return path, trav
        

# RUSH - Permutation
def permutation(dvalue, nodes):
    min_distance = MAX
    min_path = None

    # permutation
    permutations = itertools.permutations(nodes)
    for p in permutations:
        for end in END_NAME:
            path = [START_NAME] + list(p) + [end]
            current_distance = distance(dvalue, path)
            if current_distance < min_distance:
                min_distance = current_distance
                min_path = path

    #end
    trav = travel(dvalue, min_path)
    return min_path, trav


# RUSH Algorithm
# output : 
#    path : order of item
#    trav : travel path through all nodes
def rush_algorithm(dvalue, nodes):
    print(nodes)
    trav = None
    path = None

    # hybrid
    if len(nodes) <= 8:
        path, trav = permutation(dvalue, nodes)
    else:
        path, trav = nearest(dvalue, nodes)

    print(path)
    print(trav)
    return path, trav

def update(group, name):
    ''' Update d_value of input map '''

    pr = data_importer.import_rm(group, name)
    pr.initialize_graph()
    d_value = pr.graph.d_value()
    data_importer.save_d_value(group, name, d_value)
    print('d_value updated')
    return d_value

# get route from node name 
def get(group, name, item_list):
    ''' get route from node name '''

    dvalue = data_importer.get_d_value(group, name)
    if dvalue == None:
        dvalue = update(group, name)
    for item in item_list:
        if not dvalue.get(item):
            return None
    return rush_algorithm(dvalue, item_list)

# get route from id list 
def get_from_id(group, name, item_id_list):
    ''' get route from item id list '''

    nodes = []
    for item in item_id_list:
        node = db.get_node_from_id(item)
        nodes.append(node)
    nodes = list(set(nodes))
    get(group, name, nodes)