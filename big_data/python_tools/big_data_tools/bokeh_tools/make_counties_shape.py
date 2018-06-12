import sys
import shapefile
from shapely import geometry
from pyproj import Proj
#from shapely.geometry import shape
import pprint
pp = pprint.PrettyPrinter(indent = 4)

def make_polygon(indices, itererator, x_or_y):
    if x_or_y == 'x':
        index = 0
    else:
        index = 1
    x = [x[index] for x in itererator.shape.points]
    return [x[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]

def increase_ids(indices, counter, ids):
    for x in indices:
        counter += 1
        ids.append(counter)
    return counter

def add_names(indices, itererator, names):
    for i in indices:
        names.append(itererator.record[5])

def get_shp_object(path):
    return shapefile.Reader(path)

def make_all_data(sf):
    counter = 0
    ids = []
    xs = []
    ys = []
    names = []
    counter = 0
    for i in sf.iterShapeRecords():
        counter += 1
        indices = i.shape.parts.tolist()
        x_polygon = make_polygon(indices, i, 'x')
        xs.extend(make_polygon(indices, i, 'x'))
        ys.extend(make_polygon(indices, i, 'y'))
        counter = increase_ids(indices, counter,  ids)
        add_names(indices, i, names)
    return xs, ys, ids, names

def create_sf_data(shape_path):
    sf = get_shp_object(shape_path)
    xs, ys, ids, names = make_all_data(sf)
    assert len(xs) == len(ys)
    assert len(xs) == len(ids)
    return xs, ys, ids, names


def main():
    path = '/tmp/us_states_shapes/cb_2017_us_state_5m.shp'
    #sf = get_shp_object('/tmp/us_counties_shapes/cb_2017_us_county_5m.shp')
    xs, ys, ids, names = create_sf_data(path)
    the_dict = {}
    for counter, i in enumerate(xs):
        the_dict[counter] = (geometry.Polygon(list(zip(i, ys[counter]))[0:-1]), names[counter])
    the_id, state = in_what_shape(the_dict, (-71.094575, 42.336094))
    print(state)
    the_id, state = in_what_shape(the_dict, (-81.359145, 28.450916))
    print(state)

def in_what_shape(geom_dict, points):
    p = geometry.Point(points)
    for key in list(geom_dict.keys()):
        sh = geom_dict[key][0]
        if sh.contains(p):
            return key, geom_dict[key][1]
    return None, None

if __name__ == '__main__':
    main()

