from shapely.ops import transform
from functools import partial
import pyproj
from pyproj import Proj
from shapely.geometry import Point

project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:4326'),
    pyproj.Proj(init='epsg:26913'))

g2 = transform(project, Point(1,2))
print(g2)
