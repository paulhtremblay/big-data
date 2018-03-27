from read_s3 import read_from_s3
import parse_line


def map_test(path):
    return read_from_s3(path)\
        .map(lambda x: [1, 2])

def map_to_fields(path):
    return read_from_s3(path)\
        .map(lambda x: parse_line.parse_line(x))

if __name__ == '__main__':
    rdd = map_to_fields('paulhtremblay/noaa/data/1901/')
    print(rdd.take(1))
