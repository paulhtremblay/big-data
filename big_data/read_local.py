from pyspark import SparkContext

def read_from_local(path):
    sc = SparkContext('local')
    return sc.textFile('{path}'.format(path = path))

if __name__ == '__main__':
    rdd = read_from_local('/tmp/temp.txt')
    print(rdd.take(1))


