import gpxpy
import gpxpy.gpx

with  open('/home/henry/Downloads/track_march_02.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            print(dir(point))
            print(point.time)
            print(point.time_difference)
            break
