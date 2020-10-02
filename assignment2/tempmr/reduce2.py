#!/usr/bin/python3
import sys
from functools import reduce

vect_nodes = {}
def ret_fin(x):
	return 0.15+(0.85*x)

for line in sys.stdin:
	line = line.strip()
	k,v=line.split('\t') # v will contain the sum of contributions of every node that links to k
	
	v = float(v)
	if(k not in vect_nodes):
		vect_nodes[k] = []
		vect_nodes[k].append(v)

	else:
		vect_nodes[k].append(v)


for node in sorted(vect_nodes):
	new = "{0:.5f}".format(ret_fin(reduce((lambda a,b: a+b), vect_nodes[node])))
	print(node,str(new),sep=', ')
