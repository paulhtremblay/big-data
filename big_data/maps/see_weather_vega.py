import make_point_map
import pprint
import parse_idf
pp = pprint.PrettyPrinter(indent=4)

def get_points():
    d = []
    with open('../perm_data/stations_2000.csv', 'r') as read_obj:
        line = 'init'
        counter = 0
        while line:
            line = read_obj.readline()
            fields = line.split(',')
            if len(fields) != 3:
                continue
            if fields[2].strip() == '999999':
                continue
            counter += 1
            yield {'name':fields[2].strip(), 'num':1, 'latitude':fields[0], 'longitude':fields[1]}
            #d.append({'name':fields[2].strip(), 'num':1, 'latitude':fields[0], 'longitude':fields[1]})

def main():
    gen = get_points()
    make_point_map.make_map([i for i in gen])

    gen = get_points()
    d2= parse_idf.main()
    u = 0
    states = {}
    for p in gen:
        name = p.get('name')
        if not d2.get(name):
            u += 1
        else:
            state = d2[name]['st']
            if not states.get(state):
                states[state] = 0
            states[state] += 1
    print('num unmatched is {0}'.format(u))
    pp.pprint(states)

if __name__ == '__main__':
    main()
