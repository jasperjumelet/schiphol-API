import json

from math import sin, cos, sqrt, atan2, radians

from flask_restx import Api, Resource, fields
from flask import jsonify
from .models import db, Airlines, Airports, Flights
# from .config import BaseConfig

rest_api = Api(version="1.0", title="Airport API")

"""
    Flask-Restx models for api request and response data
"""

flight_api = rest_api.model('flights', {"airlineId": fields.String(),
                                        "flightNumber": fields.Integer(),
                                        "departureAirportId": fields.String(),
                                        "arrivalAirportId": fields.String})

all_airports_api = rest_api.model('airports', {"id": fields.String(),
                                           "name": fields.String(),
                                           "distance": fields.Integer()})

specific_airport_api = rest_api.model('airport_id', {"id": fields.String(),
                                                     "latitude": fields.Float(),
                                                     "longitude": fields.Float(),
                                                     "name": fields.String(),
                                                     "city": fields.String(),
                                                     "countryId": fields.String()})

airlines_api = rest_api.model('airlines', {"id": fields.String(),
                                           "name": fields.String(),
                                           "totalDistance": fields.Integer()})

"""
    Flask-Restx parsers
"""
parser = rest_api.parser()
parser.add_argument('airport_id', type=str, required=False, help='airport specific by id')                                                     

"""
    Flask-Restx routes
"""

@rest_api.route('/flights')
class Flightsapi(Resource):
    """
    Get all flights
    """
    @rest_api.marshal_list_with(flight_api)
    def get(self):
        flights = Flights.query.all()
        response = [{'airlineId': item.airlineId,
                     'flightNumber': item.flightNumber,
                     'departureAirportId': item.departureAirportId,
                     'arrivalAirportId': item.arrivalAirportId} for item in flights]
        return response
    
@rest_api.route('/airports')
class AllAirportsapi(Resource):
    def calcDistSchiphol(self, lat, lon):
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

    @rest_api.marshal_list_with(all_airports_api)
    def get(self):
        airports = Airports.query.all()

        response = []

        for airport in airports:
           response.append({'id': airport.id,
                           'name': airport.name,
                           'distance': self.calcDistSchiphol(airport.latitude, airport.longitude)})
        
        response = sorted(response, key=lambda x: x['distance'])
        return response

@rest_api.route("/airports/<string:id>")
class SpecificAirportapi(Resource):

    @rest_api.marshal_list_with(specific_airport_api)
    def get(self, id): 
        airport = Airports.query.filter_by(id=id).first()
        response = [{"id": airport.id, 
                     "latitude": airport.latitude, 
                     "longitude": airport.longitude, 
                     "name": airport.name,
                     "city": airport.city,
                     "countryId": airport.countryId}]
        return response

@rest_api.route("/airlines")
class Airlinesapi(Resource):
    
    def calcDistSchiphol(self, lat, lon):
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

    @rest_api.marshal_list_with(airlines_api)
    def get(self):
        airlines = Airlines.query.all()
        response = []
        for airline in airlines:
            flights = Flights.query.filter_by(airlineId=airline.id)
            
            totalDistanceAirline = 0

            for flight in flights:
                airport = Airports.query.filter_by(id=flight.arrivalAirportId).first()
                totalDistanceAirline += self.calcDistSchiphol(airport.latitude, airport.longitude)
            
            response.append([{"id": airline.id,
                         "name": airline.name,
                         "totalDistance": totalDistanceAirline}])
        return response
