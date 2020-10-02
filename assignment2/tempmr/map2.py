#!/usr/bin/python3
import sys

path=''
if sys.argv[1]:
    path = sys.argv[1]  # will hold the path to the file v

rank_vector = {} # will hold current page rank 

v_file=open(path,"r")

if v_file:

	lines=v_file.readlines()
	
	for line in lines:
		line=line.strip()
		key,value=line.split(',')
		if key not in rank_vector:
			rank_vector[key]=float(value) # the rank is updated
v_file.close()

for line in sys.stdin:
	
	line = line.strip()
	key,value = line.split('\t')
	
	print('%s\t%s'%(str(key),str(0)))
	adj = [x.strip().strip('\'') for x in value.strip(']').strip('[').split(',')]
	n = len(adj)
	source_contrib = 1/n
	for node in adj:
		if node in rank_vector:
			print('%s\t%s'%(str(node), str(source_contrib*rank_vector[key])))