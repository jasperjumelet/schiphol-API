import json
import logging

_logger = logging.getLogger(__name__)

from flask import Flask
# might need to import CORS to avoid browser checks

from .routes import rest_api
from .models import db
from .utils import initialize_data


_logger.info("Starting airports api")

app = Flask(__name__)

app.config.from_object('api.config.BaseConfig')

db.init_app(app)
rest_api.init_app(app)

# Database setup and import of json files
@app.before_first_request
def initialize_database():
    db.create_all()
    initialize_data()

@app.after_request
def after_request(response):
    """
    Sends back a custom error with {"success", "msg"} format
    """
    if int(response.status_code) >= 400:
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data = {"success": False,
                             "msg": list(response_data["errors"].items())[0][1]}
            response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response
