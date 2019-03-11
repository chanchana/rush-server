import json

lt = (120, 210)
rt = (620, 210)
shelf_height = 25
between_height = 14 

l_count = 1
n_count = 1
nodes = {}

for x in range(8):
    key = f'L{str(l_count).zfill(2)}'
    s = (lt[0], lt[1] + ((shelf_height + between_height) * x))
    nodes[key] = s
    l_count += 1

    key = f'L{str(l_count).zfill(2)}'
    t = (rt[0], rt[1] + ((shelf_height + between_height) * x))
    nodes[key] = t
    l_count += 1

    for y in range(8):
        key = f'N{str(n_count).zfill(3)}'
        nodes[key] = (s[0] + 31.25 + (62.5 * y), s[1])
        n_count += 1


    key = f'L{str(l_count).zfill(2)}'
    s = (lt[0], lt[1] + ((shelf_height + between_height) * x) + shelf_height)
    nodes[key] = s
    l_count += 1

    key = f'L{str(l_count).zfill(2)}'
    t = (rt[0], rt[1] + ((shelf_height + between_height) * x) + shelf_height)
    nodes[key] = t
    l_count += 1

    for y in range(8):
        key = f'N{str(n_count).zfill(3)}'
        nodes[key] = (s[0] + 31.25 + (62.5 * y), s[1])
        n_count += 1

print(nodes)

data = {}
with open("Bottom Market.rm.json", 'r') as f:
    data = json.load(f)
    data['nodes'] = nodes

with open("Bottom Market.rm.json", "w") as f:
    json.dump(data, f)
