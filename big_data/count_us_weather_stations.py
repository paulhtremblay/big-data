import parse_line
from pyspark.sql import SparkSession
from pyspark import SparkContext
from  pyspark.sql import SQLContext
import pprint
pp = pprint.PrettyPrinter(indent = 4)


def count_us_ws(path):
    sc = SparkContext('local')
    num_records = sc.textFile('s3a://{path}'.format(path = path), 100)\
       .map(lambda x: parse_line.parse_line(x))\
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') != None )\
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') < 48 )\
       .filter(lambda x: x.get('geophysical_point_observation_longitude_coordinate') > 22 )\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') != None)\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') > -68)\
       .filter(lambda x: x.get('geophysical_point_observation_latitude_coordinate') > -117)\
       .count()
    #pp.pprint(rdd.take(1))
    #print(rdd.getNumPartitions())
    print(num_records)

if __name__ == '__main__':
    count_us_ws('paulhtremblay/noaa/data/2000')
    #count_us_ws('paulhtremblay/noaa/data/1901/029070-99999-1901.gz')
    #count_us_ws('paulhtremblay/noaa/data/1901')
