from collections import defaultdict

class Graph:
    def __init__(self):
        # Create our graph as a defaultdict of lists
        self.graph = defaultdict(list)
        # Initialize variables to use for Tarjan's algorithm
        self.index = 0
        self.stack = []
        self.index_map = {}
        self.low_link = {}
        self.on_stack = {}
        self.sccs = []

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def strongconnect(self, v):
        # Set the depth index for v to the smallest unused index
        self.index_map[v] = self.index
        self.low_link[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack[v] = True

        # Consider successors of v
        for w in self.graph[v]:
            if w not in self.index_map:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(w)
                self.low_link[v] = min(self.low_link[v], self.low_link[w])
            elif self.on_stack[w]:
                # Successor w is in the stack and hence in the current Strongly Connected Component
                self.low_link[v] = min(self.low_link[v], self.index_map[w])

        # If v is a root node, pop the stack and generate an Strongly Connected Component
        if self.low_link[v] == self.index_map[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            self.sccs.append(scc)

    def find_sccs(self):
        # Find all strongly connected components
        for v in list(self.graph):  # Convert to list to avoid size change issues
            if v not in self.index_map:
                self.strongconnect(v)
        return self.sccs

    def compress_graph(self):
        # Map each node to its Strongly Connected Component index
        scc_map = {}
        for i, scc in enumerate(self.sccs):
            for node in scc:
                scc_map[node] = i

        # Create a compressed graph where each Strongly Connected Component is a single node
        compressed_graph = defaultdict(set)
        for u in self.graph:
            for v in self.graph[u]:
                if scc_map[u] != scc_map[v]:
                    compressed_graph[scc_map[u]].add(scc_map[v])

        return compressed_graph

    def find_zero_in_degree_nodes(self, compressed_graph, start_scc):
        # Calculate in-degrees for each node in the compressed graph
        in_degree = defaultdict(int)
        for u in compressed_graph:
            for v in compressed_graph[u]:
                in_degree[v] += 1

        # Find nodes with zero in-degree that are not the starting Strongly Connected Component
        zero_in_degree_nodes = [node for node in compressed_graph if in_degree[node] == 0 and node != start_scc]
        return zero_in_degree_nodes

    def min_routes_to_add(self, start_node):
        # Find Strongly Connected Components and compress the graph
        self.find_sccs()
        compressed_graph = self.compress_graph()
        # Identify the Strongly Connected Component containing the start node
        start_scc = next(i for i, scc in enumerate(self.sccs) if start_node in scc)
        # Find zero in-degree nodes in the compressed graph
        zero_in_degree_nodes = self.find_zero_in_degree_nodes(compressed_graph, start_scc)

        return len(zero_in_degree_nodes)

g = Graph()
g.add_edge('EWR', 'HND')
g.add_edge('HND','ICN')
g.add_edge('ICN','JFK')
g.add_edge('HND','JFK')
g.add_edge('JFK','LGA')
g.add_edge('BGI','LGA')
g.add_edge('ORD','BGI')
g.add_edge('DSM','ORD')
g.add_edge('SFO','DSM')
g.add_edge('SFO','SAN')
g.add_edge('SAN','EYW')
g.add_edge('EYW','LHR')
g.add_edge('LHR','SFO')
g.add_edge('TLV','DEL')
g.add_edge('DEL','DOH')
g.add_edge('DEL','CDG')
g.add_edge('CDG','SIN')
g.add_edge('SIN','CDG')
g.add_edge('CDG','BUD')

start_node = "EWR"
min_routes = g.min_routes_to_add(start_node)
print(f"Minimum routes to add to graph: {min_routes}")
