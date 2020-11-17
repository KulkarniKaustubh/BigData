from pyspark import SparkContext
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType
import pandas

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

df1=df1[df1.word==word]
df2=df2[df2.word==word]

df1=df1.repartitionByRange(100,'key_id')
df2=df2.repartitionByRange(100,'key_id')

# print(df1.show())
# print('-'*70)
# print(df2.show())

temp_df1=df1.alias('temp_df1')
temp_df2=df2.alias('temp_df2')

fdf=temp_df1.join(temp_df2, temp_df1.key_id==temp_df2.key_id)
fdf=fdf[fdf.recognized=='False']
fdf = fdf.withColumn("Total_Strokes", fdf["Total_Strokes"].cast(IntegerType()))
fdf=fdf[fdf.Total_Strokes<k]
cc=fdf.groupBy("countrycode").count().sort("countrycode")
pcc=cc.toPandas()
for i in range(len(pcc)) :
    print(pcc.loc[i, "countrycode"], pcc.loc[i, "count"])
# print(cc.show())
