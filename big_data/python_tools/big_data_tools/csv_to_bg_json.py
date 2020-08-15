import json
import csv
import random

def get_imbalanced_data_gauss2(data_len = 100,data_len_minor = None, std= .75, mean1 = 1, mean2 = 2):
    if not data_len_minor:
        #data_len_minor = data_len
        data_len_minor = int(data_len/10)
    x1 =  [random.gauss(mean1, std ) for x in range(data_len)] + [random.gauss(mean2, std) for x in range(data_len_minor)]
    y = [0 for x in range(data_len)] + [1 for x in range(data_len_minor)]
    fieldnames = ['x1', 'y']
    path = '/home/henry/Downloads/data1'
    with open(path + '.json', 'w') as write_obj:
        with open(path + '.csv', 'w') as write_obj2:
            write_obj2.write('x1,y1,row_num\n')
            for counter, v in enumerate(x1):
                d = {'x1':v, 'y':y[counter], 'row_num': counter}
                j = json.dumps(d)
                write_obj.write('{j}\n'.format(j = j))
                write_obj2.write('{v},{v2},{v3}\n'.format(
                    v = v,
                    v2 = y[counter],
                    v3 = counter
                    ))

def main():
    pass

if __name__ == '__main__':
    main()
    get_imbalanced_data_gauss2(data_len = 100000)
