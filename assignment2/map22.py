#!/usr/bin/python3
import sys

path=''
if sys.argv[1]:
    path = sys.argv[1]  # will hold the path to the file v

rank_vector={} # will hold current page rank  
#new_vector=dict() # will hold the sum of contributions of each node that links to respective key

v_file=open(path,"r")

if v_file:

	lines=v_file.readlines()
	
	for line in lines:
		line=line.strip()
		key,value=line.split(', ')
		if key not in rank_vector:
			rank_vector[key]=float(value) # the rank is updated
v_file.close()
#print(new_vector)
for line in sys.stdin:
	
	line = line.strip()
	key,value=line.split('\t')
	
	print(key,"0",sep=",")
	value=value.strip(" []") # processing string
	
	value=value.split(',') # converting to list
	n=len(value)
	
	add=rank_vector[key]/float(n) 
	 #calculating contribution of key to every node it points to 
	
	
	for val in value: # updating sum of contributions
		val=val.strip()
		val=val.strip("'")
		
		if val in rank_vector:
			print(val,add,sep=',')
	
	
