import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    # os.environ['DATABASE_URL']
    SECRET_KEY = "da64f456dfeb4eae915bf4acc9283c9f"
