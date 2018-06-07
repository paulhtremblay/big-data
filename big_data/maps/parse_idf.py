import pprint
import datetime
pp = pprint.PrettyPrinter(indent = 4)
def main():
    d = {}
    with open('isd.txt', 'r') as read_obj:
        line = 'init'
        count = 0
        while line:
            line = read_obj.readline()
            if line.strip() == '':
                continue
            count += 1
            if count == 1:
                continue
            usaf = line[0:6]
            wban = line[7:12]
            station_name = line[13:42].strip()
            ctry = line[43:47].strip()
            st = line[48:51].strip()
            call = line[51:56].strip()
            if line[57:65].strip() != '':
                lat = float(line[57:65])
            else:
                lat = 0
            if line[65:74].strip() != '':
                lon = float(line[65:74])
            else:
                lon = 0
            if line[74:81].strip() != '':
                elev = float(line[74:81])
            else:
                elev = 0
            begin = datetime.datetime.strptime(line[82:90], '%Y%m%d')
            end = datetime.datetime.strptime(line[91:99],'%Y%m%d')
            """
            d[(usaf, wban)] = {'usaf':usaf,'wban':wban, 'station_name':station_name,
                    'ctry':ctry, 'st':st, 'call':call, 'lat':lat, 'lon':lon, 
                    'elev':elev, 'begin':begin, 'end':end}

            """
            d[usaf] = {'usaf':usaf,'wban':wban, 'station_name':station_name,
                    'ctry':ctry, 'st':st, 'call':call, 'lat':lat, 'lon':lon, 
                    'elev':elev, 'begin':begin, 'end':end}
    return d

if __name__ == '__main__':
    pp.pprint(main())
