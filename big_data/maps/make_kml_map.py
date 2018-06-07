def _write_point(write_obj, longitude, latitude,  name, description = ''):
    write_obj.write("""<Placemark>
<name>{name}</name>
<description>{description}</description>
<Point>
  <coordinates>{latitude},{longitude}</coordinates>
</Point>
</Placemark>\n""".format(latitude = latitude, longitude = longitude, description
    = description, name = name))

def make_map(data):
    with open('temp_data/map_points.kml', 'w') as write_obj:
        write_obj.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
        write_obj.write("""<kml xmlns="http://www.opengis.net/kml/2.2">\n""")
        write_obj.write("""<Document>\n""")
        for i in data:
            _write_point(write_obj, i[0], i[1], i[2])
        write_obj.write("""</Document>\n""")
        write_obj.write("""</kml>""")

def main():
    data = [[37.7, -85.2, 'foo']]
    make_map(data)

if __name__ == '__main__':
    main()

