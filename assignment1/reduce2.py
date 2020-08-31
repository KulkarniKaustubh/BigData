#!/usr/bin/python
import sys
 
# maps words to their counts
country = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
 
    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue

    try:
        country[word] = country[word]+count
    except:
        country[word] = count
 
# Note: they are unsorted
for word in country.keys():
    print('%s,%s'% ( word, country[word])) 
    
