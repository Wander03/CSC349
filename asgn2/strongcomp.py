import sys

clock = 1
cycles = []


class Vertex:
    def __init__(self, key):
        self.id = key
        self.out_edges = []
        self.in_edges = []
        self.visited = False
        self.pre = None
        self.post = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        else:
            return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def discovered(self):
        self.visited = True

    def undiscovered(self):
        self.visited = False

    def get_out_edges(self):
        return self.out_edges

    def get_in_edges(self):
        return self.in_edges

    def set_pre(self, x):
        self.pre = x

    def set_post(self, x):
        self.post = x

    def get_pre(self):
        return self.pre

    def get_post(self):
        return self.post

    def reset_in_n_out(self):
        self.in_edges = []
        self.out_edges = []


class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.pre_visit_lst = []
        self.post_visit_lst = []
        self.tree_edges = []
        self.back_edges = []

    def load_edges(self):
        for v in self.V:
            self.V[v].reset_in_n_out()

        for edge in self.E:
            edge[0].out_edges.append(edge[1])
            edge[1].in_edges.append(edge[0])

    def get_vertices(self):
        return self.V.values()

    def get_edges(self):
        return self.E

    def get_pre_visit(self):
        return self.pre_visit_lst

    def add_pre_visit(self, v: Vertex):
        self.pre_visit_lst.append(v)

    def get_post_visit(self):
        return self.post_visit_lst

    def add_post_visit(self, v: Vertex):
        self.post_visit_lst.append(v)

    def pre_visit(self, v: Vertex):
        global clock
        v.set_pre(clock)
        self.add_pre_visit(v)
        clock += 1

    def post_visit(self, v: Vertex):
        global clock
        v.set_post(clock)
        self.add_post_visit(v)
        clock += 1

    def explore(self, v: Vertex):
        v.discovered()
        self.pre_visit(v)
        for u in v.get_out_edges():
            if not u.visited:
                self.tree_edges.append([v, u])
                self.explore(u)
        self.post_visit(v)

    def DFS(self):
        global clock
        clock = 1
        for v in self.get_vertices():
            v.undiscovered()
        for v in self.get_vertices():
            if not v.visited:
                self.explore(v)
        self.identify_back_edge()

    def identify_back_edge(self):
        for e in self.E:
            if (e not in self.tree_edges) and (e[0].get_post() < e[1].get_post()):
                self.back_edges.append(e)


def identify_cycle(G: Graph, back_edges):
    for back_edge in back_edges:
        for v in G.get_vertices():
            v.undiscovered()
        H = Graph(G.V.copy(), G.E.copy())
        cycle_helper(H, back_edge[1], back_edge[1], back_edge[0])


def cycle_helper(G: Graph, current: Vertex, start: Vertex, end: Vertex, path=None):
    global cycles
    if path is None:
        path = [end.id]
    current.discovered()
    if current == end:
        path.sort()
        if path in cycles:
            return
        cycles.append(path.copy())
        new_V = G.V.copy()
        new_E = G.E.copy()
        for v in path:
            remove = []
            if G.V[str(v)] not in [start, end]:
                for e in new_E:
                    if G.V[str(v)] in e:
                        remove.append(e)
                del new_V[str(v)]
                for r in remove:
                    new_E.remove(r)
        new_G = Graph(new_V, new_E)
        new_G.load_edges()
        new_G.DFS()
        identify_cycle(new_G, [[end, start]])
    for v in current.get_out_edges():
        if not v.visited:
            path.append(current.id)
            cycle_helper(G, v, start, end, path)
            path.remove(current.id)


def find_strong_comps(G: Graph):
    G.DFS()
    identify_cycle(G, G.back_edges)

    global cycles
    scc = []
    for c1 in cycles:
        for c2 in cycles:
            if len(set(c1).intersection(set(c2))) != 0:
                c1 = list(set(c1 + c2))
        if c1 not in scc:
            c1.sort()
            scc.append(c1)
    for v in G.get_vertices():
        if v.id not in (x for sub_lst in scc for x in sub_lst):
            scc.append([v.id])
    scc.sort()

    print('{!r} Strongly Connected Component(s):'.format(len(scc)))
    for cycle in scc:
        cycle = list(map(str, cycle))
        print(', '.join(cycle))


def read_in_file(filename):
    V = {}
    E = []
    new_lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            new_lines.append(lines[i].replace(' ', '').strip().split(sep=','))

        for line in new_lines:
            if line[0] not in V:
                V[line[0]] = Vertex(int(line[0]))
            if line[1] not in V:
                V[line[1]] = Vertex(int(line[1]))
            E.append([V[line[0]], V[line[1]]])
    return Graph(V, E)


def main(argv):
    graph = read_in_file(argv[1])
    graph.load_edges()
    find_strong_comps(graph)


if __name__ == '__main__':
    main(sys.argv)
