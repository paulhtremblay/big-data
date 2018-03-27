from map_data import map_to_fields


def to_df(path):
    rdd =  map_to_fields(path)
    print(type(rdd))


if __name__ == '__main__':
    df  = to_df('paulhtremblay/noaa/data/1901/')
    print(dir(df))
