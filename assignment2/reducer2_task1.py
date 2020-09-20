from operator import itemgetter
import sys

adj_list_dict = dict()

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if int(from_node) not in adj_list_dict:
        adj_list_dict[int(from_node)] = 1
    else:
        adj_list_dict[int(from_node)] = adj_list_dict[int(from_node)] + 1


for key in adj_list_dict:
    print(key, 1/adj_list_dict[key], sep=", ",end="\n")