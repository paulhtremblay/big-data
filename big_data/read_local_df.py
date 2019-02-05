from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

spark = SparkSession.builder \
   .master("local") \
   .appName("Word Count") \
   .config("spark.some.config.option", "some-value") \
   .getOrCreate()

df = spark.read.csv('data/file1.csv')
dataSchema = df.schema
dataSchema
df.show()

