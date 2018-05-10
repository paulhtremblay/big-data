import datetime
import os
from time import sleep

from pyspark import SparkContext
from pyspark.sql import SparkSession

def f(iterator):
    sleep(10)
    for x in iterator:
        yield x + 'c'

def f_(x):
    sleep(10)
    return x + 'c'

def read_local(path):
    sc = SparkContext('local')
    """
    spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
    rdd = spark.read.csv('{path}'.format(path = path))
    rdd2 = rdd.map(lambda x: x + 'c')
    return rdd2
    """
    rdd =  sc.textFile('{path}'.format(path = path))
    #rdd2 = rdd.map(lambda x: x + 'c')
    rdd2 = rdd.mapPartitions(f)
    #rdd2 = rdd.map(f)
    return rdd2

if __name__ == '__main__':
    rdd = read_local('perm_data/temp.csv')
    print(rdd.take(4))
