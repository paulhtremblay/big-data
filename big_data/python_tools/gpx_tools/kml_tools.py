import os
import argparse
import pprint
import math
from statistics import median

import tools
import smooth as smooth


pp = pprint.PrettyPrinter(indent= 4)
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

class KmlToGpxError(Exception):
    pass

def _average_lines(y, window_len, order):
    from scipy.signal import savgol_filter as savitzky_golay
    return savitzky_golay(y, window_len, order) 

def _get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help')

    parser_combine = subparsers.add_parser('combine', help='combine lines in one file')
    parser_combine.add_argument("path", help="path of file")
    parser_combine.set_defaults(func=combine)
    parser_combine_files = subparsers.add_parser('combine-files', help='combine lines from mult files')
    parser_combine_files.set_defaults(func=combine_files)
    parser_combine_files.add_argument("paths", nargs='+', help="path of file")
    parser_combine_files.add_argument("--out", '-o',  required = True, help="out-path")
    parser_convert_gpx = subparsers.add_parser('convert_to_gpx', help='convert to gpx')
    parser_convert_gpx.set_defaults(func=convert_to_gpx)
    parser_convert_gpx.add_argument("path", help="path of file")
    parser_convert_gpx.add_argument("--out", required = False,  
            help="out path of file")
    parser_convert_gpx.add_argument("--verbose", '-v',  action ='store_false')  
    parser_average_lines = subparsers.add_parser('average-lines', help='average multiple lines in KML')
    parser_average_lines.add_argument("path", help="path of file")
    parser_average_lines.add_argument("--verbose", '-v',  action ='store_true')  
    parser_average_lines.set_defaults(func=average_lines)

    parser_combine_diff_lines = subparsers.add_parser(
            'merge-lines', help='merge paths')
    parser_combine_diff_lines.add_argument("paths", nargs='+', help="path of file")
    parser_combine_diff_lines.add_argument("--verbose", '-v',  action ='store_true')  
    parser_combine_diff_lines.add_argument("--out", required = True,  
            help="out path of file")
    parser_combine_diff_lines.set_defaults(func=merge_lines)

    parser_create_mile_markers = subparsers.add_parser(
            'mile-markers', help='create mile markers')
    parser_create_mile_markers.add_argument("--verbose", '-v',  action ='store_true')  
    parser_create_mile_markers.set_defaults(func=create_mile_markers)
    parser_create_mile_markers.add_argument("path", help="path of file")
    parser_create_mile_markers.add_argument("--out", required = True,  
            help="out path of file")
    parser_create_mile_markers.add_argument("--reverse", '-r',  
            action ='store_true', help = 'route is up and back, so double points')  

    parser_prune_by_mark = subparsers.add_parser(
            'prune-by-location', help='prune by location')
    parser_prune_by_mark.add_argument("--verbose", '-v',  action ='store_true')  
    parser_prune_by_mark.add_argument("path", help="path of file")
    parser_prune_by_mark.add_argument("--start", '-s',  type = str, help = 'strart location')  
    parser_prune_by_mark.add_argument("--end", '-e',  type = str, help = 'strart location')  
    parser_prune_by_mark.set_defaults(func=prune_by_location)

    parser_files_to_line = subparsers.add_parser(
            'files-to-line', 
            help='use multpile files to create one line')
    parser_files_to_line.add_argument("paths", nargs='+', help="path of file")
    parser_files_to_line.add_argument("--out", required = True,  
            help="out path of file")
    parser_files_to_line.add_argument("--verbose", '-v',  action ='store_true')  
    parser_files_to_line.set_defaults(func=files_to_lines)

    parser_prune_to_top = subparsers.add_parser(
            'prune-to-top', help='prune just the first half of hike')
    parser_prune_to_top.add_argument("--verbose", '-v',  action ='store_true')  
    parser_prune_to_top.add_argument("path", help="path of file")
    parser_prune_to_top.set_defaults(func=prune_to_top)

    parser_polygon_from_files = subparsers.add_parser(
            'polygon-from-files', 
            help='use multpile files to create one polygon')
    parser_polygon_from_files.add_argument("paths", nargs='+', help="path of file")
    parser_polygon_from_files.add_argument("--out", '-o',  required = True,  
            help="out path of file")
    parser_polygon_from_files.add_argument("--verbose", '-v',  action ='store_true')  
    parser_polygon_from_files.set_defaults(func=polygon_from_files)

    parser_smooth = subparsers.add_parser(
            'smooth', 
            help='smooth')
    parser_smooth.add_argument("--verbose", '-v',  action ='store_true')  
    parser_smooth.add_argument("path", help="path of file")
    parser_smooth.set_defaults(func=smooth_func)
    

    args = parser.parse_args()
    args.func(args)

    return args

def get_tree(path):
    with open(path, 'r') as read_obj:
        tree = etree.parse(read_obj)
    return tree

def get_lines(tree:object)->list:
    return  tree.findall('.//{http://www.opengis.net/kml/2.2}LineString/{http://www.opengis.net/kml/2.2}coordinates')  

def get_points(tree:object)-> list:
    final = []
    l =  tree.findall('.//{http://www.opengis.net/kml/2.2}Placemark')  
    for i in l:
        is_linestring = False
        children = list(i)
        for j in children:
            if j.tag == '{http://www.opengis.net/kml/2.2}LineString':
                is_linestring = True
        if not is_linestring:
            final.append(i)
    return final

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
                print(coordinates)
                raise KmlToGpxError('more than one point in element; don\'t know how to handle')
            coordinates = element.text.strip()

    return name, coordinates

def get_cooridinates_from_string(s:str)->(str, str, str):
    s = s.strip()
    fields = s.split(',')
    if len(fields) < 2:
        raise KmlToGpxError('not enough fields in coordinates')
    elevation = None
    if len(fields) == 3:
        elevation = fields[2]
    return fields[1], fields[0], elevation

def _get_points_from_line_string(s):
    final = []
    for i in s.split('\n'):
        lat, lon, ele =  get_cooridinates_from_string(s= i)
        final.append((float(lat), float(lon), float(ele)))
    return final

def tracks_from_kml(path, verbose = False):
    tree = get_tree(path = path)
    lines = get_lines(tree= tree)
    final = []
    for counter, i in enumerate(lines):
        name = f'track_{counter}'
        d = {'name':name, 'points':_get_points_from_line_string(s = i.text.strip())}
        final.append(d)
    return final


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
            xmlns= "http://www.opengis.net/kml/2.2")
    return root

def make_write_root_gpx()-> object:
    root = etree.Element("gpx", 
            creator = "GPSMAP 64st", version = "1.1", xmlns= "http://www.topografix.com/GPX/1/1")
    return root

def ns():
    return  'http://www.opengis.net/kml/2.2'  

def make_polygon(
        name: str,
        points: list,
        verbose: bool,
        )-> object:
    points = swap_long_lat(points)
    placemark_e = etree.Element("Placemark")
    name_e =etree.Element("name") 
    name_e.text = name
    polygon_e =etree.Element("Polygon") 
    placemark_e.append(name_e)
    placemark_e.append(polygon_e)
    outerBoundaryIs_e =etree.Element("outerBoundaryIs") 
    polygon_e.append(outerBoundaryIs_e)
    LinearRing_e =etree.Element("LinearRing") 
    tessellate_e =etree.Element("tessellate") 
    tessellate_e.text = "1"
    LinearRing_e.append(tessellate_e)
    coordinates_e =etree.Element("coordinates") 
    if points[0] != points[-1]:
        points.append(points[0])
    coordinates_e.text =  make_point_strings(points)
    LinearRing_e.append(coordinates_e)
    outerBoundaryIs_e.append(LinearRing_e)
    return placemark_e
          


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
    name_e =etree.Element("name") 
    name_e.text = str(name)
    coordinates =etree.Element("coordinates") 
    coordinates.text = f"{longitude},{latitude},{elevation}"
    point.append(coordinates)
    placemark.append(point)
    placemark.append(name_e)
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
    points = swap_long_lat(points)
    placemark = etree.Element("Placemark")
    name_e =etree.Element("name") 
    name_e.text = name
    placemark.append(name_e)
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


def write_to_path(root, path, verbose = False):
    s =  etree.tostring(root)
    with open(path, 'wb') as write_obj:
        write_obj.write(s)
    if verbose:
        print(f'wrote to {path}')

def main():
    args = _get_args()


def combine_files(args):
    in_paths = args.paths
    write_root = make_write_root()
    folder =etree.Element("Folder") 
    write_root.append(folder)
    for counter1, i in enumerate(in_paths):
        root = get_tree(i)
        lines = get_lines(tree = root)
        for counter2, j in enumerate(lines):
            s = j.text.strip()
            line_el = make_line(name = f'combined-line-{counter1 + 1}{counter2 + 1}', 
                    points = s)
            folder.append(line_el)
    write_to_path(root = write_root, path = args.out)


def _make_out_path(path):
    dir_ = os.path.dirname(os.path.abspath(path))
    rel_in_path = os.path.split(path)[1]
    rel_in_path_no_ext = os.path.splitext(rel_in_path)[0]
    out_path = os.path.join(dir_, f'{rel_in_path_no_ext}_combined.kml')
    return out_path

def _make_out_path_gen(path, ext, name = '', ):
    dir_ = os.path.dirname(os.path.abspath(path))
    rel_in_path = os.path.split(path)[1]
    rel_in_path_no_ext = os.path.splitext(rel_in_path)[0]
    out_path = os.path.join(dir_, f'{rel_in_path_no_ext}{name}.{ext}')
    return out_path

def _make_points_from_lines(line_list):
    assert False, 'not used'
    final = []
    for i in line_list:
        for element in i.iter():
            if element.tag == '{http://www.opengis.net/kml/2.2}coordinates':
                coordinates = element.text.strip()
                for j in coordinates.split('\n'):
                    pairs = get_cooridinates_from_string(s = j)
                    pairs = (pairs[1], pairs[0], pairs[2])
                    final.append(pairs)
    final = sorted(final, key = lambda x:x[0])
    longitude = [x[0] for x in final]
    latitude = [x[1] for x in final]
    return longitude, latitude

def combine(args):
    in_path = args.path
    root = combine_lines(root_or_path = in_path)
    write_to_path(root = root, path = _make_out_path(in_path))

def convert_to_gpx(args):
    tree = get_tree(path = args.path)
    line_list = get_lines(tree)
    point_list = get_points(tree = tree)
    write_root = make_write_root_gpx()
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
    out = args.out
    if not args.out:
       out = _make_out_path_gen(path = args.path, ext = 'gpx' )
    write_to_path(root = write_root, path = out,verbose = args.verbose)

def average_lines(args):
    raise NotImplementedError('not good algorithm')
    tree = get_tree(path = args.path)
    line_list = get_lines(tree)
    longitude, latitude = _make_points_from_lines(line_list)
    #fitted_longitude = _average_lines(y = longitude, window_len = 20, order = 3)
    fitted_latitude = _average_lines(y = latitude, window_len = 45, order = 3)
    assert len(latitude) == len(fitted_latitude)
    #assert len(longitude) == len(fitted_latitude)
    points = []
    for counter, i in enumerate(longitude):
        points.append((i, fitted_latitude[counter],0))
    root = make_write_root()
    new_line_element = make_line(name = 'averaged-line', points = points)
    root.append(new_line_element)
    out = _make_out_path_gen(path = args.path, ext = 'kml', name = '_smoothed' )
    write_to_path(root = root, path = out,verbose = args.verbose)

def _find_nearest(p, points):
    smallest = (None, None)
    #distance, index
    for counter, i in enumerate(points):
        dis = haversine_distance(
            latitude_1 = p[0] , 
            longitude_1= p[1], 
            latitude_2 = i[0]  , 
            longitude_2= i[1] )
        if smallest[0] == None or dis < smallest[0]:
            smallest = (dis, counter)
    return smallest

def _too_far(dis, max_ = 15):
    if dis < max_:
        return False
    return True

def _get_median(points):
    lats = []
    longs = []
    for i in points:
        lats.append(i[0])
        longs.append(i[1])
    lats = sorted(lats)
    longs = sorted(longs)
    return median(lats), median (longs)


def _get_cluster(point, points, max_):
    final = []
    for i in points:
        for j in i:
            dis = haversine_distance(
                latitude_1 = point[0] , 
                longitude_1= point[1], 
                latitude_2 =j[0]  , 
                longitude_2= j[1] )
            if dis <= max_:
                final.append((j[0], j[1]))
    return final

def merge_lines(args):
    tracks = []
    for path in args.paths:
        ext = os.path.splitext(path)[1]
        if ext == '.gpx':
            tracks.append(tracks_from_gpx(path))
        elif ext == '.kml':
            tracks.append(tracks_from_kml(path))
        else:
            raise NotImplementedError(f'not ext for {ext}')
    base_track = tracks[0][0]['points']
    final = []
    n_lons = []
    n_lats = []
    for p in base_track:
        temp_ = [p]
        for i in tracks[1:]:
            nearest = _find_nearest(p, i[0]['points'])
            if not _too_far(nearest[0]):
                temp_.append(i[0]['points'][nearest[1]])
            n_lat, n_lon  = _get_median(points = temp_)
            n_lats.append(n_lat)
            n_lons.append(n_lon)
            final.append((n_lat, n_lon))
    n_lats_s = _average_lines(y = n_lats, window_len = 30, order = 3)
    root = make_write_root()
    points = []
    for i in final:
        points.append((i[1], i[0], 0))
    points2 = []
    for counter, i in enumerate(n_lats_s):
        points2.append((n_lons[counter], i, 0))

    new_line_element = make_line(name = 'averaged-line', points = points2)
    root.append(new_line_element)
    out = args.out
    write_to_path(root = root, path = out,verbose = args.verbose)

def merge_lines_cluster(args):
    tracks = []
    for path in args.paths:
        ext = os.path.splitext(path)[1]
        if ext == '.gpx':
            tracks.append(tracks_from_gpx(path))
    points = [tracks[x][0]['points'] for x in range(len(tracks))]
    f = []
    for i in points[0]:
        c = _get_cluster(
                point = i,
                points = points,
                max_ = 25
                )
        f.append(_get_median(
                points = c
                ))
    points_ = []
    for i in f:
        points_.append((i[1], i[0], 0))
    root = make_write_root()
    new_line_element = make_line(name = 'averaged-line', points = points_)
    root.append(new_line_element)
    #out = _make_out_path_gen(path = args.path, ext = 'kml', name = '_smoothed' )
    out = '/home/henry/Downloads/averaged2.kml'
    write_to_path(root = root, path = out,verbose = args.verbose)

"""
These are GPX functions
"""

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

def tracks_from_gpx(path, verbose = False):
    tree = get_tree(path = path)
    trk =   tree.findall('.//{http://www.topografix.com/GPX/1/1}trk')  
    final = []
    for counter, i in enumerate(trk):
        name = f'track_{counter}'
        d = {'name':name, 'points':[]}
        trksegs = i.findall('{http://www.topografix.com/GPX/1/1}trkseg')
        for j in trksegs:
            trackpoints = j.findall('{http://www.topografix.com/GPX/1/1}trkpt')
            for trackpoint in trackpoints:
                ele = trackpoint.findall('{http://www.topografix.com/GPX/1/1}ele')
                elevation = 0
                if ele:
                    elevation = float(ele[0].text)
                d['points'].append((float(trackpoint.get('lat')), float(trackpoint.get('lon')), elevation))
        final.append(d)
    return final

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

#distance

def calc_distance(origin, destination):
    """great-circle distance between two points on a sphere
       from their longitudes and latitudes"""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km. earth

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = (sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon/2) * sin(dlon/2))
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    return d

def haversine_distance(
    latitude_1: float, 
    longitude_1: float, 
    latitude_2: float, 
    longitude_2: float) -> float:    
    """
    Haversine distance between two points, expressed in meters.

    Implemented from http://www.movable-type.co.uk/scripts/latlong.html
    """
    EARTH_RADIUS = 6378.137 * 1000

    d_lon = math.radians(longitude_1 - longitude_2)
    lat1 = math.radians(latitude_1)
    lat2 = math.radians(latitude_2)
    d_lat = lat1 - lat2

    a = math.pow(math.sin(d_lat/2),2) + \
        math.pow(math.sin(d_lon/2),2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.asin(math.sqrt(a))
    d = EARTH_RADIUS * c

    return d

def create_mile_markers(args):
    l = tracks_from_kml(path = args.path)
    root = make_write_root()
    document_e =etree.Element("Document") 
    root.append(document_e)
    for i in l:
        points = i['points']
        miles = tools.create_mile_markers(
                points = points, 
                reverse = args.reverse)
        for mile in miles:
            p =make_point(
                    name = mile['mile'], 
                    latitude = mile['latitude'], 
                    longitude =  mile['longitude'], 
                    description = None,
                    elevation = mile['elevation'])
            document_e.append(p)

    write_to_path(root = root, path = args.out,verbose = args.verbose)

def _convert_string_to_points(s):
    st, end = s.split(',')
    st = float(st)
    end = float(end)
    return st, end

def swap_long_lat(points):
    """
    for kml
    """
    final = []
    for i in points:
        final.append((i[1], i[0], i[2]))
    return final

def prune_by_location(args):
    l = tracks_from_kml(path = args.path)
    assert len(l) ==1
    if not args.start:
        start = 0
    else:
        lon, lat = _convert_string_to_points(args.start)
        n = find_nearest = tools.find_nearest(
                point = (lon, lat), points = l[0]['points'], verbose = args.verbose)
        start = n[0]
    if not args.end:
        end  = len(l[0]['points']) -1
    else:
        lon, lat = _convert_string_to_points(args.end)
        n = find_nearest = tools.find_nearest(
                point = (lon, lat), points = l[0]['points'], verbose = args.verbose)
        end = n[0]
    points = l[0]['points'][start:end]
    root = make_write_root()
    line_element = make_line(name = 'new-line', points = points)
    root.append(line_element)
    out = _make_out_path_gen(path = args.path, ext = 'kml', name = '_pruned' )
    write_to_path(root = root, path = out,verbose = args.verbose)

def files_to_lines(args):
    points = []
    for i in args.paths:
        l = tracks_from_kml(path = i)
        assert len(l) == 1
        for i in l[0]['points']:
            points.append(i)
    line_element = make_line(name = 'new-line', points = points)
    root = make_write_root()
    root.append(line_element)
    write_to_path(root = root, path = args.out,verbose = args.verbose)

def tracks_from_file(path, verbose = False):
    ext = os.path.splitext(path)[1]
    if ext == '.gpx':
        tree = tracks_from_gpx(path = path, verbose = verbose)
    elif ext == '.kml':
        tree = tracks_from_kml(path = path, verbose = verbose)
    else:
        raise ValueError('no match')
    return tree


def prune_to_top(args):
    l = tracks_from_file(args.path)
    assert len(l) == 1
    high_point =  tools.find_highest(
            points = l[0]['points'], verbose = args.verbose)
    points = l[0]['points'][0:high_point[0]]
    line_element = make_line(name = 'new-line', points = points)
    root = make_write_root()
    root.append(line_element)
    out = _make_out_path_gen(path = args.path, ext = 'kml', name = '_highest' )
    write_to_path(root = root, path = out,verbose = args.verbose)

def polygon_from_files(args):
    points = []
    for i in args.paths:
        tracks = tracks_from_kml(path = i)
        for track  in  tracks:
            for j in track['points']:
                points.append(j)

    line_element = make_polygon(
            name = 'new-line', points = points, verbose = args.verbose)
    root = make_write_root()
    root.append(line_element)
    write_to_path(root = root, path = args.out,verbose = args.verbose)

def smooth_func(args):
    tracks = tracks_from_file(
            path = args.path, 
            verbose = args.verbose)
    assert len(tracks) == 1
    smoothed_points = smooth.process(
            points = tracks[0]['points'],
            verbose = args.verbose
            )
    line_element = make_line(name = 'smoothed-line', points = smoothed_points)
    root = make_write_root()
    root.append(line_element)
    out = _make_out_path_gen(path = args.path, ext = 'kml', name = '_smoothed' )
    write_to_path(root = root, path = out,verbose = args.verbose)

if __name__== '__main__':
    main()
