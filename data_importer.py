import logging
import json
import lib.Pointr as Pointr


def import_rm(group, name):
    pr = Pointr.Pointr()

    with open('map/data/{}/{}.rm.json'.format(group, name), 'r') as f:
        data = json.load(f)
        # print(data)
        for key in data['nodes']:
            position = (data['nodes'][key][0], data['nodes'][key][1])
            pr.add(key, position)
        for link in data['links']:
            p1, p2 = link[0], link[1]
            pr.add_edge_name(p1, p2)

        return pr
    return None


def save_d_value(group, name, dvalue):
    with open('map/data/{}/{}.dvalue.json'.format(group, name), 'w') as f:
        json.dump(dvalue, f)


def get_d_value(group, name):
	data = None
	try:
		with open('map/data/{}/{}.dvalue.json'.format(group, name), 'r') as f:
			data = json.load(f)
	except:
		pass
	return data

if __name__ == '__main__':
    import_rm('sample', 'sample')
