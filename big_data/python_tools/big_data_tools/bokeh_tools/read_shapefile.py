import shapefile
from shapely.geometry import shape
path = '/Users/a6002538/Documents/shapefiles/bokeh_map/DAMSELFISH_distributions.shp'
sf = shapefile.Reader(path)
#print(dir(sf))
feature = sf.shapeRecords()[0]
first = feature.shape.__geo_interface__  
fields = sf.fields

def records_gen(sf):
    for i in sf.iterRecords():
        yield i


print(fields)
print(len(sf.shapes()))
print(len(sf.records()))
rec_gen = records_gen(sf)
"""
for i in sf.iterShapes():
    print(i.shapeType)
    bb =  [ coord for coord in i.bbox]
    print(bb)
    record = next(rec_gen)
    print(len(fields))
    print(record)
    print(len(record))
    print(fields[5])
    print(record[6])
    break
"""

for i in sf.iterShapeRecords():
    print(i)
    print(i.record)
    break
