from graph_build import graph_text

class graph:
    def __init__(self, nodes) -> None:
        self.nodes = nodes
        self.processed_graph = {}
        for node in self.nodes:
            self.processed_graph[node] = min_path_finder(nodes, node)
        tmp = get_normalized_graph(nodes)
        self.processed_graph_normalised = {}
        for node in tmp:
            self.processed_graph_normalised[node] = min_path_finder(tmp, node)
    
    def standard_path(self, start, target):
        if not start in self.nodes:
            raise Exception(f"node {start} is not a connection or virtual point")
        if not target in self.nodes[start][1]:
            raise Exception(f"tried following the path {start} -> {target} however {start} -> {target} does not exist")
        return self.nodes[start][1][target], [target]

    def dist_path(self, start, target):
        if not start in self.processed_graph:
            raise Exception(f"node {start} is not a connection or virtual point")
        if not target in self.processed_graph[start]:
            raise Exception(f"no path exists from {start} to {target}")
        return self.processed_graph[start][target]
    
    def norm_path(self, start, target):
        if not start in self.processed_graph_normalised:
            raise Exception(f"node {start} is not a connection or virtual point")
        if not target in self.processed_graph_normalised[start]:
            raise Exception(f"no path exists from {start} to {target}")
        return self.processed_graph_normalised[start][target]
                             
def min_path_finder(graph, a):
    # uses dijkstra's algorithm
    # assumes no negative arc
    # will hang on negative cycle
    nodes = graph
    min_distance = {}
    min_distance[a] = [0, []]
    known_distance = [(0, a, [])]
    while known_distance:
        min_node = min(known_distance)
        known_distance.remove(min_node)
        length, name, path = min_node
        node_arcs = nodes[name][1]
        for target, arc_len in node_arcs.items():
            if target in min_distance:
                if min_distance[target][0] > length + arc_len:
                    min_distance[target] = (length + arc_len, path + [name])
            else:
                min_distance[target] = [length + arc_len, path + [name]]
                known_distance.append((length + arc_len, target, path + [name]))
    for i in min_distance:
        min_distance[i][1] = min_distance[i][1][1:] + [i]
    return min_distance

def get_normalized_graph(nodes):
    ret_nodes = {}
    for i, rest in nodes.items():
        ret_nodes[i] = [rest[0], {ii: 1 for ii in rest[1]}]
    return(ret_nodes)

def get_graph_text(text, mode):
    nodes = graph_text(text, mode)
    return graph(nodes)

    

