from pyspark import SparkContext
import sys

word=''
if sys.argv[1]:
	word=sys.argv[1]
	
if(sys.argv[2]):
	k = int(sys.argv[2])
	
path=''
if sys.argv[3]:
	path=sys.argv[3]

sc = SparkContext('local',"task2")

rdd = sc.textFile(path)
mappedRdd = rdd.map(lambda x: x.split(',')) #to send joined dataset here

columns={}
ind=0
for i in mappedRdd.first(): # stores indices of each column
	columns[i]=ind
	ind+=1

#They want only unrecognised, stroke<k ----- outputs
wordRdd = mappedRdd.filter(lambda x: x[columns['word']] == word) # I only want what word they passed in cmd arg line
un_recRdd = wordRdd.filter(lambda x: x[columns['recognized']] == 'False') # Now filter only False (unrecognised) columns

un_recRdd_k = un_recRdd.filter(lambda x: int(x[columns['Total_Strokes']]) < k) # filter only those which have strokes < k(passed in args)
ctry = un_recRdd_k.map(lambda x: (x[columns['countrycode']], 1)) # [(CA, 1), (US, 1), (CA, 1)]
count_ctry = ctry.reduceByKey(lambda x,y : (x+y) ).sortByKey()  # [(CA, 2), (US, 1)]

#print(count_ctry.collect())
for item in count_ctry.collect():
	print(f"{item[0]},{item[1]}")
