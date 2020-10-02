#!usr/bin/python3
import sys

path = ''
if sys.argv[1]:
	path = sys.argv[1]

node_ranks = {}
new_node_ranks = {}

with open(path, 'r') as v_file:
	lines = v_file.readlines()

	for line in lines:
		node, rank = line.split(', ')
		node_ranks[node] = float(rank)
		new_node_ranks[node] = 0

for line in sys.stdin:
	line = line.strip()

	node, adj_list = line.split('\t')
	adj_list = adj_list.strip('[]').split(', ')

	num_outgoing = len(adj_list)

	new_rank = node_ranks[node]/num_outgoing

	for val in adj_list:
		new_node_ranks[val] += new_rank

for node in node_ranks:
	print(f'{node}, {node_ranks[node]}')
