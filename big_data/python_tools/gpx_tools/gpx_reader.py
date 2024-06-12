import os
import argparse
import datetime
from pytz import timezone
import pytz
import tempfile
import subprocess
import math

import csv
import uuid

import gpxpy
import gpxpy.gpx

import pprint
pp = pprint.PrettyPrinter(indent = 4)

class GpxError(Exception):
    pass


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of file")
    parser.add_argument("--type", '-t', 
            choices = [
                'view', 
                'prune-number', 
                'prune-speed', 
                'join-segment',
                'from-kml',
                'smooth',
                'create-markers',
                'map-from-walk',
                'waypoints',
                'climb',
                ],
            required = True,
            help="type of convert")
    parser.add_argument("--verbose", '-v',  
            action="store_true",
            help="verbose output")
    parser.add_argument("--start", '-s',  
            type = int,
            required = False,
            help="start of prune")
    parser.add_argument("--end", '-e',  
            type = int,
            required = False,
            help="end of prune")
    parser.add_argument("--interval",   
            type = int,
            required = False,
            help="interval for elevation")
    parser.add_argument("--max-speed", '-mxs',  
            type = float,
            default = 7,
            required = False,
            help="end of prune")
    parser.add_argument("--min-speed", '-mis',  
            type = float,
            default = 0,
            required = False,
            help="end of prune")
    parser.add_argument("--out", '-o',  
            required = False,
            help="outpute")
    args = parser.parse_args()
    if args.type == 'prune-number'  and not args.start:
        parser.error('-s is required when type is prune-number .')
    if args.type == 'prune-number'  and not args.end:
        parser.error('-e is required when type is prune-number .')
    if args.type == 'prune-number'  and not args.out:
        parser.error('-o is required when type is prune-number .')
    if args.type == 'prune-speed'  and not args.out:
        parser.error('-o is required when type is prune-speed .')
    if args.type == 'smooth-segment'  and not args.out:
        parser.error('-o is required when type is smooth-segment .')
    if args.type == 'from-kml'  and not args.out:
        parser.error('-o is required when type is from-prune .')
    if args.type == 'waypoints'  and not args.interval:
        parser.error('--interval is required when type is waypoints .')
    return args

def _make_gpx_writer_segment():
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    return gpx, gpx_segment

def _get_info(point, prev_point):
    d = point.distance_3d(prev_point)
    td =  point.time_difference(prev_point) #in miliseconds
    s = point.speed_between(prev_point)
    if s:
        s = s * 2.23694
    current = _create_dt(point)
    return current, d, td, s, point.elevation

def _create_dt(point):
    if point.time == None:
        return None
    dt =  datetime.datetime.strptime(
        point.time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    dt = dt.replace(tzinfo = pytz.utc)
    return dt

def _write_gpx_to_file(gpx, path, verbose = False):
    if verbose:
        print('writting to {f}'.format(f = path))
    with  open(path, 'w') as write_obj:
        write_obj.write(gpx.to_xml())

def _make_gpx_writer_segment():
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    return gpx, gpx_segment

def _round(x, n = 0):
    if not x:
        return x
    return(round(x,n))

def convert_from_kml(in_path, out_path, verbose = False):
    import kml_to_gpx
    tree = kml_to_gpx.convert(path = in_path, 
            verbose = verbose)
    gpx_read = gpxpy.parse(tree)
    _write_gpx_to_file(gpx_read, out_path, verbose = verbose)
    return

def _round_ele(elevation, interval):
    elevation_ = elevation * 3.28084
    return round(elevation_/interval) * interval

def create_markers(
        path, elevation_interval = 300, verbose = False):
    elevation_mark = None
    prev_mile = None
    elevations = []
    miles = []
    total_distance = 0
    with  open(path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed, elevation =  _get_info(point, prev_point)
                if elevation == None:
                    continue
                if elevation < 0:
                    elevation = 0
                elevation_feet = elevation * 3.28084
                if distance:
                    total_distance += distance
                prev_point = point
                if elevation_mark != None \
                    and math.floor(elevation_feet/elevation_interval) != elevation_mark:
                    mark_elevation = math.floor(elevation_feet/elevation_interval) * elevation_interval
                    elevations.append({'elevations':_round(
                            elevation = point.elevation,
                            interval = elevation_interval,
                            ),
                        'elevations': elevation_mark * elevation_interval,
                        'lattitude':point.latitude,
                        'longitude': point.longitude,
                        'elevation': point.elevation * 3.28084
                        }
                            )

                if prev_mile != None and math.floor(total_distance * 0.000621371) != prev_mile:
                    mile_mark = math.floor(total_distance * 0.000621371)
                    miles.append({'mile':mile_mark,
                        'lattitude':point.latitude,
                        'longitude': point.longitude,
                        'elevation': point.elevation
                        }
                            )
                prev_mile = math.floor(total_distance * 0.000621371)
                elevation_mark = math.floor(elevation_feet/elevation_interval)

    return elevations, miles


def view(path, out_path):
    if not out_path:
        out_path = os.path.join(os.environ['HOME'], 'Downloads', 'out_{uuid}.csv'.format(
            uuid = uuid.uuid1().hex))
        print('out path is {o}'.format(o = out_path))
    start_time = None
    total_distance = 0
    elevation_mark = None
    prev_mile = None
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    with open(out_path, 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['num', 'current_time', 'distance', 
            'time_from_last', 'speed', 'elevation', 
            'total_distance', 'elevation_gain' ])
        for track in gpx_read.tracks:
            for segment in track.segments:
                prev_point = None
                for counter, point in enumerate(segment.points):
                    current_time, distance, time_bet, speed, elevation =  _get_info(point, prev_point)
                    elevation_feet = elevation * 3.28084
                    if not start_time:
                        start_time = current_time
                    current_time_pacific = datetime.datetime(1900,1,1)
                    if current_time:
                        current_time_pacific = current_time.astimezone(timezone('US/Pacific'))
                    if distance:
                        total_distance += distance
                    prev_point = point
                    if elevation_mark != None  and math.floor(elevation_feet/300) != elevation_mark:
                        mark_elevation = math.floor(elevation_feet/300) * 300
                    else:
                        mark_elevation = ''
                    if prev_mile != None and math.floor(total_distance * 0.000621371) != prev_mile:
                        mile_mark = math.floor(total_distance * 0.000621371)
                    else:
                        mile_mark = ''
                    prev_mile = math.floor(total_distance * 0.000621371)
                    csv_writer.writerow([counter + 1, 
                        current_time_pacific.strftime('%Y-%m-%d %H:%M:%S'), 
                        _round(distance), 
                        _round(time_bet), _round(speed,1), 
                        round(elevation_feet,0),  
                        round(total_distance * 0.000621371, 2),
                        mark_elevation,
                        mile_mark,
                        ])
                    elevation_mark = math.floor(elevation_feet/300)
        if current_time:
            total_time = current_time - start_time
        else:
            total_time = None
        total_distance_ = round(total_distance * 0.000621371, 1)
        if total_time:
            mph = total_distance_/(total_time.total_seconds()/3600)
        if total_time:
            csv_writer.writerow(['', total_time, total_distance_, '', mph])

def create_track_prune_excess_speed(in_path, verbose, max_speed = 7, 
        min_speed = 0,
        out_path = None):
    start_time = None
    total_distance = 0
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(in_path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed =  _get_info(point, prev_point)
                prev_point = point
                if speed != None and (speed < min_speed or  speed > max_speed):
                    if verbose:
                        print('skipping')
                        continue
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                            )
    _write_gpx_to_file(gpx_writer, out_path, verbose = verbose)

def create_track_by_numbers(in_path, start_num, end_num,out_path = None,
        verbose = False):
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(in_path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            for counter, point in enumerate(segment.points):
                if counter +1 >= start_num and counter + 1 <= end_num:
                    gpx_segment.points.append(
                            gpxpy.gpx.GPXTrackPoint(
                                latitude = point.latitude, 
                                longitude = point.longitude, 
                                elevation=point.elevation,
                                time = point.time
                                )
                            )

                else: 
                    if verbose:
                        print('skipping')
    _write_gpx_to_file(gpx_writer, out_path, verbose = verbose)

def smooth_and_simplify(in_path, verbose = False):
    with  open(in_path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    cloned_simplified = gpx_read.clone()
    cloned_simplified.simplify()
    base = os.path.splitext(in_path)[0]
    _write_gpx_to_file(
            gpx = cloned_simplified, path = f'{base}_simplified.gpx', 
            verbose = verbose)
    cloned = gpx_read.clone()
    cloned.reduce_points(min_distance = 100)
    _write_gpx_to_file(
            gpx = cloned, path = f'{base}_reduced.gpx', 
            verbose = verbose)

def create_track_from_segments(in_path, out_path, verbose = False ):
    """
    KML will often result in many segments; this function makes on continuous GPX
    """
    start_time = None
    total_distance = 0
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(in_path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            for counter, point in enumerate(segment.points):
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                            )
    _write_gpx_to_file(gpx_writer, out_path, verbose = True)

def _get_tree_from_path(in_path):
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(in_path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    return gpx_read

def _get_waypoints_path(in_path):
    dir_name, base_name = os.path.split(in_path)
    date_s = base_name[6:16]
    date = datetime.datetime.strptime(date_s, '%Y-%m-%d')
    month = date.strftime('%B').upper()
    day = date.strftime('%d')
    year = date.strftime('%y')
    d_s = f'{day}-{month}-{year}'
    waypoints_base_name = f'Waypoints_{d_s}.gpx'
    waypoints_path = os.path.join(dir_name, waypoints_base_name)
    if not os.path.isfile(waypoints_path):
        return None
    return waypoints_path

def _make_tracks_list(tree) -> list:
    final = []
    for track in tree.tracks:
        for segment in track.segments:
            for counter, point in enumerate(segment.points):
                final.append( gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            ))
    return final

def _get_highest_point(track_list):
    max_ = (None, None)
    for counter, i in enumerate(track_list):
        e = i.elevation
        if max_[1] == None or i.elevation > max_[1]:
            max_ = (counter, i.elevation)
    return max_

def _is_breadcrumb(s):
    try:
        i = int(s)
        return True
    except ValueError:
        return False

def _fix_waypoints(waypoints):
    final = []
    for i in waypoints:
        if not _is_breadcrumb(i.name):
            final.append(i)
    return final

def _make_separate_waypoints(path, waypoints):
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    dir_name, base_name = os.path.split(path)
    out_path = os.path.join(dir_name, 'sep_waypoints.gpx')
    for i in waypoints:
        gpx_writer.waypoints.append(i)
    _write_gpx_to_file(gpx_writer, path = out_path)

def waypoints(path, interval, verbose):
    elevations, miles =  create_markers(
            path, 
            verbose = verbose, 
            elevation_interval = interval)
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    dir_name, base_name = os.path.split(path)
    def create_waypoint(info, key):
        gpx_wps = gpxpy.gpx.GPXWaypoint()
        gpx_wps.latitude = info['lattitude']
        gpx_wps.longitude = info['longitude']
        #gpx_wps.symbol = "Marks-Mooring-Float"

        gpx_wps.name = f"{info[key]}"
        #gpx_wps.description = "Vaarwater GRUTTE GAASTMAR"
        return gpx_wps
        gpx.waypoints.append(gpx_wps)
    for i in miles:
        w=create_waypoint(info = i, key= 'mile')
        gpx_writer.waypoints.append(w)
    base_name, ext = os.path.splitext(base_name)
    out_path = os.path.join(dir_name, f'{base_name}_miles_waypoints.gpx')
    _write_gpx_to_file(gpx_writer, path = out_path, verbose = verbose)

    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    for i in elevations:
        w=create_waypoint(info = i, key = "elevations")
        gpx_writer.waypoints.append(w)
    out_path = os.path.join(dir_name, f'{base_name}_elevations_waypoints.gpx')
    _write_gpx_to_file(gpx_writer, path = out_path, verbose = verbose)

    def make_diff_elevations():
        d = {}
        for i in elevations:
            e = i['elevations']
            if not d.get(e):
                d[e] = []
            d[e].append(i)
        return d

    d = make_diff_elevations()
    for key in d.keys():
        gpx_writer, gpx_segment = _make_gpx_writer_segment()
        for i in d[key]:
            w=create_waypoint(info = i, key = "elevations")
            gpx_writer.waypoints.append(w)
        out_path = os.path.join('/home/henry/Downloads/elevations', 
                f'{key}_elevations_waypoints.gpx')
        _write_gpx_to_file(gpx_writer, path = out_path, verbose = verbose)




def map_from_walk(in_path, verbose):
    tracks_tree = _get_tree_from_path(in_path)
    waypoints_path = _get_waypoints_path(in_path)
    waypoints_tree = None
    if waypoints_path:
        waypoints_tree = _get_tree_from_path(waypoints_path)
    track_points = _make_tracks_list(tracks_tree)
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    counter, elevation = _get_highest_point(track_points)
    climb = track_points[0:counter]
    waypoints = waypoints_tree.waypoints
    for i in climb:
        gpx_segment.points.append(i)
    waypoints = _fix_waypoints(waypoints)
    for i in waypoints:
        gpx_writer.waypoints.append(i)
    _write_gpx_to_file(gpx_writer, path = '/home/henry/Downloads/climb.gpx')
    _make_separate_waypoints(path = waypoints_path, waypoints = waypoints)

def climb(in_path, verbose):
    tracks_tree = _get_tree_from_path(in_path)
    track_points = _make_tracks_list(tracks_tree)
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    counter, elevation = _get_highest_point(track_points)
    climb = track_points[0:counter]
    for i in climb:
        gpx_segment.points.append(i)
    dir_name, base_name = os.path.split(in_path)
    base_name, ext = os.path.splitext(base_name)
    out_path = os.path.join(dir_name, f'{base_name}_climb.gpx')
    _write_gpx_to_file(gpx_writer, path = out_path)




if __name__ == '__main__':
    args = _get_args()
    if args.type == 'view':
        view(path = args.path, 
                out_path = args.out)
    elif args.type == 'prune':
        create_track_by_numbers(in_path = args.path, 
            start_num = args.start, end_num = args.end, out_path = args.out,
            verbose = args.verbose)
    elif args.type == 'prune-speed':
        create_track_prune_excess_speed(in_path = args.path, 
            out_path = args.out,
            max_speed = args.max_speed,
            min_speed = args.min_speed,
            verbose = args.verbose)
    elif args.type == 'prune-number':
        create_track_by_numbers(in_path = args.path, 
        start_num = args.start, end_num = args.end,
        out_path = args.out,
        verbose = args.verbose)
    elif args.type == 'join-segment':
        create_track_from_segments(
                in_path = args.path, 
                out_path = args.out, 
                verbose = args.verbose )
    elif args.type == 'smooth':
        smooth_and_simplify(
                in_path = args.path, 
                verbose = args.verbose )
    elif args.type == 'from-kml':
        convert_from_kml(
                in_path = args.path, 
                out_path = args.out, 
                verbose = args.verbose )
    elif args.type == 'map-from-walk':
        map_from_walk(
                in_path = args.path, 
                verbose = args.verbose )
    elif args.type == 'create-markers':
        create_markers(path = args.path,
                verbose = args.verbose)
    elif args.type == 'waypoints':
        waypoints(path = args.path,
                interval = args.interval,
                verbose = args.verbose)
    elif args.type == 'climb':
        climb(in_path = args.path,
                verbose = args.verbose)
    else:
        raise  GpxError('arg not found')
