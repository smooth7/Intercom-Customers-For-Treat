import math
EARTH_RADIUS_KM = 6371


def calculate_distance_km(lat_1_degree, long_1_degree, lat_2_degree, long_2_degree):

    lat_1_radians = math.radians(lat_1_degree)
    long_1_radians = math.radians(long_1_degree)
    lat_2_radians = math.radians(lat_2_degree)
    long_2_radians = math.radians(long_2_degree)
    abs_diff_long = abs(long_1_radians - long_2_radians)

    central_angle = math.acos(math.sin(lat_1_radians) * math.sin(lat_2_radians) +
                              math.cos(lat_1_radians) * math.cos(lat_2_radians) * math.cos(abs_diff_long))
    distance = EARTH_RADIUS_KM * central_angle
    return distance
