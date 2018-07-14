import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def two_stages(path1, path2):
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    rdd1 = sc.textFile('s3a://{path}'.format(path = path1))
    rdd2 = sc.textFile('s3a://{path}'.format(path = path2))
    union_rdd = rdd1.union(rdd2)
    union_rdd.count()


if __name__ == '__main__':
    two_stages('paulhtremblay/noaa/data/2000', 'paulhtremblay/noaa/data/1999')
