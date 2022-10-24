import argparse
import gpxpy
import gpxpy.gpx
import datetime
import pprint
pp = pprint.PrettyPrinter(indent = 4)

class GpxError(Exception):
    pass

def view():
    with  open('/home/henry/Downloads/track_march_02.gpx', 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                if prev_point:
                    print('Point at ({0},{1}) -> {2}'.format(
                        point.latitude, point.longitude, point.elevation))
                    print('time diff in seconds is {s}'.format(
                        s =point.time_difference(prev_point)))
                    print('datetime is {d}'.format(
                        d = datetime.datetime.strptime(
                        point.time.strftime('%Y-%m-%d %H:%M:%S'), 
                        '%Y-%m-%d %H:%M:%S')))
                    print('distance from last in meters isa {d} '.format(
                        d = point.distance_2d(prev_point)))
                    print('speed in m/s is {s}'.format(
                        s = point.speed_between(prev_point)))
                if prev_point:
                    break
                prev_point = point

def create_track():
    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    with  open('/home/henry/Downloads/track_march_02.gpx', 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)
            for point in segment.points:
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                        )

    with  open('/home/henry/Downloads/track_test_gpx.gpx', 'w') as write_obj:
        write_obj.write(gpx.to_xml())
def create_dt(point):
    return datetime.datetime.strptime(
        point.time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

def my_filter(point, prev_point):
    dt=create_dt(point)  


def get_info(point, prev_point):
    d = point.distance_3d(prev_point)
    td =  point.time_difference(prev_point) #in miliseconds
    s = point.speed_between(prev_point)
    current = create_dt(point)
    return current, d, td, s

def make_gpx_writer_segment():
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    return gpx, gpx_segment

def write_gpx_to_file(gpx, path, verbose = False):
    if verbose:
        print('writting to {f}'.format(f = path))
    with  open(path, 'w') as write_obj:
        write_obj.write(gpx.to_xml())

def create_track_not_over_speed(in_file, out, max_speed = 3.2, min_speed = 0, 
        verbose = False, start_time = None, end_time = None,
        continue_after_max = False):
    gpx_writer, gpx_segment = make_gpx_writer_segment()
    with  open(in_file, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed =  get_info(point, prev_point)
                prev_point = point
                if speed and speed < min_speed:
                    continue
                if speed and speed > max_speed:
                    if verbose:
                        print(point.time)
                        print("speed {s} over {m}, so returning.".format(s = speed, m = max_speed))
                        print('writing {n} points'.format(n= counter))
                    if continue_after_max:
                        continue
                    else:
                        write_gpx_to_file(gpx_writer, out,  verbose = verbose)
                        return
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                        )
    write_gpx_to_file(gpx_writer, out, verbose = verbose)


def get_walking_tracks(in_file,  max_speed = 3.2, min_speed = 0, 
        verbose = False):
    """Stops at first singn of excessive speed"""
    all_tracks = [[]]
    final = []
    with  open(in_file, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            is_over = False
            n_over = 0
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed =  get_info(point, prev_point)
                prev_point = point
                if speed and speed > max_speed:
                    n_over += 1
                    if not is_over:
                        all_tracks.append([])
                    is_over = True
                else:
                    is_over = False
                    all_tracks[-1].append(create_dt(point))
    for i in all_tracks:
        final.append((len(i), i[0], i[-1]))
    return final

def create_track_time_range(in_file, out, start_time, end_time, 
        max_speed = 3.2, min_speed = 0, verbose = False):
    gpx_writer, gpx_segment = make_gpx_writer_segment()
    with  open(in_file, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed =  get_info(point, prev_point)
                if current_time < start_time or\
                        current_time > end_time :
                    continue
                if speed:
                    if speed > max_speed:
                        raise GpxError('speed {s} is over allowed {m}'.format(
                            s = speed, m = max_speed))
                prev_point = point
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                        )

    write_gpx_to_file(gpx_writer, out,  verbose = verbose)

def create_track_time_range2(in_file, out, verbose = False):
    gpx_writer, gpx_segment = make_gpx_writer_segment()
    with  open(in_file, 'r') as gpx_file:
        gpx_read = gpxpy.parse(gpx_file)
    for track in gpx_read.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                current_time, distance, time_bet, speed =  get_info(point, prev_point)
                if current_time < datetime.datetime(2022,1,5):
                    continue
                gpx_segment.points.append(
                        gpxpy.gpx.GPXTrackPoint(
                            latitude = point.latitude, 
                            longitude = point.longitude, 
                            elevation=point.elevation,
                            time = point.time
                            )
                        )

    write_gpx_to_file(gpx_writer, out,  verbose = verbose)

def view2(in_file, verbose = False):
    n = 0
    with  open(in_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            prev_point = None
            for counter, point in enumerate(segment.points):
                n+= 1
    if verbose:
        print('created {n} points'.format(n = n))

if __name__ == '__main__':
    #in_file = '/home/henry/Downloads/Track_2020-09-08 190333.gpx'
    in_file = '/home/henry/Downloads/Track_2022-01-06 163548.gpx'
    out = '/home/henry/Downloads/jan_6_walk_out.gpx'
    create_track_time_range2(in_file, out)

    #out2 = '/home/henry/Downloads/walk_ny_eve2_track.gpx'
    #out_1 = '/home/henry/Downloads/walk_ny_eve_1_track.gpx'
    #start_time = datetime.datetime(2020, 12, 31, 21, 27, 34)
    #end_time = datetime.datetime(2021, 12, 31, 21, 27, 34)




if __name__ == '__main__n':
    #view()
    #create_track()
    #just get track until speed too much. Very useful in most cases
    create_track_not_over_speed(in_file = in_file, 
            out = '/home/henry/Downloads/camadan_beach.gpx', 
            verbose = True)
    f = get_walking_tracks(in_file,  max_speed = 3.2, min_speed = 0, verbose = True) 
    f = [x for x in f if x[0] > 45]
    # get the last track, because that was the art garden
    print(f[-1])
    create_track_time_range(in_file = in_file, 
            out = '/home/henry/Downloads/art_gallery.gpx', 
            start_time = f[-1][1], end_time = f[-1][2], 
            max_speed = 3.2, min_speed = 0, verbose = False)
