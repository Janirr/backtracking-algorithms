import random
import time
import sys

sys.setrecursionlimit(10000000)


class Graph:

    def __init__(self, edges_array):
        self.n = 0
        self.edges = edges_array
        self.undirected_graph = []
        self.directed_graph = []
        self.hasHamCycleUndirected = False
        self.hasHamCycleDirected = False
        self.hasEulerCycleUndirected = False
        self.hasEulerCycleDirected = False

    def insertValues(self):
        leave = False
        while not leave:
            print("Connections:", *self.edges)
            print("To go back, please press enter without any values\n")
            edge = []
            try:
                edge = list(map(int, input("Pass 2 numbers separated by space: ").split()))
                if len(edge) == 2:
                    self.edges.append(edge)
            except ValueError:
                print('Incorrect value')
            if not edge:
                leave = True
                print("\n")

    def connections(self):
        print("Connections:", *self.edges)

    def reset(self):
        self.hasHamCycleUndirected = False
        self.hasHamCycleDirected = False
        self.hasEulerCycleUndirected = False
        self.hasEulerCycleDirected = False

    def createGraph(self):
        self.reset()
        if len(self.edges) > 0:
            vertexes = []
            if len(self.edges) > 0:
                print(self.edges)
                for i in range(len(self.edges)):
                    vertexes.append(self.edges[i][0])
                    vertexes.append(self.edges[i][1])
                self.n = len(set(vertexes))
                self.undirected_graph = [[0] * self.n for _ in range(self.n)]
                self.directed_graph = [[] * self.n for _ in range(self.n)]
                for i in range(len(self.edges)):
                    x = self.edges[i][0] - 1
                    y = self.edges[i][1] - 1
                    self.undirected_graph[x][y] = 1
                    self.undirected_graph[y][x] = 1
                    self.directed_graph[x].append(y)
                print("\n-- UNDIRECTED GRAPH --")
                print(*self.undirected_graph, sep="\n")
                print("\n-- DIRECTED GRAPH --")
                print(*self.directed_graph)
                for j in range(self.n):
                    print(j, self.directed_graph[j], sep="->")

    def randomGraph(self, n, s):
        edges_list = []
        max_edges = (n * (n - 1))
        for i in range(n):
            for j in range(n):
                if i != j:
                    edge = [i + 1, j + 1]
                    edges_list.append(edge)
        random_list_directed = random.sample(range(1, max_edges), int(abs(s - 100) / 100 * max_edges))
        random_list_directed.sort(reverse=True)
        for i in random_list_directed:
            edges_list.pop(i)
        self.edges = edges_list
        self.undirected_graph = [[0] * self.n for _ in range(self.n)]
        self.directed_graph = [[] * self.n for _ in range(self.n)]
        for i in range(len(self.edges)):
            x = self.edges[i][0] - 1
            y = self.edges[i][1] - 1
            self.undirected_graph[x][y] = 1
            self.undirected_graph[y][x] = 1
            self.directed_graph[x].append(y)

    def tests(self):
        functions = ['self.EulerCycleDirected()', 'self.EulerCycleUndirected()', 'self.hamCycleDirected()',
                     'self.hamCycleUndirected()']
        files = ['EulerDirected.txt', 'EulerUndirected.txt', 'HamiltonDirected.txt', 'HamiltonUndirected.txt']
        for l in range(len(functions)):
            file = open("tests/" + files[l], "w")
            file.write("time[ms];n;s\n")
            for i in range(10, 40, 10):
                for j in range(10, 100, 10):
                    self.n = i
                    for k in range(10):
                        self.randomGraph(i, j)
                        start = time.time()
                        self.reset()
                        exec(functions[l])
                        end = time.time()
                        file.write('{};{};{}\n'.format((end - start) * 1000, i, j))
                        print('{};{};{}'.format((end - start) * 1000, i, j))
            file.close()

    def readFile(self):
        print("Press ENTER to go back")
        option = ' '
        while option != '':
            option = input("Enter file name: ")
            try:
                self.clearArray()
                f = open(option)
                self.edges = []
                self.n, k = map(int, f.readline().split())
                for i in range(k):
                    connection = list(map(int, f.readline().split()))
                    self.edges.append(connection)
                print("Data has been imported correctly\n")
                option = ''
                f.close()
            except IOError:
                print("File cannot be read\n")

    def deleteLastEdge(self):
        if len(self.edges) > 0:
            print("Deleted element: ", self.edges[-1])
            self.reset()
            self.edges.pop()

    def clearArray(self):
        self.edges = []
        self.undirected_graph = []
        self.directed_graph = []
        self.reset()

    def isSafe(self, v, path, pos):
        if self.undirected_graph[path[pos - 1]][v] == 0:
            return False
        for i in range(pos):
            if path[i] == v:
                return False
        return True

    # Hamiltonian Cycles
    def HamCycles(self):
        self.hamCycleDirected()
        self.hamCycleUndirected()

    # Undirected Hamiltonian Cycle
    def hamCycleUndirected(self):
        if len(self.undirected_graph) > 0:
            path = [0]  # Starting from first value
            visited = [False] * (len(self.undirected_graph))
            for i in range(len(visited)):
                visited[i] = False
            visited[0] = True
            self.findHamCycleUndirected(1, path, visited)
            if not self.hasHamCycleUndirected:
                print("Undirected: Graf wejściowy nie zawiera cyklu.")

    def findHamCycleUndirected(self, pos, path, visited):
        if not self.hasHamCycleUndirected:
            if pos == len(self.undirected_graph):  # Found a cycle
                if self.undirected_graph[path[-1]][path[0]] != 0:
                    self.hasHamCycleUndirected = True
                    path.append(0)
                    list_from_1 = list(map(lambda num: num + 1, path))
                    print("Undirected hamiltonian cycle:", list_from_1)
                    path.pop()
                return
            for v in range(len(self.undirected_graph)):
                if self.isSafe(v, path, pos) and not visited[v]:
                    path.append(v)
                    visited[v] = True
                    self.findHamCycleUndirected(pos + 1, path, visited)
                    visited[v] = False
                    path.pop()
        else:
            return

    # Directed Hamiltonian Cycle
    def hamCycleDirected(self):
        if len(self.directed_graph) > 0:
            path = [0]  # Starting from first value
            visited = [False] * (len(self.undirected_graph))
            visited[0] = True
            self.findHamCycleDirected(0, path, visited)
            if not self.hasHamCycleDirected:
                print("Directed hamiltionian cycle: Graf wejściowy nie zawiera cyklu.")

    def findHamCycleDirected(self, pos, path, visited):
        if not self.hasHamCycleDirected:
            if len(path) == len(self.directed_graph) and path[0] in self.directed_graph[path[-1]]:  # Found a cycle
                self.hasHamCycleDirected = True
                list_from_1 = list(map(lambda num: num + 1, path))
                print("Directed hamiltonian cycle:", list_from_1)
                path.pop()
                return
            for v in range(len(self.directed_graph[pos])):
                if not visited[self.directed_graph[pos][v]]:
                    path.append(self.directed_graph[pos][v])
                    visited[self.directed_graph[pos][v]] = True
                    self.findHamCycleDirected(self.directed_graph[pos][v], path, visited)
                    visited[self.directed_graph[pos][v]] = False
                    path.pop()
        else:
            return

    # Euler Cycles
    def EulerCycles(self):
        self.EulerCycleDirected()
        self.EulerCycleUndirected()

    # Directed Euler Cycle
    def EulerCycleDirected(self):
        if len(self.directed_graph) > 0:
            possible = True
            x = self.n + 1
            ins = [0] * x
            outs = [0] * x
            for i in range(len(self.edges)):
                ins[self.edges[i][0]] += 1
                outs[self.edges[i][1]] += 1
            for i in range(len(self.directed_graph)):
                if len(self.directed_graph) == 0:
                    possible = False
            if ins == outs and possible:
                max_node = len(self.directed_graph)
                visited_edge = [[False for _ in range(max_node + 1)] for _ in range(max_node + 1)]
                path = self.DFSDirected(0, visited_edge)
                list_from_1 = list(map(lambda num: num + 1, path))
                print("Euler Directed:", list_from_1)
            else:
                print("Euler Directed: Graf wejściowy nie zawiera cyklu")

    def DFSDirected(self, u, visited_edge, path=None):
        if path is None:
            path = []
        path = path + [u]
        for v in self.directed_graph[u]:
            if visited_edge[u][v] is False:
                visited_edge[u][v], visited_edge[v][u] = True, True
                path = self.DFSDirected(v, visited_edge, path)
        return path

    # Undirected Euler Cycle
    def EulerCycleUndirected(self):
        if len(self.undirected_graph) > 0:
            possible = True
            max_node = len(self.undirected_graph)
            for i in range(max_node):
                if (self.undirected_graph[i].count(1) - self.undirected_graph[i][i]) % 2 == 1:
                    possible = False
            if possible:
                visited_edge = [[False for _ in range(max_node + 1)] for _ in range(max_node + 1)]
                path = self.DFSUndirected(0, visited_edge, [])
                self.hasEulerCycleUndirected = True
                list_from_1 = list(map(lambda num: num + 1, path))
                print("Undirected Euler:", list_from_1)
            else:
                print("Undirected Euler: Graf wejściowy nie zawiera cyklu.")

    def DFSUndirected(self, u, visited_edge, path):
        path = path + [u]
        for v in range(len(self.undirected_graph[u])):
            if not visited_edge[u][v] and self.undirected_graph[u][v] == 1:
                visited_edge[u][v], visited_edge[v][u] = True, True
                path = self.DFSUndirected(v, visited_edge, path)
        return path
