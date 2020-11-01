from pyspark import SparkContext
import sys

word=''
if sys.argv[1]:
	word=sys.argv[1]
path=''
if sys.argv[3]: # might have to change it to argv[3]
	path=sys.argv[3]

fil=path
sc=SparkContext('local',"task1")

rdd=sc.textFile(path) # stores it as rdd automatically

mappedRdd=rdd.map(lambda x: x.split(',')) # stores it as 'list of lists' rdd
#print(mappedRdd.take(5))


columns={}
ind=0
for i in mappedRdd.first(): # stores indices of each column
	columns[i]=ind
	ind+=1
#print(columns)

wordRdd=mappedRdd.filter(lambda x: x[columns['word']]==word) #gets subset of data where the word attribute is the same as that provided as argument

recRdd=wordRdd.filter(lambda x: x[columns['recognized']]=='True') #filters out the recognized drawings

#print(recRdd.take(5))

unrecRdd=wordRdd.filter(lambda x: x[columns['recognized']]=='False') #filters out the unrecognized drawings

#print(unrecRdd.take(5))

avg_strokes_recRdd=recRdd.map(lambda x : int(x[columns['Total_Strokes']])).mean() #calculates the avg strokes for recognized == True
avg_strokes_unrecRdd=unrecRdd.map(lambda x : int(x[columns['Total_Strokes']])).mean() #calculates the avg strokes for recognized == False

print("{0:.5f}".format(avg_strokes_recRdd))
print("{0:.5f}".format(avg_strokes_unrecRdd))

