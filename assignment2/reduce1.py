#!/usr/bin/python3
import sys

path = ''
if sys.argv[1]:
    path = sys.argv[1]  # will hold the path to the file v


current = None

adj_list_dict = {}
vlist = []

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if from_node not in vlist:
        vlist.append(from_node)
        if current == from_node:
            adj_list.append(to_node)
        else:
            if current:
                adj_list.sort()
                print(from_node, adj_list, sep="\t", end="\n")
            current = from_node
            adj_list = []

if current == from_node:
    print(from_node, adj_list, sep="\t", end="\n")


v_file = open(path, "w")
if v_file:
    for key in from_node:
        # writes lines of adj_list to stdout
        v_file.write('{}, 1\n'.format(key))  # writes lines of V to file
v_file.close()
