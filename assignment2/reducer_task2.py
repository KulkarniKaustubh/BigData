#!/usr/bin/python3
import sys

for line in sys.stdin:
	line = line.strip()
	
	k,v=line.split(',') # v will contain the sum of contributions of every node that links to k
	k=k.strip("\'")
	add=0.15+(0.85*float(v)) # calculating new rank
	add=float("{:.5f}".format(add))
	print(k,add,sep=',')
