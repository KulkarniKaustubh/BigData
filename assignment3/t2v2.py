from pyspark import SparkContext
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import StringType

def f(x):
    d = {}
    for i in range(len(x)):
        d[str(i)] = x[i]
    return d

word=''
if sys.argv[1]:
	word=sys.argv[1]
	
if(sys.argv[2]):
	k = int(sys.argv[2])
	
data1=''
if sys.argv[3]:
	data1=sys.argv[3]

data2=''
if sys.argv[4]:
	data2=sys.argv[4]

sc = SparkContext('local',"task2")

#rdd1 = sc.textFile("shape_stat.csv")
#rdd2 = sc.textFile("shape.csv")
rdd1 = sc.textFile(data2)
rdd2 = sc.textFile(data1)

mappedRdd1 = rdd1.map(lambda x: x.split(','))
mappedRdd2 = rdd2.map(lambda x: x.split(','))


spark = SparkSession(sc)

header=mappedRdd1.first()
fields = [StructField(field_name, StringType(), True) for field_name in header]
schema = StructType(fields)
frdd1=mappedRdd1.filter(lambda row:row != header)
df1=spark.createDataFrame(frdd1,schema=schema)


header=mappedRdd2.first()
fields = [StructField(field_name, StringType(), True) for field_name in header]
schema = StructType(fields)
frdd2=mappedRdd2.filter(lambda row:row != header)
df2=spark.createDataFrame(frdd2,schema=schema)


df1=df1.repartitionByRange(100,'key_id')
df2=df2.repartitionByRange(100,'key_id')

print(df1.show())
print('-'*70)
print(df2.show())
"""
columns1={}
ind=0
for i in mappedRdd1.first(): # stores indices of each column
	columns1[i]=ind
	ind+=1

columns2={}
ind=0
for i in mappedRdd2.first(): # stores indices of each column
	columns2[i]=ind
	ind+=1
'''
columns1
{'word': 0, 'timestamp': 1, 'recognized': 2, 'key_id': 3, 'Total_Strokes': 4}

columns2
{'word': 0, 'countrycode': 1, 'key_id': 2}
'''


pairRdd1 = mappedRdd1.map(lambda x: (x[columns1['key_id']], x)) #this is to join based on key = 'key_id'
pairRdd2 = mappedRdd2.map(lambda x: (x[columns2['key_id']], x))

joinrdd = pairRdd1.join(pairRdd2)
fil_joinrdd = joinrdd.map(lambda x: (x[1][0], x[1][1][columns2['countrycode']]))

'''
joinrdd
[('4665167562407936', (['alarm clock', '2017-03-28 20:20:50.81058 UTC','True', '4665167562407936','7'], ['alarm clock', 'GB','4665167562407936']))]

fil_joinrdd
[(['alarm clock', '2017-03-28 20:20:50.81058 UTC', 'True', '4665167562407936', '7'], 'GB')]
'''


wordRdd = fil_joinrdd.filter(lambda x: x[0][columns1['word']] == word)
un_recRdd = wordRdd.filter(lambda x: x[0][columns1['recognized']] == 'False')

'''
un_recRdd (only contains recognized = false and word = word )
[(['ambulance', '2017-03-03 11:47:22.79851 UTC', 'True', '5689948554395648', '7'], 'GB')]
'''


un_recRdd_k = un_recRdd.filter(lambda x: int(x[0][columns1['Total_Strokes']]) < k)
'''
un_recRdd_k (only < k strokes)
[(['ambulance', '2017-03-22 07:01:25.66032 UTC', 'True', '4930758240108544', '4'], 'KR')]
'''

ctry = un_recRdd_k.map(lambda x: (x[1], 1))
'''
[(CA, 1), (US, 1), (CA, 1)]
'''

count_ctry = ctry.reduceByKey(lambda x,y : (x+y) ).sortByKey()
'''
[(CA, 2), (US, 1)]
'''

#print(count_ctry.collect())
for item in count_ctry.collect():
	print(f"{item[0]},{item[1]}")
"""
