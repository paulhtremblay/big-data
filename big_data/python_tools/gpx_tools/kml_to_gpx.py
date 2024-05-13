try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

class KmlToGpxError(Exception):
    pass

def get_lines(tree)->list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}LineString/{http://www.opengis.net/kml/2.2}coordinates')  

def get_points(tree)-> list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}Placemark')  
    #return  tree.findall('.//{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates')  

def get_tree(path):
    with open(path, 'r') as read_obj:
        tree = etree.parse(read_obj)
    return tree

def get_waypoint_info_from_element(placemark):
    name = None
    coordinates = None
    for element in placemark.iter():
        if element.tag == '{http://www.opengis.net/kml/2.2}name':
            if name != None:
                raise KmlToGpxError('more than one point in element; don\'t know how to handle')
            name = element.text
        elif element.tag == '{http://www.opengis.net/kml/2.2}coordinates':
            if coordinates != None:
                raise KmlToGpxError('more than one point in element; don\'t know how to handle')
            coordinates = element.text.strip()

    return name, coordinates

def make_write_root():
    root = etree.Element("gpx", 
            creator = "GPSMAP 64st", version = "1.1", xmlns= "http://www.topografix.com/GPX/1/1")
    return root

def add_wpx(root, lattitude, longitude, name, elevation = None):
    wpt = etree.Element("wpt", lat=lattitude, lon=longitude)
    if elevation:
        ele = etree.Element("ele")
        ele.text = elevation
    name_element = etree.Element("name")
    name_element.text = name
    sym = etree.Element("sym")
    sym.text = "Residence"

    if elevation:
        wpt.append(ele)
    wpt.append(name_element)
    wpt.append(sym)
    root.append(wpt)

def write_to_path(root, path):
    result = etree.tostring(root, pretty_print=True)
    with open(path, 'wb') as write_obj:
        write_obj.write(result)

def get_cooridinates(s):
    fields = s.split(',')
    if len(fields) < 2:
        raise KmlToGpxError('not enough fields in coordinates')
    elevation = None
    if len(fields) == 3:
        elevation = fields[2]
    return fields[1], fields[0], elevation


def test():
    tree = get_tree(path = '/home/henry/Downloads/waypoints_test.gpx.kml')
    line_list = get_lines(tree)
    print(line_list)
    point_list = get_points(tree = tree)
    print(point_list)
    x = point_list[0]
    name, coordinates  = get_waypoint_info_from_element(placemark = point_list[0])
    write_root = make_write_root()
    lattitude, longitude, elevation = get_cooridinates(coordinates)
    add_wpx(root = write_root, lattitude = lattitude, 
            longitude = longitude, name = name, elevation = elevation)
    write_to_path(path = '/home/henry/Downloads/test_kml_convert.gpx', root = write_root)


if __name__== '__main__':
    test()

