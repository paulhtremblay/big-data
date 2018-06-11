import sys
from bokeh.plotting import figure, show, output_file
import shapefile
from pyproj import Proj
#from shapely.geometry import shape
import pprint
pp = pprint.PrettyPrinter(indent = 4)
path = '/Users/a6002538/Documents/shapefiles/continental_us/us_continental.shp'
sf = shapefile.Reader(path)
original = Proj(sf)
states = ['MA', 'NH']
xs_points = []
ys_points = []
fill_colors = []
for i in sf.iterShapeRecords():
    indices = i.shape.parts.tolist()
    if i.record[4] not in states:
        continue
    if i.record[4] == 'MA':
        fill_colors.extend(['blue' for x in indices])
    elif i.record[4] == 'NH':
        fill_colors.extend(['red' for x in indices])
    x = [x[0] for x in i.shape.points]
    x = [x[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]
    y = [x[1] for x in i.shape.points]
    y = [y[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]
    xs_points.extend(x)
    ys_points.extend(y)

p = figure(title="test map 2", toolbar_location="left",
           plot_width=700, plot_height=700)
p.patches(xs_points, ys_points,
          fill_color=fill_colors, 
          fill_alpha=0.7,
          line_color="white", line_width=0.5)
#don't need to reporject, since shapefile is also in nad83
p.circle([-71.094575], [42.336094], size=5, color="black", alpha=0.5)

show(p)
