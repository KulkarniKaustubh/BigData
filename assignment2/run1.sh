#!/bin/sh

python3 map1.py < web-Google.txt > temp
echo "pushed web-Goolge.txt to MAPPER1 --> output to temp"
sort -o temp temp
echo "sorted temp"
python3 reduce1.py < temp v > adj_list
echo "pushed temp, passed v into REDUCER1 --> output to adj_list, initial v vector to file v"
sort -o adj_list adj_list
echo "sorted adj_list"
sort -o v v
echo "sorted v"

echo "RUN1 tasks done ::::  run RUN2"
