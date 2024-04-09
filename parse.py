from tokenizer import tokenizer

def parse_node(tok):
    return tok.eat("node")[1]

def parse_virtual_point(tok):
    return tok.eat("node")[1]

def parse_distance(tok):
    return float(tok.eat("distance")[1])

def parse_arc(tok):
    tok.eat("(")
    a = parse_node(tok)
    tok.eat(',')
    b = parse_node(tok)
    tok.eat(',')
    c = parse_distance(tok)
    tok.eat(")")
    return (a, b, c)

def parse_node_list(tok):
    tok.eat("{")
    ret_list = []
    if tok.peak_type() != "}":
        ret_list.append(parse_node(tok))
    while tok.peak_type() != "}":
        tok.optional_eat(",")
        if tok.peak_type() == "}":
            break
        ret_list.append(parse_node(tok))
    tok.eat("}")
    return ret_list

def parse_arc_list(tok):
    tok.eat("{")
    ret_list = []
    if tok.peak_type() != "}":
        ret_list.append(parse_arc(tok))
    while tok.peak_type() != "}":
        tok.optional_eat(",")
        if tok.peak_type() == "}":
            break
        ret_list.append(parse_arc(tok))
    tok.eat("}")
    return ret_list

def parse_virtual_point_list(tok):
    tok.eat("{")
    ret_list = []
    if tok.peak_type() != "}":
        ret_list.append(parse_virtual_point(tok))
    while tok.peak_type() != "}":
        tok.optional_eat(",")
        if tok.peak_type() == "}":
            break
        ret_list.append(parse_virtual_point(tok))
    tok.eat("}")
    return ret_list

def parse_connections_block(tok):
    tok.eat("connections")
    return {"connections": parse_node_list(tok)}

def parse_virtual_points_block(tok):
    tok.eat("virtual_points")
    return {"virtual_points": parse_virtual_point_list(tok)}

def parse_distance_block(tok):
    tok.eat("distances")
    return {"distances": parse_arc_list(tok)}

def parse_graphs(tok):
    return {**parse_connections_block(tok), **parse_virtual_points_block(tok), **parse_distance_block(tok)}

def parse(tok):
    return parse_graphs(tok)

def parse_text(text, mode):
    if mode == 'yml':
        return parse_text_yml(text)
    tok = tokenizer(text)
    ret = parse(tok)
    if tok.peak_type() != "EOF":
        raise Exception(f"text after finished parsing: {tok.remaining_text}")
    return ret

import yaml
def parse_text_yml(text):
    parsed_tree = yaml.safe_load(text)
    return parsed_tree
