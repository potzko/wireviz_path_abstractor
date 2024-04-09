from parse import parse_text as parse

def checked_merge(dict_a, dict_b):
    overlapping_keys = dict_a.keys() & dict_b.keys()
    if overlapping_keys:
        errors = []
        for i in overlapping_keys:
            errors.append(f"can't define {i} as {dict_a[i]} and as {dict_b[i]}")
        raise Exception(f"overlapping definitions: \n{'\n'.join(errors)}")
    return {**dict_a, **dict_b}

def push_arc(dict, a, b, val):
    if not a in dict:
        raise Exception(f"can't define arc on point {a} as it is not defined as a connection or a virtual point")
    if not b in dict:
        raise Exception(f"can't define arc on point {b} as it is not defined as a connection or a virtual point")
    if b in dict[a][1]:
        raise Exception(f"can't define arc {a} -> {b} as {val} and {dict[a][1][b]} at the same time")
    dict[a][1][b] = val
    dict[b][1][a] = val

def build_connections(tree):
    assert "connections" in tree
    nodes = {}
    for name in tree["connections"]:
        if name in nodes:
            raise Exception(f"defined {name} as a connection multiple times")
        nodes[name] = ['node', {}]
    return nodes

def build_virtual_points(tree):
    assert "virtual_points" in tree
    nodes = {}
    for name in tree["virtual_points"]:
        if name in nodes:
            raise Exception(f"defined {name} as a virtual_point multiple times")
        nodes[name] = ['virtual_point', {}]
    return nodes

def build_arcs(tree, nodes):
    assert "distances" in tree
    for a, b, length in tree["distances"]:
        push_arc(nodes, a, b, length)
    return nodes

def graph(tree):
    nodes = {}
    connection_graph = build_connections(tree)
    virtual_points_graph = build_virtual_points(tree)

    nodes = checked_merge(connection_graph, virtual_points_graph)
    nodes = build_arcs(tree, nodes)

    for i in nodes:
        nodes[i][1][i] = nodes[i][1].get(i, 0) 

    return nodes

def graph_text(text, mode):
    parsed_tree = parse(text, mode)
    return graph(parsed_tree)
