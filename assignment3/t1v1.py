from pyspark import SparkContext
from pyspark.sql import SparkSession
import sys

word=''
if sys.argv[1]:
	word=sys.argv[1]
path=''
if sys.argv[2]:
	path=sys.argv[2]

fil=path
sc=SparkContext('local',"task1")
spark = SparkSession.builder.master("local[1]").appName("task1").getOrCreate()

#data= spark.read.format("csv").option("header","False").load(path)
data=spark.read.csv(path)#.rdd.map(list).cache()

#print(type(data.select('_c0')))
print("--"*20)
print(data.show())
print("--"*20)

"""
subset=data['_c3'].filter(lambda d: d==word).cache()

recognized=subset['recognized'].filter(lambda d: d==True).cache()
not_recognized=subset['recognized'].filter(lambda d: d==False).cache()
"""
