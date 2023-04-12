import pytest

def test_flights_api(client):
    """
    Tests for flight api
    """
    req_airlines = client.get("/flights")

    # Test if api response works
    assert 200 == req_airlines.status_code

    req_airlines_data = req_airlines.get_json()


    airline1 = {'airlineId': 't1', 
                'flightNumber': 1, 
                'departureAirportId': 'AMS',
                'arrivalAirportId': 'AMM'}

    airline2 = {'airlineId': 't1',
                'flightNumber': 2,
                'departureAirportId': 'AMS',
                'arrivalAirportId': 'AMM'}
    
    assert airline1 == req_airlines_data[0]
    assert airline2 == req_airlines_data[1]

def test_airports_api(client):
    """
    Tests for airports api
    """
    req_airports = client.get("/airports")

    # Test if api response works
    assert 200 == req_airports.status_code

    req_airports_data = req_airports.get_json()

    airport1 = {'id': 'AMS', 
                'name': 'Amsterdam-Schiphol Airport',
                'distance': 0}
    airport2 = {'id': 'AMM', 
                'name': 'Queen Alia International Airport', 
                'distance': 3401}
    
    assert airport1 == req_airports_data[0]
    assert airport2 == req_airports_data[1]

def test_airport_id_api(client):
    """
    Tests for airports filter by id api
    """
    req_airport = client.get("/airports/AMM")

    # Test if api response works
    assert 200 == req_airport.status_code

    req_airport_data =  req_airport.get_json()

    airport = {'id': 'AMM', 
               'latitude': 31.722534, 
               'longitude': 35.98932, 
               'name': 'Queen Alia International Airport', 
               'city': 'Amman', 
               'countryId': 'JO'}
    assert airport == req_airport_data[0]

    # check for error handling in invalid requests
    req_invalid_airport_data = client.get("/airports/1")
    assert 404 == req_invalid_airport_data.status_code

def test_airlines_api(client):
    """
    Tests for airlines api
    """
    req_airlines = client.get("/airlines")

    # test if api response works
    assert 200 == req_airlines.status_code

    req_airlines_data = req_airlines.get_json()

    airlines = {'id': 't1', 'name': 'Test Airline', 'totalDistance': 6802}

    assert airlines == req_airlines_data[0]
