try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

class KmlToGpxError(Exception):
    pass

def get_lines(tree:object)->list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}LineString/{http://www.opengis.net/kml/2.2}coordinates')  

def get_points(tree:object)-> list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}Placemark')  

def get_tree(path:str)-> object:
    with open(path, 'r') as read_obj:
        tree = etree.parse(read_obj)
    return tree

def get_waypoint_info_from_element(placemark:object) -> (str,str):
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

def make_write_root()-> object:
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

def write_to_path(root:object, path:str):
    result = etree.tostring(root, pretty_print=True)
    with open(path, 'wb') as write_obj:
        write_obj.write(result)

def get_cooridinates_from_string(s:str)->(str, str, str):
    s = s.strip()
    fields = s.split(',')
    if len(fields) < 2:
        raise KmlToGpxError('not enough fields in coordinates')
    elevation = None
    if len(fields) == 3:
        elevation = fields[2]
    return fields[1], fields[0], elevation

def make_trk(root:object)-> object:
    trk = etree.Element("trk")
    root.append(trk)
    return trk

def make_trkpt(lattitude:str, longitude:str, elevation:str)->object:
    trkpt = etree.Element("trkpt", lat=lattitude, lon = longitude, )
    if elevation:
        ele = etree.Element("ele")
        ele.text = elevation
        trkpt.append(ele)
    return trkpt

def make_trkseg(trk:object, coordinates:str)->object:
    trkseg = etree.Element("trkseg")
    for i in coordinates.text.split('\n'):
        if i.strip() == '':
            continue
        lattitude, longitude, elevation = get_cooridinates_from_string(i)
        trkpt = make_trkpt(
                lattitude = lattitude, 
                longitude = longitude, 
                elevation = elevation)
        trkseg.append(trkpt)
    return trkseg

def convert(path:str, out_path:str = None, verbose:bool = False):
    assert False, 'use kml_tools.py convert-to-gpx'
    tree = get_tree(path = path)
    line_list = get_lines(tree)
    point_list = get_points(tree = tree)
    write_root = make_write_root()
    for i in point_list:
        name, coordinates  = get_waypoint_info_from_element(
                placemark = i)
        lattitude, longitude, elevation = get_cooridinates_from_string(coordinates)
        add_wpx(root = write_root, lattitude = lattitude, 
            longitude = longitude, name = name, elevation = elevation)
    trk = make_trk(root = write_root)
    for i in line_list:
        trkseg = make_trkseg(trk = trk, coordinates = i)
        trk.append(trkseg)
    if out_path:
        write_to_path(path = out_path, root = write_root)
    else:
        return etree.tostring(write_root)

    if verbose:
        print(f'wrote to {out_path}')

def test():
    path = '/home/henry/Downloads/si_route.kml'
    out_path = '/home/henry/Downloads/test_si_convert.gpx'

    convert(
            path = path, 
            out_path = out_path,
            verbose = True
            )


if __name__== '__main__':
    test()

