from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from typing import Optional


db = SQLAlchemy()

# ------------- USER ----------------------

class newUser(BaseModel): 
    username: str
    password: str
    email: str
    role: Optional[str] = "user" # domyślna wartość, dla admina powinna byc wartosc "admin"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "password": self.password, "email": self.email, "role": self.role}
    
# -------------------- AIRPORT - lotniska (w Polsce) --------------------

class newAirport(BaseModel):
    name: str
    iata: str
    #icao: str

class Airport(db.Model):
    __tablename__="airports"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    iata = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "iata": self.iata}

# -------------------- LOCATION - zagraniczne cele podrozy ------------------

class newLocation(BaseModel): 
    name: str
    country: str
    city: str
    airport: str
    desc: str
    cena: int

class Location(db.Model):
    __tablename__="locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    airport = db.Column(db.String, nullable=False) # kod IATA najbliższego lotniska (powinno się zgadzać z API)
    desc = db.Column(db.String, nullable=False) #  opis lokacji 
    cena = db.Column(db.Integer, nullable=False, default=0) # cena lotu z Polski do lokacji

    def to_dict(self):
        return {"id": self.id, "name": self.name, "country": self.country, "city": self.city, "airport": self.airport, "desc": self.desc, "cena": self.cena}


# ---------------------- BOOKING - rezerwacje --------------------

class newBooking(BaseModel):
    bookingId: int
    userId: str
    flightIata: str
    locationId: str
    departureDate: str
    returnDate: str

class Booking(db.Model): 
    __tablename__="bookings"
    bookingId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String, nullable=False)
    flightIata = db.Column(db.String, nullable=False)
    locationId = db.Column(db.String, nullable=False)
    departureDate = db.Column(db.String, nullable=False)
    returnDate = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"bookingId": self.bookingId, "userId": self.userId, "flightIata": self.flightIata, "locationId": self.locationId, "departureDate": self.departureDate, "returnDate": self.returnDate}


# ------------------------- FLIGHT - loty ---------------

class newFlight(BaseModel):
    #flightIata: str
    departureIata: str
    departureDate: str
    arrivalIata: str
    arrivalDate: str

class Flight(db.Model):
    __tablename__="flights"
    flightId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #flightIata = db.Column(db.String, nullable=False)
    departureIata = db.Column(db.String, nullable=False)
    departureDate = db.Column(db.String, nullable=False)
    arrivalIata = db.Column(db.String, nullable=False)
    arrivalDate = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"flightId": self.flightId, 
                #"flightIata": self.flightIata, 
                "departureIata": self.departureIata, "departureDate": self.departureDate, "arrivalIata": self.arrivalIata, "arrivalDate": self.arrivalDate}
    
