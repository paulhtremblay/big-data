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
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') != None )\
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') < -67 )\
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') > -125 )\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') != None)\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') < 48)\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') > 25)
    df = rdd.toDF()
    df.registerTempTable('my_table')
    df2 = sqlContext.sql(""" select distinct
    geophysical_point_observation_latitude_coordinate,
geophysical_point_observation_longitude_coordinate,
fixed_weather_station_usaf_master_station_catalog_identifier
from my_table
order by geophysical_point_observation_latitude_coordinate
    """)
    return df2


if __name__ == '__main__':
    #df  = to_df('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
    #df  = to_df('paulhtremblay/noaa/data/1930')
    df  = to_df('paulhtremblay/noaa/data/2000')
    df.repartition(1).write.mode('Overwrite').csv('temp_data')
