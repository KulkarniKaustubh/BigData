from operator import itemgetter
import sys

adj_list_dict = dict()

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if int(from_node) not in adj_list_dict:
        adj_list_dict[int(from_node)] = [int(to_node)]
    else:
        adj_list_dict[int(from_node)].append(int(to_node))


for key in adj_list_dict:
    print(key, adj_list_dict[key], sep = "\t", end = "\n")




