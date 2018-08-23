import sys
import os
import shapefile
from shapely import geometry
#from shapely.geometry import shape
import pprint
pp = pprint.PrettyPrinter(indent = 4)
import zipfile
import tempfile
import shutil

class Chorpleth:

    def __init__(self, the_type):
        assert the_type in ['state', 'county']
        if the_type == 'state':
            path = os.path.join(sys.prefix, 'map_data', 'cb_2017_us_state_5m.zip')
        else:
            path = os.path.join(sys.prefix, 'map_data', 'cb_2017_us_county_5m.zip')
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path) as zip_ref:
            zip_ref.extractall(temp_dir)
        if the_type == 'state':
            path = os.path.join(temp_dir, 'cb_2017_us_state_5m.shp' )
        else:
            path = os.path.join(temp_dir, 'cb_2017_us_county_5m.shp' )
        xs, ys, names = self.create_sf_data(path)
        shutil.rmtree(temp_dir)
        self.dict = {}
        self.points_dict = {}
        for counter, i in enumerate(names):
            #getting rid of small territories belonging to AK
            if not self.points_dict.get(i):
                self.points_dict[i] = []
            self.points_dict[i].append((xs[counter], ys[counter]))
            """
            if i == 'AK':
                if max(xs[counter]) < 0:
                    self.points_dict[i].append((xs[counter], ys[counter]))
            else:
                self.points_dict[i].append((xs[counter], ys[counter]))
            """
        for counter, i in enumerate(xs):
            if not self.dict.get(names[counter]):
                self.dict[names[counter]] = []
            self.dict[names[counter]].append(geometry.Polygon(list(zip(i, ys[counter]))[0:-1]))

    def add_names(slef, indices, itererator, names):
        for i in indices:
            names.append(itererator.record[4])

    def make_all_data(self, sf):
        counter = 0
        xs = []
        ys = []
        names = []
        for i in sf.iterShapeRecords():
            indices = i.shape.parts.tolist()
            x_polygon = self.make_polygon(indices, i, 'x')
            xs.extend(self.make_polygon(indices, i, 'x'))
            ys.extend(self.make_polygon(indices, i, 'y'))
            self.add_names(indices, i, names)
        return xs, ys,  names

    def make_polygon(self, indices, itererator, x_or_y):
        if x_or_y == 'x':
            index = 0
        else:
            index = 1
        x = [x[index] for x in itererator.shape.points]
        return [x[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]

    def create_sf_data(self, shape_path):
        sf =  shapefile.Reader(shape_path)
        xs, ys, names = self.make_all_data(sf)
        assert len(xs) == len(ys)
        assert len(xs) == len(names)
        return xs, ys, names

    def get_id_of_shape(self, points):
        p = geometry.Point(points)
        for key in list(self.dict.keys()):
            shapes = self.dict[key]
            for sh in shapes:
                if sh.contains(p):
                    return key
        return None

    def get_shape(self, the_id):
        return self.dict.get(the_id)

    def get_points(self, the_id):
        return self.points_dict.get(the_id)

if __name__ == '__main__':
    choropleth = Chorpleth(the_type = 'state')
    print(choropleth.get_id_of_shape((-71.097320, 42.338124)))

