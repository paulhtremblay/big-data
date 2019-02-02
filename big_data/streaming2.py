from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
from pyspark.sql.types import *
import sys
import time

spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

dataSchema = StructType([StructField('Arrival_Time',LongType(),True),
    StructField('Creation_Time',LongType(),True),
    StructField('Device',StringType(),True),
    StructField('Index',LongType(),True),
    StructField('Model',StringType(),True),
    StructField('User',StringType(),True),
    StructField('gt',StringType(),True),
    StructField('x',DoubleType(),True),
    StructField('y',DoubleType(),True),
    StructField('z',DoubleType(),True)
                     ])

streaming = spark.readStream.schema(dataSchema).option("maxFilesPerTrigger", 1)\
        .json( '/home/henry/projects/Spark-The-Definitive-Guide/data/activity-data_small')
        
spark.conf.set("spark.sql.shuffle.partitions", 5)
activityCounts = streaming.groupBy("gt").count()
activityQuery = activityCounts.writeStream.queryName("activty_counts").format("memory").outputMode("complete").start()

print('here0')
print('here1')
spark.streams.active
print('here2')
spark.sql("select * from activty_counts").show()
print('here3')
time.sleep(5)
print('sleeping for 5....')
spark.sql("select * from activty_counts").show()
print('sleeping for 5....')
spark.sql("select * from activty_counts").show()
activityQuery.awaitTermination()

