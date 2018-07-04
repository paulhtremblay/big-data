from pyspark import SparkContext, SparkConf

def read_from_local(path):
    #sc = SparkContext('local')
    conf = SparkConf().setAppName('Summer_Course').setMaster('local')
    sc = SparkContext(conf=conf)


    """
    spark = SparkSession.builder \
           .master("local") \
           .appName("Word Count") \
           .config("spark.some.config.option", "some-value") \
           .getOrCreate()
    """
    return sc.textFile('{path}'.format(path = path))

if __name__ == '__main__':
    rdd = read_from_local('/tmp/temp.txt')
    print(rdd.take(1))


