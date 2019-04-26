import pprint
pp =pprint.PrettyPrinter(indent = 4)
from numpy import nan
import numpy as np
import json
try:
    from . import  choropleth_prep
except SystemError:
    import choropleth_prep
except ImportError:
    import choropleth_prep

def point_is_territory(x):
    assert isinstance(x, list)
    for i in x:
        if max(i[0]) > 0:
            return True

def move_hawaii():
    choropleth=  choropleth_prep.Chorpleth('state')
    points = choropleth.points_dict
    ak = points['HI']
    final = {'x':[], 'y':[]}
    for i in ak:
        if max(i[0]) > 0:
            continue
        final['x'] += i[0]
        final['y'] += i[1]
    xs = [ x + 35 for x in final['x']]
    ys = [x + 5 for x in final['y']]
    d = {'x':xs, 'y': ys}
    return d

def resize_alaska():
    choropleth=  choropleth_prep.Chorpleth('state')
    points = choropleth.points_dict
    ak = points['AK']
    final = {'x':[], 'y':[]}
    for i in ak:
        if max(i[0]) > 0:
            continue
        final['x'] += i[0]
        final['y'] += i[1]
    xs = [.5 * x -30 for x in final['x']]
    ys = [.5 * x - 8 for x in final['y']]
    d = {'x':xs, 'y': ys}
    with open('data/alaska_resized.json', 'w') as write_obj:
        json.dump(final, write_obj)
    return d

def resize_alaska_counties():
    choropleth=  choropleth_prep.Chorpleth('state')
    points = choropleth.points_dict
    ak = points['AK']
    final = {'x':[], 'y':[]}
    for i in ak:
        if max(i[0]) > 0:
            continue
        final['x'] += i[0]
        final['y'] += i[1]
    xs = [.5 * x -30 for x in final['x']]
    ys = [.5 * x - 8 for x in final['y']]
    d = {'x':xs, 'y': ys}
    return d

def make_counties_no_territories_with_move():
    fips = {}
    with open('data/zip_fips.json', 'r') as read_obj:
        zips = json.load(read_obj)
    for key_zip in zips.keys():
        fip = zips[key_zip]['fips']
        state = zips[key_zip]['state']
        fips[fip] = state
    choropleth=  choropleth_prep.Chorpleth('county')
    points = choropleth.points_dict
    final = {}
    for key in points.keys():
        state  = fips.get(key)
        if  state in ['GU', 'VI', 'PR', 'AS', 'MP', 'HI', 'AK', None]:
            continue
        l = choropleth.get_points(key)
        if point_is_territory(l):
            continue
        final[key] = {'x':[], 'y':[] }
        for i in l:
            final[key]['x'] += i[0]
            final[key]['y'] += i[1]
            final[key]['state'] = state
    with open('data/counties_non_territories_with_move.json', 'w') as write_obj:
        json.dump(final, write_obj)

def states_alaska_resize():
    ak = resize_alaska()
    hi = move_hawaii()
    choropleth=  choropleth_prep.Chorpleth('state')
    points = choropleth.points_dict
    final = {}
    for key in points.keys():
        if key in ['GU', 'VI', 'PR', 'AS',  'MP', 'AK', 'HI']:
            continue
        final[key] = {'x':[], 'y':[]}
        l = choropleth.get_points(key)
        for i in l:
            if max(i[0]) > 0:
                continue
            final[key]['x'] += i[0]
            final[key]['y'] += i[1]
    final['AK'] = ak
    final['HI'] = hi
    with open('data/states_states_resize.json', 'w') as write_obj:
        json.dump(final, write_obj)

def make_counties_no_territories():
    fips = {}
    with open('data/zip_fips.json', 'r') as read_obj:
        zips = json.load(read_obj)
    for key_zip in zips.keys():
        fip = zips[key_zip]['fips']
        state = zips[key_zip]['state']
        fips[fip] = state
    choropleth=  choropleth_prep.Chorpleth('county')
    points = choropleth.points_dict
    final = {}
    for key in points.keys():
        state  = fips.get(key)
        if  state in ['GU', 'VI', 'PR', 'AS', 'MP', None]:
            continue
        l = choropleth.get_points(key)
        if point_is_territory(l):
            continue
        final[key] = {'x':[], 'y':[] }
        for i in l:
            final[key]['x'] += i[0]
            final[key]['y'] += i[1]
            final[key]['state'] = state
    with open('data/counties_non_territories.json', 'w') as write_obj:
        json.dump(final, write_obj)

def make_states_no_territories():
    choropleth=  choropleth_prep.Chorpleth('state')
    points = choropleth.points_dict
    final = {}
    for key in points.keys():
        if key in ['GU', 'VI', 'PR', 'AS',  'MP']:
            continue
        final[key] = {'x':[], 'y':[]}
        l = choropleth.get_points(key)
        for i in l:
            if max(i[0]) > 0:
                continue
            final[key]['x'] += i[0]
            final[key]['y'] += i[1]
    with open('data/states_non_territories.json', 'w') as write_obj:
        json.dump(final, write_obj)

if __name__ == '__main__':
    #make_states_no_territories()
    #make_counties_no_territories()
    #resize_alaska()
    #states_alaska_resize()
    make_counties_no_territories_with_move()
