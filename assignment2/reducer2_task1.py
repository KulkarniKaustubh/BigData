import sys

keys=[]

for line in sys.stdin:
    line = line.strip()
    from_node, to_node = line.split('\t')

    if from_node not in keys:
        keys.append(from_node) # get unique values of from nodes
   

for key in keys:
    print(key, 1, sep=",",end="\n")
