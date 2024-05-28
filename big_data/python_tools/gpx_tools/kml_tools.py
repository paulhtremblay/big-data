import os
import argparse
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

class KmlToGpxError(Exception):
    pass

def _get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help')

    parser_combine = subparsers.add_parser('combine', help='a help')
    parser_combine.add_argument("path", help="path of file")
    parser_combine.set_defaults(func=combine)
    args = parser.parse_args()
    args.func(args)

    return args

def get_tree(path):
    with open(path, 'r') as read_obj:
        tree = etree.parse(read_obj)
    return tree

def get_lines(tree:object)->list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}LineString/{http://www.opengis.net/kml/2.2}coordinates')  

def get_cooridinates_from_lines(line_list):
    l =   []
    for i in line_list:
        l.append(i.text.strip())
    return '\n'.join(l)

def combine_lines(root_or_path):
    if isinstance(root_or_path, str):
        root = get_tree(root_or_path)
    else:
        root = root_or_path
    lines = get_lines(tree = root)
    s= get_cooridinates_from_lines(line_list = lines)
    line_el = make_line(name = 'combined-line', 
            points = s)
    root = make_write_root()
    root.append(line_el)
    return root

def make_write_root()-> object:
    root = etree.Element("kml", 
            xmlns= "http://www.topografix.com/GPX/1/1")
    return root

def ns():
    return  'http://www.opengis.net/kml/2.2'  

def make_point(
        name, 
        latitude, 
        longitude, 
        description = None,
        elevation = 0):
    placemark = etree.Element("Placemark")
    if description:
        description_e =etree.Element("description") 
        description_e.text = description
        placemark.append(description_e)
    point =etree.Element("Point") 
    coordinates =etree.Element("coordinates") 
    coordinates.text = f"{longitude},{latitude},{elevation}"
    point.append(coordinates)
    placemark.append(point)
    return placemark

def make_point_strings(points):
    if isinstance(points, str):
        return points
    coordinates_list = []
    for i in points:
        coordinates_list.append(f'{i[0]},{i[1]},{i[2]}')
    coordinates_string = '\n'.join(coordinates_list)
    return coordinates_string

def make_line(name, points):
    placemark = etree.Element("Placemark")
    line_string =etree.Element("LineString") 
    extrude = etree.Element("extrude") 
    extrude.text = '1'
    line_string.append(extrude)
    tessellate = etree.Element("tessellate") 
    tessellate.text = '1'
    line_string.append(tessellate)
    coordinates = etree.Element("coordinates") 
    coordinates_string = make_point_strings(points)
    coordinates.text = coordinates_string
    line_string.append(coordinates)
    placemark.append(line_string)
    return placemark


def write_to_path(root, path):
    s =  etree.tostring(root)
    with open(path, 'wb') as write_obj:
        write_obj.write(s)

def main():
    args = _get_args()

def combine(args):
    in_path = args.path
    dir_ = os.path.dirname(os.path.abspath(in_path))
    rel_in_path = os.path.split(in_path)[1]
    rel_in_path_no_ext = os.path.splitext(rel_in_path)[0]
    out_path = os.path.join(dir_, f'{rel_in_path_no_ext}_combined.kml')
    root = combine_lines(root_or_path = in_path)
    write_to_path(root = root, path = out_path)

if __name__== '__main__':
    main()
    pass
