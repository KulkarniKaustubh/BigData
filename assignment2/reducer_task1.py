import sys

path = ''
if sys.argv[1]:
    path = sys.argv[1]  # will hold the path to the file v

adj_list_dict = dict()

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if from_node not in adj_list_dict:          # if from_node not already in dict create a list with the to_node
        adj_list_dict[from_node] = [to_node]
    else:
        # if from_node already in dictionary append to node to its list
        adj_list_dict[from_node].append(to_node)

v_file = open(path, "w")
if v_file:
    for key in adj_list_dict:
        # writes lines of adj_list to stdout
        adj_list_dict[key].sort() #sorting list
        print(key, adj_list_dict[key], sep="\t", end="\n")
        v_file.write('{},1\n'.format(key))  # writes lines of V to file
