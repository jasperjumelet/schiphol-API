import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airlines(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))

class Airports(db.Model):
    id = db.Column(db.String(), primary_key=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    name = db.Column(db.String())
    city = db.Column(db.String())
    countryId = db.Column(db.String())
    distToAMS = db.Column(db.Integer())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def toDict(self):
        cls_dict = {}
        cls_dict['id'] = self.id
        cls_dict['latitude'] = self.latitude
        cls_dict['longtitude'] = self.longtitude
        cls_dict['name'] = self.name
        cls_dict['city'] = self.city
        cls_dict['country_id'] = self.country_id

        return cls_dict
    
    def toJSON(self):
        return self.toDict()

class Flights(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    airlineId = db.Column(db.String())
    flightNumber = db.Column(db.Integer())
    departureAirportId = db.Column(db.String())
    arrivalAirportId = db.Column(db.String())

