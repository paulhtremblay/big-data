import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import datetime
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def count_us_ws(path):
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    rdd = sc.textFile('s3a://{path}'.format(path = path), 100)\
       .map(lambda x: parse_line.parse_line(x))
       
    df = rdd.toDF()
    df.write.parquet('s3a://paulhtremblay/parquet_test/new/{date}'.format(date = datetime.datetime.now()))
    pp.pprint(df.show())
    air_temperature_observation_air_temperature
    fixed_weather_station_ncei_wban_identifier

    """
    (df
        .write
        .partitionBy("favorite_color")
        .bucketBy(42, "name")
        .saveAsTable("people_partitioned_bucketed"))
    """


if __name__ == '__main__':
    #count_us_ws('paulhtremblay/noaa/data/1991')
    count_us_ws('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
        
