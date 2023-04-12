from .models import db
from .database_init import initialize_data

def reinitialize_database():
    db.drop_all()
    db.create_all
    initialize_data()
