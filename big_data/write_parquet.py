import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import datetime
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def write_to_parquet(path):
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    rdd = sc.textFile('s3a://{path}'.format(path = path), 100)\
       .map(lambda x: parse_line.parse_line(x))
    df = rdd.toDF()
    df.write.mode('Overwrite').parquet('s3a://paulhtremblay/parquet_test/simple')

    """
    (df
        .write
        .partitionBy("favorite_color")
        .bucketBy(42, "name")
        .saveAsTable("people_partitioned_bucketed"))
    """


if __name__ == '__main__':
    write_to_parquet('paulhtremblay/noaa/data/2000')
    #write_to_parquet('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
