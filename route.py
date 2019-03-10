import data_importer
import itertools
import lib.Pointr
MAX = 999999999.9
START_NAME = 'START'
END_NAME = 'END'

def get_travel(dvalue, pairs):
    travel = []
    for pair in pairs:
        travel += dvalue[pair[0]][pair[1]][1]
    return travel

def make_pair(path):
    pairs = []
    for i in range(len(path) - 1):
        pairs.append((path[i], path[i+1]))
    return pairs

def cal_dist(dvalue, pairs):
    dist = 0
    for pair in pairs:
        dist += dvalue[pair[0]][pair[1]][0]
    return dist

def full_path(names):
    return [START_NAME] + names + [END_NAME]

def make_travel(dvalue, path):
    travel = []
    pairs = make_pair(path)
    for pair in pairs:
        travel += dvalue[pair[0]][pair[1]][1]
    return travel + [END_NAME]

def nearest(dvalue, names):

    def get_min(target):
        minv = MAX
        data = ''
        for key in free:
            if key != target and dvalue[target][key][0] < minv:
                minv = dvalue[target][key][0]
                data = key
        return data

    free = names.copy()
    path = []
    path.append(START_NAME)
    while len(free) > 0:
        found = get_min(path[-1])
        path.append(found)
        free.remove(found)

    path.append(END_NAME)
    return make_travel(dvalue, path)


def rush_algorithm(dvalue, names):
    print(names)
    print(full_path(names))
    min_value = MAX
    min_path = None
    min_travel = None
    if len(names) <= 8:
        permutations = itertools.permutations(names)
        for p in permutations:
            path = full_path(list(p))
            # print(path)
            pairs = make_pair(path)
            # print(cal_dist(dvalue, pairs))
            dist = cal_dist(dvalue, pairs)
            if dist < min_value:
                min_value = dist
                min_path = path
        min_travel = make_travel(dvalue, min_path)
    else:
        min_travel = nearest(dvalue, names)

    # print(min_value)
    # print(min_path)
    # print(min_travel)
    print(min_travel)
    return min_travel


def update(group, name):
    ''' Update d_value of input map '''
    pr = data_importer.import_rm(group, name)
    pr.initialize_graph()
    d_value = pr.graph.d_value()
    data_importer.save_d_value(group, name, d_value)
    print('d_value updated')
    return d_value

def get(group, name, item_list):
    dvalue = data_importer.get_d_value(group, name)
    if dvalue == None:
        dvalue = update(group, name)
    for item in item_list:
        if not dvalue.get(item):
            return None
    return rush_algorithm(dvalue, item_list)

if __name__ == '__main__':
    # update()
    # get('sample', 'sample', ['1', '4', '12', '14', '106', '100'])
    # get('sample', 'sample', ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    # get('sample', 'sample', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
    # print(get('sample', 'sample', ['1', '4', '12', '1444', '105556', '100']))
    # get('sample', 'sample', ['1', '12', '14', '106'])
    update('KMUTT', 'KMUTT Book Store')