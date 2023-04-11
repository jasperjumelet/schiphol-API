from .models import Airports
from math import sin, cos, sqrt, atan2, radians


def calcDistSchiphol(lat: float, lon: float) -> int:
    """
    Fill in lat, lon of a airports and returns the distance in km to schiphol
    """
    schiphol = Airports.query.filter_by(id="AMS").first()
    
    # Radius of the earth in km
    R = 6371 

    lat1, lon1, lat2, lon2 = map(radians, [schiphol.latitude, schiphol.longitude, lat, lon])

    dlon = lon2 - lon1
    dlat = lat2- lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return int(distance)  