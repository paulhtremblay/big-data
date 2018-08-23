from pyspark import SparkContext

def read_from_local(path):
    sc = SparkContext('local')
    conf = sc._jsc.hadoopConfiguration()
    conf.set("textinputformat.record.delimiter", "\n\n\n")
    return sc.textFile('{path}'.format(path = path))

if __name__ == '__main__':
    rdd = read_from_local('/tmp/temp.txt')
    print(rdd.take(1))


