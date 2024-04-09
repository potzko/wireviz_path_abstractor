import graph_lib
import sys
import re
line = re.compile("# *@ *length.*?\n")
def calc_path(text, graph):
    abstract_path = text.split("length", 1)[1][:-1]
    abstract_path = abstract_path.strip()
    abstract_path = abstract_path.replace('  ', ' ')
    abstract_path = abstract_path.split(" ")
    path_type = "path"
    node = None
    path_length = 0  
    ind_tmp = 0
    for ind, i in enumerate(abstract_path):
        if i in ["path", "dist", "connection_count"]:
            path_type = i
        else:
            node = i
            path = [i]
            ind_tmp = ind
            break
    for i in abstract_path[ind_tmp + 1:]:
        if i in ["path", "dist", "connection_count"]:
            path_type = i
        else:
            match path_type:
                case "path":
                    tmp_dist, tmp_path = graph.standard_path(node, i)
                    path += tmp_path
                    path_length += tmp_dist
                case "dist":
                    tmp_dist, tmp_path = graph.dist_path(node, i)
                    path += tmp_path
                    path_length += tmp_dist
                case "connection_count":
                    tmp_dist, tmp_path = graph.norm_path(node, i)
                    path += tmp_path
                    path_length += tmp_dist
            node = i
    return path, path_length


def format_file(address_file, address_data):
    with open(address_data, "r") as data_file:
        data = data_file.read()
    nodes = graph_lib.get_graph_text(data)

    with open(address_file, 'r') as unformated_file:
        text = unformated_file.read()
    paths = line.findall(text)
    unformated_out = line.sub(text, "{}")


def main(data_file_path, format_file_path, out_file = None):
    with open(data_file_path, "r") as data_file:
        data = data_file.read() + '\n'
    mode = data_file_path.split('.')[-1]
    nodes = graph_lib.get_graph_text(data, mode)
    with open(format_file_path, "r") as format_file:
        file = format_file.read()
    
    proccessed_length_arr = []
    for i in line.findall(file):
        proccessed_length_arr.append(calc_path(i, nodes))
    proccessed_length_arr = [f"length: {i[1]}   #path = {' -> '.join(i[0])}" for i in proccessed_length_arr]
    
    file = line.sub("{}\n", file)
    new_file = file.format(*proccessed_length_arr)

    if out_file == None:
        import os
        import shutil

        # ask for forgiveness not permission 🙏
        try:
            os.makedirs('default_out')
        except:
            pass

        shutil.rmtree('default_out')

        os.makedirs('default_out')
        with open("default_out\\tmp.yml", 'w') as out:
            out.write(new_file)
        
        os.system("wireviz default_out\\tmp.yml")

    else:
        with open(out_file, 'w') as out:
            out.write(new_file)

    
if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else: main(sys.argv[1], sys.argv[2])