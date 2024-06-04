import  math

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

def reverse_points(points):
    points_ = [x for x in points]
    for i in reversed(points):
        points_.append(i)
    return points_

def create_mile_markers(points, 
        reverse = False,
        verbose = False):
    if reverse:
        points = reverse_points(points)
    total_distance = 0
    prev_point = None
    prev_mile = None
    miles = []
    for point in points:
        if not prev_point:
            prev_point = point
            continue
        dis =  haversine_distance(
            latitude_1 = prev_point[0], 
            longitude_1= prev_point[1], 
            latitude_2= point[0], 
            longitude_2= point[1])     
        total_distance += dis
        if prev_mile != None and math.floor(total_distance * 0.000621371) != prev_mile:
            mile_mark = math.floor(total_distance * 0.000621371)
            miles.append({'mile':mile_mark,
                'latitude':point[0],
                'longitude': point[1],
                'elevation': point[2]
                }
                    )
        prev_mile = math.floor(total_distance * 0.000621371)
        prev_point = point
    return miles


def create_mile_markers_(
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

