from .models import Airlines, Airports, Flights, db
import requests
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError


_logger = logging.getLogger(__name__)

def initialize_airlines(data):
    """
    Initialization of airlines data to database
    """
    # Create a session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    for airline in data:
        new_entry = Airlines(id=airline['id'],
                             name=airline['name'])
        # Check for duplicates or type errors
        try:
            session.add(new_entry)
            session.flush()
        except (FlushError, IntegrityError):
            session.rollback()
    session.commit()

def initialize_airports(data):
    """
    Initialization of airports data to database
    """
    # Create a session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    for airport in data:
        new_entry = Airports(id=airport['id'],
                             latitude=airport['latitude'],
                             longitude=airport['longitude'],
                             name=airport['name'],
                             city=airport['city'],
                             countryId=airport['countryId'])
        # Check for duplicates or type errors
        try:
            session.add(new_entry)
            session.flush()
        except (FlushError, IntegrityError):
            session.rollback()
    session.commit()

def initialize_flights(data):
    """
    Initialization of flights data to database
    """
    # Create a session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    for flight in data:
        new_entry = Flights(airlineId=flight['airlineId'],
                            flightNumber=flight['flightNumber'],
                            departureAirportId=flight['departureAirportId'],
                            arrivalAirportId=flight['arrivalAirportId'])        
        # Check for duplicates or type errors
        try:
            session.add(new_entry)
            session.flush()
        except (FlushError, IntegrityError):
            session.rollback()

    session.commit()


def initialize_data():
    airlines = 'https://assignments-assets.datasavannah.com/schiphol/airlines.json'
    airports = 'https://assignments-assets.datasavannah.com/schiphol/airports.json'
    flights = 'https://assignments-assets.datasavannah.com/schiphol/flights.json'
    
    try:
        req_airlines = requests.get(airlines).json()
        req_airports = requests.get(airports).json()
        req_flights = requests.get(flights).json()
    except Exception as e:
        _logger.error(f"Error in initialization data requests: {e}")

    initialize_airlines(req_airlines)
    initialize_airports(req_airports)
    initialize_flights(req_flights)
