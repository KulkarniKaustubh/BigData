import sys

adj_list_dict = dict()

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if from_node not in adj_list_dict:          # if from_node not already in dict create a list with the to_node
        adj_list_dict[from_node] = [to_node]
    else:
        adj_list_dict[from_node].append(to_node) # if from_node already in dictionary append to node to its list


for key in adj_list_dict:
    print(key, adj_list_dict[key], sep = "\t", end = "\n")




