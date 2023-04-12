from .models import Airports
from math import sin, cos, sqrt, atan2, radians


def calcDistSchiphol(lat: float, lon: float) -> int:
    """
    Fill in lat, lon of a airports and returns the distance in km to schiphol
    """
    # define lat and lon of amsterdam (schiphol)
    lat_ams, lon_ams = (52.30907, 4.763385)
    
    # Radius of the earth in km
    R = 6371 

    lat1, lon1, lat2, lon2 = map(radians, [lat_ams, lon_ams, lat, lon])

    dlon = lon2 - lon1
    dlat = lat2- lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return int(distance)  

# Define the custom type for the distance parameter
def distance_type(value):
    if value.endswith('mi'):
        return float(value[:-2]) * 1.60934  # Convert miles to kilometers
    elif value.endswith('km'):
        return float(value[:-2])
    else:
        raise ValueError('Invalid distance unit. Must be "mi" or "km".')