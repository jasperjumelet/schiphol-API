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
    
    # Check if filter by airlineId returns correct content
    req_specific_airline = client.get("/flights/t1")
    assert [airline1, airline2] == req_specific_airline.get_json()

    # Check if invalid filter gives 404
    req_invalid_airline = client.get("/flights/invalid")
    assert 404 == req_invalid_airline.status_code


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

    req_airport_km = client.get("/airports?distanceUnit=999999km")
    req_airport_km_data = req_airport_km.get_json()
    assert 200 == req_airport_km.status_code
    assert [airport1, airport2] == req_airport_km_data

    req_airline_km = client.get("/airports?distanceUnit=40km")
    assert req_airport_km.status_code == 200
    
    # test miles filter
    req_airport_mi = client.get("/airports?distanceUnit=999999mi")
    req_airport_mi_data = req_airport_mi.get_json()
    assert 200 == req_airport_mi.status_code
    assert [airport1, airport2] == req_airport_mi_data

    req_airline_mi = client.get("/airports?distanceUnit=40mi")
    assert req_airline_mi.status_code == 200


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

    # test km filter
    req_airline_km = client.get("/airlines?distanceUnit=999999km")
    req_airline_km_data = req_airline_km.get_json()
    assert 200 == req_airline_km.status_code
    assert airlines == req_airline_km_data[0]

    req_airline_km = client.get("/airlines?distanceUnit=40km")
    assert req_airline_km.status_code == 404
    
    # test miles filter
    req_airline_mi = client.get("/airlines?distanceUnit=999999mi")
    req_airline_mi_data = req_airline_mi.get_json()
    assert 200 == req_airline_mi.status_code
    assert airlines == req_airline_mi_data[0]

    req_airline_mi = client.get("/airlines?distanceUnit=40mi")
    assert req_airline_mi.status_code == 404