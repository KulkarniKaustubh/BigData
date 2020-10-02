#!/usr/bin/python3
import sys

path = ''
if sys.argv[1]:
	path = sys.argv[1]  # will hold the path to the file v

adj_list = []
v_file = open(path, "a")
prev_from_node = None

for line in sys.stdin:
	line = line.strip()
	from_node, to_node = line.split('\t')

	if prev_from_node != from_node:
		print(f'{from_node}\t{adj_list}')
		v_file.write(f'{from_node}, 1\n')
		adj_list = []

	prev_from_node = from_node
	adj_list.append(to_node)
if prev_from_node:
	print(f'{prev_from_node}\t{adj_list}')
	v_file.write(f'{prev_from_node}, 1\n')
