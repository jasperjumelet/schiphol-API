import json
import logging

_logger = logging.getLogger(__name__)

from flask import Flask
# might need to import CORS to avoid browser checks

from .routes import rest_api
from .models import db
from .database_init import initialize_data

def create_app(config="dev"):
    _logger.info("Starting airports api")

    app = Flask(__name__)

    if config == "test":
        app.config.from_object('api.config.TestConfig')
    # This else statement can be split up between prod and dev
    else:
        app.config.from_object('api.config.BaseConfig')

    db.init_app(app)
    rest_api.init_app(app)

    return app
