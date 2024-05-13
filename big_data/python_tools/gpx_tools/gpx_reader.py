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

def _run_shell(args, verbose = False):
        if verbose:
            print(f'args are {args}')
        response = subprocess.run(
            args,  
            capture_output=True, check=True, )
        return response

def convert_from_kml(in_path, out_path, verbose = False):
    fh, out_path_temp = tempfile.mkstemp() 
    args = [
        'gpsbabel',  
        '-w',  '-i',  
        'kml',  '-f', 
        in_path, 
        '-o',  
        'gpx', 
        '-F',  
        out_path_temp
            ]
    response = _run_shell(args = args, 
            verbose = True
            )
    create_track_from_segments(
            in_path = out_path_temp, 
            out_path = out_path, 
            verbose = verbose )
    os.close(fh)
    os.remove(out_path_temp)



def _run_shell(args, verbose = False):
        if verbose:
            print(f'args are {args}')
        response = subprocess.run(
            args,  
            capture_output=True, check=True, )
        return response


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of file")
    parser.add_argument("--type", '-t', 
            choices = [
                'view', 
                'prune-number', 
                'prune-speed', 
                'smooth-segment',
                'from-kml',
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
        parser.error('-o is required when type is prune-speed .')
    if args.type == 'from-kml'  and not args.out:
        parser.error('-o is required when type is prune-speed .')
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
        total_time = current_time - start_time
        total_distance_ = round(total_distance * 0.000621371, 1)
        mph = total_distance_/(total_time.total_seconds()/3600)
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
    elif args.type == 'smooth-segment':
        create_track_from_segments(
                in_path = args.path, 
                out_path = args.out, 
                verbose = args.verbose )
    elif args.type == 'from-kml':
        convert_from_kml(
                in_path = args.path, 
                out_path = args.out, 
                verbose = args.verbose )
    else:
        raise  GpxError('arg not found')
