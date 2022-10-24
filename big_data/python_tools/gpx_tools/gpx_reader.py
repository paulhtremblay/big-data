import os
import argparse
import datetime
from pytz import timezone
import pytz

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
    parser.add_argument("--type", '-t', choices = ['view', 'prune'],
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
    parser.add_argument("--out", '-o',  
            required = False,
            help="outpute")
    args = parser.parse_args()
    if args.type == 'prune'  and not args.start:
        parser.error('-s is required when type is prune .')
    if args.type == 'prune'  and not args.end:
        parser.error('-e is required when type is prune .')
    if args.type == 'prune'  and not args.out:
        parser.error('-o is required when type is prune .')
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
    current = _create_dt(point)
    return current, d, td, s

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

def _round(x):
    if not x:
        return x
    return(round(x))

def view(path):
    out_path = os.path.join(os.environ['HOME'], 'Downloads', 'out_{uuid}.csv'.format(
        uuid = uuid.uuid1().hex))
    print('out path is {o}'.format(o = out_path))
    start_time = None
    total_distance = 0
    gpx_writer, gpx_segment = _make_gpx_writer_segment()
    with  open(path, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    with open(out_path, 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['num', 'current_time', 'distance', 'time_from_last', 'speed' ])
        for track in gpx_read.tracks:
            for segment in track.segments:
                prev_point = None
                for counter, point in enumerate(segment.points):
                    current_time, distance, time_bet, speed =  _get_info(point, prev_point)
                    if not start_time:
                        start_time = current_time
                    current_time_pacific = current_time.astimezone(timezone('US/Pacific'))
                    if distance:
                        total_distance += distance
                    prev_point = point
                    csv_writer.writerow([counter + 1, 
                        current_time_pacific.strftime('%Y-%m-%d %H:%M:%S'), 
                        _round(distance), 
                        _round(time_bet), _round(speed)])
        total_time = current_time - start_time
        total_distance_ = round(total_distance/1500 * .62, 1)
        csv_writer.writerow(['', total_time, total_distance_])

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
    _write_gpx_to_file(gpx_writer, out_path, verbose = verbose)

if __name__ == '__main__':
    args = _get_args()
    if args.type == 'view':
        view(path = args.path)
    elif args.type == 'prune':
        create_track_by_numbers(in_path = args.path, 
            start_num = args.start, end_num = args.end, out_path = args.out,
            verbose = args.verbose)
