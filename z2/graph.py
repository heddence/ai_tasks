class Graph:
    def __init__(self, graph={}):
        self.graph = graph

    def __str__(self):
        graph = ''
        for v in self.get_vertices():
            for a in self.get_adjacent(v):
                graph += f'({v}, {a}, {self.graph[v][a]})'
        return graph

    def set_vertex(self, vertex):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}
        return self

    def set_adjacent(self, vertex, adjacent, weight=0):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}
        if adjacent not in self.graph.keys():
            self.graph[adjacent] = {}

        self.graph[vertex][adjacent] = weight
        self.graph[adjacent][vertex] = weight
        return self

    def get_vertices(self):
        return list(self.graph.keys())

    def get_adjacent(self, vertex):
        if vertex in self.graph.keys():
            return self.graph[vertex]

    def get_path_cost(self, path):
        path_cost = 0
        for v, a in zip(path, path[1:]):
            path_cost += self.graph[v][a]
        return path_cost
