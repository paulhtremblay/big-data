import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
from pyspark.sql.functions import exp
from pyspark.sql.types import IntegerType
import datetime
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def count_us_ws(path):
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    rdd = sc.textFile('s3a://{path}'.format(path = path), 100)\
       .map(lambda x: parse_line.parse_line(x))
       
    df = rdd.toDF()
    df_with_int_temp = df.withColumn("int_temp", df["air_temperature_observation_air_temperature"].cast(IntegerType()))
    df_with_int_temp.write.mode('Overwrite').parquet('s3a://paulhtremblay/parquet_test/no_partition'.format(date = datetime.datetime.now()))
    #df.printSchema()
    #sqlContext.registerDataFrameAsTable(df_with_int_temp, 'weather')
    #new_df = sqlContext.sql("SELECT max(int_temp) FROM weather")
    #new_df.show()
    
    #air_temperature_observation_air_temperature
    #fixed_weather_station_ncei_wban_identifier
    #print(dir(df_with_int_temp.write))
    df_with_int_temp.write.mode('Overwrite').partitionBy("int_temp").parquet("s3a://paulhtremblay/parquet_test/partition")

    """
    (df
        .write
        .partitionBy("fixed_weather_station_ncei_wban_identifier")
        .bucketBy(42, "name")
        .saveAsTable("people_partitioned_bucketed"))
    """


if __name__ == '__main__':
    #count_us_ws('paulhtremblay/noaa/data/1991')
    count_us_ws('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
        
