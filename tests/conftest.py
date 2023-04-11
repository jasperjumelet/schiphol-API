import pytest

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api import create_app, db
from api.database_init import initialize_airlines, initialize_airports, initialize_flights


def initialize_test_data():
    with open('tests/testdata/test_airlines.json', 'r') as f:
        initialize_airlines(json.load(f)) 
    with open('tests/testdata/test_airports.json') as f:
        initialize_airports(json.load(f))
    with open('tests/testdata/test_flights.json') as f:
         initialize_flights(json.load(f))
    

@pytest.fixture()
def app():
    app = create_app(config="test")
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
            db.create_all()
            initialize_test_data()
    yield app
    # Remove database file after testing
    os.unlink(os.getcwd() + '/instance/test.db')

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

    
