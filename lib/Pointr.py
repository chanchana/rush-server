
import lib.Graphr as gr
import tkinter as tk
import math


class Edge(object):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.weight = math.sqrt(
            (point2.position[0] - point1.position[0])**2 + (point2.position[1] - point1.position[1])**2)


class Point(object):
    def __init__(self, name, position):
        self.position = position
        # self.x = int(position[0])
        # self.y = int(position[1])
        self.name = name


class Pointr(object):

    def __init__(self):
        self.points = []
        self.point_of = {}
        self.edges = []
        self.graph = None
        self.root = None
        # self.canvas = None
        # self.point_of_node = None

    def add(self, name, position):
        'point (x, y)'
        new_point = Point(name, position)
        self.point_of[name] = new_point
        self.points.append(new_point)
        return new_point

    def get_point(self, name):
        return self.point_of[name]

    def add_edge_name(self, name1, name2):
        p1 = self.get_point(name1)
        p2 = self.get_point(name2)
        return self.add_edge(p1, p2)

    def add_edge(self, point1, point2):
        new_edge = Edge(point1, point2)
        self.edges.append(new_edge)
        return new_edge

    def initialize_graph(self):
        if not self.graph:

            # self.point_of_node = {}
            self.graph = gr.Graph(directed=False, weighted=True)

            for e in self.edges:
                # node1 = self.graph.add_node(e.point1)
                # node2 = self.graph.add_node(e.point1)

                # self.point_of_node[node1] = e.point1
                # self.point_of_node[node2] = e.point2
                self.graph.add_adj(e.point1.name, e.point2.name, e.weight)

        self.graph.show_matrix()

    def show_shortest(self, from_point):
        self.initialize_graph()

        self.graph.dijkstra(from_point.name)

    def show_route_lite(self, from_point_name, to_point_name):
        self.initialize_graph()
        self.gui_init()
        self.gui_create()
        try:
            values = self.graph.get_route_lite(from_point_name, to_point_name)
            nodes = values[1]

            if len(nodes) == 1:
                print('Not reachable')

            tmp = self.point_of[nodes[0].name]
            for n in nodes:
                point = self.point_of[n.name]
                self.gui_point(point, color='green')
                self.gui_edge_from_points(tmp, point, color='blue')

                tmp = point

            self.gui_show()

        except:
            print('No route')

    def show_route(self, point_names):
        self.initialize_graph()
        self.gui_init()
        self.gui_create()
        try:
            original_names = point_names.copy()
            path = self.graph.get_route(point_names)

            print(path)

            if len(path) == 0:
                print('Not reachable')

            tmp = self.point_of[path[0]]
            for p in path:
                point = self.point_of[p]
                
                self.gui_edge_from_points(tmp, point, color='blue')

                if p in original_names:
                    self.gui_point(point, color='blue')
                else:
                    self.gui_point(point, color='green')

                tmp = point

            self.gui_show()

        except:
            print('No route')

    ##### GUI #####

    def gui_init(self):

        def close_win(event):
            print("You hit return.")

        print('s')
        self.root = tk.Tk()
        self.root.bind('<Return>', close_win)
        self.root.bind('a', close_win)
        self.canvas = tk.Canvas(height=600, width=600)

        # coord = 10, 50, 240, 210
        # arc = canvas.create_arc(coord, start=0, extent=300, fill="blue")
        # # canvas.create_oval(10, 10, 30, 30, fill='red')
        # self.create_pin(canvas, (30, 30), 'test')
        # self.create_pin(canvas, (50, 30), 'test')
        # self.create_pin(canvas, (10, 90), 'test')
        # self.create_pin(canvas, (150, 150), 'test')

    def gui_create(self):
        for p in self.points:
            # print(p.position)
            self.gui_point(p)

        for e in self.edges:
            self.gui_edge(e)

        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()

    def gui_show(self):

        self.canvas.pack()
        self.root.mainloop()

        print('t')

    def gui_point(self, point, color='red'):
        self.create_pin(self.canvas, point.position, point.name, color)

    def gui_edge(self, edge, color='black'):
        self.create_line(self.canvas, edge, color)

    def gui_edge_from_points(self, point1, point2, color='black'):
        new_edge = Edge(point1, point2)
        self.create_line(self.canvas, new_edge, color)

    @staticmethod
    def create_pin(canvas, position, name, color):
        pin_size = 2
        print('TEST')
        print(position)
        tx, ty, bx, by = float(position[0]) - pin_size, float(position[1]) - pin_size, float(position[0]) + pin_size, float(position[1]) + pin_size
        canvas.create_oval(tx, ty, bx, by, fill=color)
        canvas.create_text(position[0], position[1], text=name)

    @staticmethod
    def create_line(canvas, edge, color):
        # pin_size = 5
        x1, y1, x2, y2 = edge.point1.position[0], edge.point1.position[1], edge.point2.position[0], edge.point2.position[1]
        canvas.create_line(x1, y1, x2, y2, fill=color)
        # canvas.create_text(position[0], position[1], text=name)
        
if __name__ == '__main__':

    pr = Pointr()
    # p1 = pr.add('1', (30, 40))
    # p2 = pr.add('2', (40, 40))
    # p3 = pr.add('3', (80, 40))
    # p4 = pr.add('4', (45, 60))
    # p5 = pr.add('5', (70, 60))

    import random

    points = []

    for i in range(30):
        x, y = random.randrange(10, 590), random.randrange(10, 590)
        p1 = pr.add(str(i), (x, y))
        print('(' + str(x) + ', ' + str(y) + ')')
        points.append(p1)

    for i in range(40):
        p1 = points[random.randint(0, len(points) - 1)]
        p2 = points[random.randint(0, len(points) - 1)]

        pr.add_edge(p1, p2)

    # pr.add_edge(p1, p2)
    # pr.add_edge(p2, p3)
    # pr.add_edge(p1, p4)
    # pr.add_edge(p2, p4)
    # pr.add_edge(p5, p3)
    # pr.add_edge(p4, p5)


    # pr.show()
    # pr.initialize_graph()
    # pr.show_shortest(p1)

    # pr.initialize_gui()
    # pr.gui_create()
    # pr.gui_show()

    # pr.gui_init()
    # pr.gui_create()
    # pr.gui_show()

    # pr.show_route_lite('1', '2')
    pr.show_route(['1', '2', '3', '4', '5'])



