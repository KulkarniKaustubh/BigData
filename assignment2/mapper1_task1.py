import sys

for line in sys.stdin:

    line = line.strip()
    words = line.split()
    if len(words) == 2 and words[0] != '#':
        print(words[0],words[1], sep = "\t")
