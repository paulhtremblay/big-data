import datetime
import os

from pyspark import SparkContext

def read_from_s3(path):
    sc = SparkContext('local')
    return sc.textFile('s3a://{path}'.format(path = path))

if __name__ == '__main__':
    rdd = read_from_s3('paulhtremblay/noaa/data/1901/')
    print(rdd.take(1))


