#!/bin/sh

if python3 map2.py < adj_list v > map2op; then
	echo "pushed adj_list, passed v into MAPPER2 --> output to map2op"
	sort -o map2op map2op
	echo "sorted map2op"
	python3 reduce2.py < map2op > v1
	echo "pushed map2op into REDUCER1 --> output to v1"
	sort -o v1 v1
	echo "sorted v1"
	cp v1 v
	echo "copied v1 to v"
else
	echo "failure $?"
fi
