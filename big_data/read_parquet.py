import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def count_us_ws(path):
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL data source example") \
        .getOrCreate()
    parquetFile = spark.read.parquet('s3a://paulhtremblay/parquet_test/new')
    print(type(parquetFile))


if __name__ == '__main__':
    #count_us_ws('paulhtremblay/noaa/data/1991')
    count_us_ws('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
        
