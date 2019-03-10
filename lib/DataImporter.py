import Pointr
import logging
import json

# def import_rmp(filename='map.rmp'):

#     pr = Pointr.Pointr()

#     with open(filename) as f:
#         for line in f:
#             line = line.strip()
#             if line == '' or line[0] == '#':
#                 continue
            
#             data = line.split(' ')
#             if data[0] == 'POINT':
#                 point = (float(data[2]), float(data[3]))
#                 t = pr.add(data[1], point)
#                 # print(point)
#                 print('ADDED')
#                 print(t.position)
#             elif data[0] == 'LINK':
#                 pr.add_edge_name(data[1], data[2])
#             else:
#                 logging.warning('DataImporter Error import : ' + line)

#             # print(line)


#     return pr

def import_rm(group, name):
    pr = Pointr.Pointr()

    with open('/{}/{}.rm.json'.format(group, name)) as f:
        data = json.load(f)
        print(data)

def save_d_value(group, name, dvalue):
    pass

def get_d_value(group, name):
    pass

if __name__ == '__main__':
    import_rm('sample', 'sample')
