#!/usr/bin/python3
import sys
from functools import reduce

vect_nodes = {}

for line in sys.stdin:
	line = line.strip()
	k,v=line.split('\t') # v will contain the sum of contributions of every node that links to k
	
	v = float(v)
	if(k not in vect_nodes):
		vect_nodes[k] = []

	vect_nodes[k].append(v)


for node in sorted(vect_nodes):
	add = reduce((lambda a,b: a+b), vect_nodes[node])
	new = "{0:.5f}".format(0.15+(0.85*add))
	print(node,str(new),sep=', ')
