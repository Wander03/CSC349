import sys


class Vertex:
    def __init__(self, key):
        self.id = key
        self.edges = []
        self.degree = 0

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        else:
            return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def reset_edges(self):
        self.edges = []


class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.load_edges()

    def load_edges(self):
        for v in self.V:
            self.V[v].reset_edges()

        for edge in self.E:
            edge[0].edges.append(edge[1])
            edge[0].degree += 1

    def get_vertices(self):
        return self.V.values()

    def get_edges(self):
        return self.E


def read_in_file(filename):
    V = {}
    E = []
    new_lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            new_lines.append(lines[i].strip().split(sep=' '))

        for line in new_lines:
            if line[0] not in V:
                V[line[0]] = Vertex(int(line[0]))
            if line[1] not in V:
                V[line[1]] = Vertex(int(line[1]))
            E.append([V[line[0]], V[line[1]]])
            E.append([V[line[1]], V[line[0]]])
    E.sort()
    return Graph(V, E)


def smart_greedy_VC(G: Graph):
    C = []
    H = Graph(G.V.copy(), G.E.copy())

    while H.get_edges() != []:
        max_degree = 0
        v = None
        for vert in H.get_vertices():
            if vert.degree > max_degree:
                max_degree = vert.degree
                v = vert.id

        new_V = {}
        for vert in H.get_vertices():
            if vert.id != v:
                new_V[str(vert.id)] = vert

        new_E = []
        for e in H.get_edges():
            if H.V[str(v)] not in e:
                new_E.append(e)

        H = Graph(new_V, new_E)
        C.append(v)
    return C


def basic_greedy_VC(G: Graph):
    C = []
    H = Graph(G.V.copy(), G.E.copy())

    while H.get_edges() != []:
        (u, v) = H.get_edges()[0]

        new_E = []
        for e in H.get_edges():
            if u not in e and v not in e:
                new_E.append(e)

        new_V = {}
        for vert in H.get_vertices():
            for e in new_E:
                if (vert.id == e[0] or vert.id == e[1]) and vert not in new_V:
                    new_V[str(vert.id)] = vert

        H = Graph(new_V, new_E)
        C.append(u)
        C.append(v)
    return C


def VC_checker(G: Graph, C):
    covered = []
    for e in G.get_edges():
        for v in C:
            if v in e and e not in covered:
                covered.append(e)

    return len(covered) == len(G.get_edges())


def get_subsets(V, n):
    if n == 0:
        return [[]]

    subsets = []
    for i in range(len(V)):
        cur = V[i]
        rest = V[i+1:]
        rest_subsets = get_subsets(rest, n-1)

        for v in rest_subsets:
            subsets.append([cur, *v])

    return subsets


def brute_force_VC(G: Graph):
    for i in range(1, len(G.get_vertices())):
        subsets = get_subsets(list(G.get_vertices()), i)
        for s in subsets:
            if VC_checker(G, s):
                return s


def save_output(out, sg, bg, bf):
    with open('my' + out + '.txt', 'w') as f:
        f.write("log-Approximation: %s" % ' '.join([str(v) for v in sg])+"\n")
        f.write("2-Approximation: %s" % ' '.join([str(v) for v in bg])+"\n")
        f.write("Exact Solution: %s" % ' '.join([str(v) for v in bf]))


def main(argv):
    G = read_in_file(argv[1])
    sg = smart_greedy_VC(G)
    bg = basic_greedy_VC(G)
    bf = brute_force_VC(G)
    save_output(argv[1][-5], sg, bg, bf)
    print("log-Approximation: %s" % ' '.join([str(v) for v in sg]))
    print("2-Approximation: %s" % ' '.join([str(v) for v in bg]))
    print("Exact Solution: %s" % ' '.join([str(v) for v in bf]))


if __name__ == '__main__':
    main(sys.argv)
    # main([0, 'in1.txt', 'my1.txt'])
