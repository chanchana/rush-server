import logging

DEFAULT_WEIGHT = 1

class Node:
    def __init__(self, name, data=None):
        self.name = name
        self.adjs = []

    def add_data(self, data):
        self.data = data

    def add_adj(self, edge):
        self.adjs.append(edge)

    def get_adj(self, node):
        for adj in self.adjs:
            if adj.to == node:
                return adj
        
        return None

    def get_adj_weight(self, node_name):
        for adj in self.adjs:
            if adj.to.name == node_name:
                return adj.weight

        return 0

    def __str__(self):
        return '{} -> {}'.format(self.name, [x.get_adj_node_name() for x in self.adjs])

class Edge:
    def __init__(self, to:Node, weight=DEFAULT_WEIGHT):
        self.to = to
        self.weight = weight

    def get_adj_node_name(self):
        return self.to.name

class Graph:
    def __init__(self, graph_data=None, directed=True, weighted=False):
        self.names = {}
        self.nodes = []
        self.directed = directed
        self.weighted = weighted

        if graph_data:
            # print(graph_data)
            self.add_adjs(graph_data)

    def get_node(self, name):
        # for node in self.nodes:
        #     if node.name == name:
        #         return node
        # return None
        if self.names.get(name):
            return self.names[name]
        
        return None

    def d_value(self):
        data = {}

        for node in self.nodes:
            data[node.name] = {}
            value = self.dijkstra(node.name)
            for v in value:
                data[node.name][v.name] = value[v]
                # print(value[v])

        print(data)
        return data


    def dijkstra(self, start_node_name):

        def make_path(parent_dict, key):
            path = []
            path.append(key.name)
            string = str(key.name)
            while parent_dict[key] != None:
                key = parent_dict[key]
                path.append(key.name)
                string = str(key.name) + ' -> ' + string

            path = list(reversed(path))

            path.pop(-1)
            return path, string

        start_node = self.get_node(start_node_name)

        nodes = self.nodes.copy()
        d_value = {}
        value = {}

        parent = {}

        for node in nodes:
            d_value[node] = 999999
            parent[node] = None

        d_value[start_node] = 0

        while len(nodes) > 0:
            # current_node = min(d_value.items(), key= lambda x: x[1])[0]
            current_node = min(nodes, key=lambda x:d_value[x])
            nodes.remove(current_node)

            # print(current_node.name)
            for adj in current_node.adjs:
                if adj.to in nodes:
                    if d_value[current_node] + adj.weight < d_value[adj.to]:
                        d_value[adj.to] = d_value[current_node] + adj.weight
                        parent[adj.to] = current_node
        # print(d_value)
        # print(path_string)



        # print('d=')
        # for p in d_value:
        #     print(p.name, d_value[p])
        # print('end')

        # print('p=')
        for p in parent:
            # print(p)
            path_arr, string = make_path(parent, p)
            # print(string)
            value[p] = (d_value[p], path_arr, string)
        # print('end')

        # print(value)

        return value

        # print('p2=')
        # for p in path:
        #     print(p.name, path[p])
        # print('end')

    def add_node(self, name, data=None):
        new_node = Node(name, data)
        self.nodes.append(new_node)
        self.names[name] = new_node
        return new_node

    def add_nodes(self, names):
        for name in names:
            self.add_node(name)

    def add_adj(self, from_node, to_node, weight=DEFAULT_WEIGHT):
        start_node = self.get_node(from_node)
        end_node = self.get_node(to_node)

        if not start_node:
            start_node = self.add_node(from_node)
        
        if not end_node:
            end_node = self.add_node(to_node)

        if not self.check_adj(start_node, end_node):
            start_node.add_adj(Edge(end_node, weight))

            if not self.directed:
                end_node.add_adj(Edge(start_node, weight))
    
    def add_adjs(self, edges):
        for edge in edges:
            node1 = edge[0]
            node2 = edge[1]

            if self.weighted:
                weight = edge[2]
            else:
                weight = DEFAULT_WEIGHT

            # print(node1, node2, weight)
            self.add_adj(node1, node2, weight)

    def get_route_lite(self, from_node_name, to_node_name):
        values = self.dijkstra(from_node_name)
        to_node = self.get_node(to_node_name)
        # print('RETURN')
        # print(values)
        # print(to_node)

        print(values[to_node])
        # print(value[to_node])
        return values[to_node][2]

    def get_route(self, node_names):
        start_node_name = node_names[0]
        end_node_name = node_names[-1]
        node_names.pop(0)
        node_names.pop(-1)
        pop_name = ''
        path = []
        path_name = []
        string = ''
        
        current_node_name = start_node_name

        while len(node_names) != 0:

            dijkstra_value = self.dijkstra(current_node_name)
            d_value = {}
            print(dijkstra_value)
            for name in node_names:
                d_value[name] = dijkstra_value[self.get_node(name)][0]
            
            min_d_name = min(d_value, key=d_value.get)
            min_d_node = self.get_node(min_d_name)

            path = reversed(dijkstra_value[min_d_node][1])
            string += dijkstra_value[min_d_node][2]

            for p in path:
                path_name.append(p.name)

            pop_name = path_name.pop()

            current_node_name = min_d_name
            node_names.remove(current_node_name)


        last_path = reversed(self.dijkstra(pop_name)[self.get_node(end_node_name)][1])

        for lp in last_path:
            path_name.append(lp.name)

        return path_name

    def check_adj(self, from_node:Node, to_node:Node):
        return True if from_node.get_adj(to_node) else False

    def show(self):
        for node in self.nodes:
            print(node)

    def show_matrix(self):
        for node in self.nodes:
            print('\t{}|'.format(node.name), end='')
        
        print('')

        for _ in range(len(self.nodes)):
            print('_________', end ='')

        print('')
        for node in self.nodes:
            print('{}|'.format(node.name), end='')
            for n in self.nodes:
                print('\t{}'.format(node.get_adj_weight(n.name)), end='')
            print('')


if __name__ == '__main__':
    ##### TEST CASE #####
    graph_set = {(1, 2), (1, 4), (2, 3), (5, 6)}
    network = {('J', 'M', 3),
                ('M', 'N', 1),
                ('P', 'M', 4), ('P', 'S', 7),
                ('K', 'J', 7), ('K', 'N', 9), ('K', 'M', 12), ('K', 'O', 4),
                ('N', 'P', 10),
                ('Q', 'O', 6), ('Q', 'R', 6),
                ('S', 'Q', 3), ('S', 'T', 11),
                ('L', 'K', 10), ('L', 'O', 5),
                ('O', 'Q', 8), ('O', 'R', 1),
                ('R', 'T', 9)}
    g = Graph(network, weighted=True)

    # g.dijkstra('J')
    # print(g.get_node('Q'))

    # g.get_route_lite('J', 'Q')
    # g.get_route_lite('J', 'N')
    # g.get_route_lite('O', 'T')

    print('\n\n\n\n\n')
    print('result')
    print(g.get_route(['J', 'P', 'Q', 'T']))

    ####################
