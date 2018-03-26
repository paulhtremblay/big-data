import datetime
import os

from pyspark import SparkContext

sc = SparkContext('local')
rdd = sc.textFile('s3a://paulhtremblay/noaa/data/1901/')
print(rdd.take(1))


