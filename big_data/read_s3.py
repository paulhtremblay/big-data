from pyspark import SparkContext
from pyspark.sql import Row
from pyspark import SparkContext
import datetime
from  pyspark.sql import SQLContext
import datetime

#sc = SparkContext('local')
sc  = SparkContext(appName = "validation {0}".format(datetime.datetime.now()))
sqlContext = SQLContext(sc)
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "AKIAIY3EQMUFTAIYW6ZA")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "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")
#print(dir(sc))
rdd = sc.textFile('s3a://paulhtremblay/noaa/data/1901/')
#rdd = sc.wholeTextFiles("s3a://paulhtremblay/noaa_tmp/", 100000)
print(rdd.take(1))


