import pprint
import json
pp = pprint.PrettyPrinter(indent = 4)

def convert(path):
    with open(path, 'r') as read_obj:
        line = 'init'
        counter = 0
        l = []
        while line:
            line = read_obj.readline()
            counter += 1
            if counter == 1:
                continue
            fields = line.split('\t')
            if len(fields) != 2:
                continue
            l.append({'id':fields[0], 'rate':float(fields[1].strip())})
    return l

def main():
    return convert('unemployment.tsv')

if __name__ == '__main__':
    pp.pprint(main())
