#!/usr/bin/python3
import sys
current=None
add=0
for line in sys.stdin:
	line = line.strip()
	
	k,v=line.split(',') # v will contain the sum of contributions of every node that links to k
	k=k.strip("'")
	if current==k:
		add+=float(v)
	else:
		
		if current:
			new="{0:.5f}".format(0.15+(0.85*(add)))
			print(f'{current},{new}')
		current=k
		add=float(v)
if current==k:
	new="{0:.5f}".format(0.15+(0.85*add))
	print(f'{current},{new}')
