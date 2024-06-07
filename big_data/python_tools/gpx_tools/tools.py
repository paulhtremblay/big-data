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


def find_nearest(point, points):
    nearest = (None, None)
    for counter, i in enumerate(points):
        distance = haversine_distance(
            latitude_1 =  point[0], 
            longitude_1 = point[1], 
            latitude_2 = i[0], 
            longitude_2 = i[1]    
        )
        if nearest[1] == None or distance < nearest[1]:
            nearest = (counter, distance)
    return nearest



