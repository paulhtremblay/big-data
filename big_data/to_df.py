import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def to_df(path):
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    rdd = sc.textFile('s3a://{path}'.format(path = path))\
       .map(lambda x: parse_line.parse_line(x))\
       .filter(lambda x: x.get('air_temperature_observation_air_temperature') == -7.8)
    df = rdd.toDF()
    df.registerTempTable('my_table')
    df2 = sqlContext.sql("select * from my_table limit 1")
    return df


if __name__ == '__main__':
    #df  = to_df('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
    df  = to_df('paulhtremblay/noaa/data/1991')
        
