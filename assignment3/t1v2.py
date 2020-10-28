from pyspark import SparkContext
import sys

word=''
if sys.argv[1]:
	word=sys.argv[1]
path=''
if sys.argv[2]:
	path=sys.argv[2]

fil=path
sc=SparkContext('local',"task1")

rdd=sc.textFile(path)

mappedRdd=rdd.map(lambda x: x.split(','))
#print(mappedRdd.take(5))


columns={}
ind=0
for i in mappedRdd.first():
	columns[i]=ind
	ind+=1
#print(columns)

wordRdd=mappedRdd.filter(lambda x: x[columns['word']]==word)

recRdd=wordRdd.filter(lambda x: x[columns['recognized']]=='True')

#print(recRdd.take(5))

unrecRdd=wordRdd.filter(lambda x: x[columns['recognized']]=='False')

#print(unrecRdd.take(5))

avg_strokes_recRdd=recRdd.map(lambda x : int(x[columns['Total_Strokes']])).mean()
avg_strokes_unrecRdd=unrecRdd.map(lambda x : int(x[columns['Total_Strokes']])).mean()
print(avg_strokes_recRdd)
print(avg_strokes_unrecRdd)

