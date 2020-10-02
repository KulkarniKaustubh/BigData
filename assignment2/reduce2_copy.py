#!/usr/bin/python3
import sys

prev_k = None
add = 0

for line in sys.stdin:
	line = line.strip()

	k, v = line.split(',') # v will contain the sum of contributions of every node that links to k
	#k = k.strip("'")

	if prev_k and prev_k != k:
		new="{0:.5f}".format(0.15+(0.85*add))
		print(f'{prev_k}, {new}')
		add = 0

	prev_k = k
	add += float(v)

if prev_k:
	new="{0:.5f}".format(0.15+(0.85*add))
	print(f'{prev_k}, {new}')
