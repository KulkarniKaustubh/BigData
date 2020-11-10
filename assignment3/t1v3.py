from pyspark import SparkContext
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, avg

word=''
if sys.argv[1]:
	word=sys.argv[1]

path=''
if sys.argv[3]: # might have to change it to argv[3]
	path=sys.argv[3]


sc=SparkContext('local',"task1")

rdd=sc.textFile(path) # stores it as rdd automatically

mappedRdd=rdd.map(lambda x: x.split(',')) # stores it as 'list of lists' rdd
#print(mappedRdd.take(5))

spark = SparkSession(sc)

header=mappedRdd.first()
fields = [StructField(field_name, StringType(), True) for field_name in header]
schema = StructType(fields)
frdd=mappedRdd.filter(lambda row:row != header)
df=spark.createDataFrame(frdd,schema=schema)

fbyword=df.filter(df.word==word)

rec=fbyword.filter(fbyword.recognized==True)
unrec=fbyword.filter(fbyword.recognized==False)

#print(rec.show())
print(rec.agg(avg(rec.Total_Strokes)).show())
