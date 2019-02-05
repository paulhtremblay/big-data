from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.streaming import StreamingContext
import datetime
from  pyspark.sql import SQLContext

# create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
sqlContext = SQLContext(sc)
ssc = StreamingContext(sc, 1)
# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
# split each line into words
words = lines.flatMap(lambda line: line.split(" "))
with open("test.txt" , 'w') as write_obj:
    write_obj.write('{t}'.format( t = dir(words)))


# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
def for_each_func(rdd):

    now = datetime.datetime.now().strftime('%Y_%m_%d_%M')
    path = 'output_{now}'.format(now = now)
    if rdd.count() == 0:
        return
    #rdd.toDF().write.mode("append")(path)
    rdd.toDF().write.mode('Append').format("csv").save(path)
    #df.write.mode('Overwrite').parquet('s3a://paulhtremblay/parquet_test/simple')
    #df.write.format("csv").save(filepath)


    #rdd.saveAsTextFile(path)
    """
    with open('test2.txt', 'w') as write_obj:
        write_obj.write('{d}\n'.format(d = dir(rdd)))
        assert False
    """

# Print the first ten elements of each RDD generated in this DStream to the console
#wordCounts.pprint()
wordCounts.foreachRDD(for_each_func)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
