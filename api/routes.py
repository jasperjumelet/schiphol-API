import json

from flask_restx import Api, Resource, fields, reqparse
from flask import jsonify
from .utils import calcDistSchiphol, distance_type
from .models import db, Airlines, Airports, Flights
import logging

_logger = logging.getLogger(__name__)

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
parser.add_argument('airport_id', type=str, required=False, help='Need to fill in a valid id')                                                     
parser.add_argument('airline_id', type=str, required=False, help='Need to fill in a valid id')                                                     
parser.add_argument('distanceUnit', type=distance_type, required=False, help='Distance cannot be blank')
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
    
@rest_api.route('/flights/<string:airline_id>')
class Flightsapi(Resource):
    """
    Get all flights
    """
    @rest_api.marshal_list_with(flight_api)
    def get(self, airline_id):
        try:
            flight = Flights.query.filter_by(airlineId=airline_id)
            response = [{'airlineId': flight.airlineId,
                        'flightNumber': flight.flightNumber,
                        'departureAirportId': flight.departureAirportId,
                        'arrivalAirportId': flight.arrivalAirportId}]
            return response
        except AttributeError:
            _logger.error(f"airlineId: {airline_id} is invalid or non existend")
            return {"error": f"could not find id: {airline_id} in database"}, 404
@rest_api.route('/airports')
class AllAirportsapi(Resource):
    @rest_api.expect(parser)
    @rest_api.marshal_list_with(all_airports_api)
    def get(self):
        distance = parser.parse_args().get('distanceUnit', None)
        if distance:
            airports = Airports.query.filter(Airports.distToAMS < distance).all()
        else:
            airports = Airports.query.all()

        response = []

        for airport in airports:
           response.append({'id': airport.id,
                           'name': airport.name,
                           'distance': airport.distToAMS})
        
        response = sorted(response, key=lambda x: x['distance'])
        return response

@rest_api.route("/airports/<string:id>")
class SpecificAirportapi(Resource):

    @rest_api.marshal_list_with(specific_airport_api)
    def get(self, id): 
        try:
            airport = Airports.query.filter_by(id=id).first()
            response = [{"id": airport.id, 
                        "latitude": airport.latitude, 
                        "longitude": airport.longitude, 
                        "name": airport.name,
                        "city": airport.city,
                        "countryId": airport.countryId}]
            
            return response
        except AttributeError:
            _logger.error(f"id: {id} is invalid or non existend")
            return {"error": f"could not find id: {id} in database"}, 404

@rest_api.route("/airlines")
class Airlinesapi(Resource):

    @rest_api.expect(parser)
    @rest_api.marshal_list_with(airlines_api)
    def get(self):
        distance = parser.parse_args().get('distanceUnit', None)
        airlines = Airlines.query.all()
        response = []
        for airline in airlines:
            flights = Flights.query.filter_by(airlineId=airline.id)
            
            totalDistanceAirline = 0

            for flight in flights:
                if distance:
                    airport = Airports.query.filter((Airports.distToAMS < distance) & (Airports.id == flight.arrivalAirportId)).all()
                else:
                    airport = Airports.query.filter_by(id=flight.arrivalAirportId).first()
                totalDistanceAirline += airport.distToAMS
            
            response.append({"id": airline.id,
                         "name": airline.name,
                         "totalDistance": totalDistanceAirline})
        return response
