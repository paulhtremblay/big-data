import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def read_pq():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL data source example") \
        .getOrCreate()
    df = spark.read.parquet('s3a://paulhtremblay/parquet_test/no_partition')
    df.createOrReplaceTempView("weather")
    max_df = spark.sql("SELECT max(int_temp) FROM weather")
    max_df.show()


if __name__ == '__main__':
    read_pq()
        
