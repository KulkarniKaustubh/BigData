#!/usr/bin/python3
import sys

path=''
if sys.argv[1]:
    path = sys.argv[1]  # will hold the path to the file v

rank_vector=dict() # will hold current page rank  

v_file=open(path,"r")

if v_file:

	lines=v_file.readlines()
	
	for line in lines:
		line=line.strip()
		key,value=line.split(',')
		if key not in rank_vector:
			rank_vector[key]=float(value) # the rank is updated

new_vector=dict() # will hold the
for line in sys.stdin:
	
	line = line.strip()
	key,value=line.split('\t')
	
	value=value.strip('[')
	value=value.strip(']')
	
	value=value.split(',')
	n=len(value)
	
	add=rank_vector[key]/n
	
	for val in value:
		val=val.strip()
		if val not in new_vector:
			new_vector[val]=add
		else:
			new_vector[val]+=add

for key in new_vector:
	print(key,new_vector[key],sep=',')
	
	
