from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from typing import Optional


db = SQLAlchemy()

# ------------- USER ----------------------

class newUser(BaseModel): # nie wiem czy to wgl potrzebne, może to się przyda jako schema do requestow?
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
    
# -------------------- AIRPORT - lotniska (w Polsce i miejscach, które są celem podróży) --------------------

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

# -------------------- LOCATION - hotele, domki itd. ------------------

class newLocation(BaseModel): 
    country: str
    city: str
    airport: str
    desc: str

class Location(db.Model):
    __tablename__="locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String, nullable=False)
    airport = db.Column(db.String, nullable=False) # kod IATA najbliższego lotniska (powinno się zgadzać z API)
    desc = db.Column(db.String, nullable=False) #  opis lokacji (do wrzucenia na stronę?)

    def to_dict(self):
        return {"id": self.id, "country": self.country, "city": self.city, "airport": self.airport, "desc": self.desc}


# ---------------------- BOOKING - rezerwacje --------------------

class newBooking(BaseModel):
    bookingId: str
    userId: str
    flightId: str
    locationId: str
    departureDate: str
    returnDate: str

class Booking(db.Model): # TODO: dodać relacje z innymi tabelami
    __tablename__="bookings"
    bookingId = db.Column(db.String, primary_key=True, autoincrement=True)
    userId = db.Column(db.String, nullable=False)
    flightId = db.Column(db.String, nullable=False)
    locationId = db.Column(db.String, nullable=False)
    departureDate = db.Column(db.String, nullable=False)
    returnDate = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"bookingId": self.bookingId, "userId": self.userId, "flightId": self.flightId, "locationId": self.locationId, "departureDate": self.departureDate, "returnDate": self.returnDate}


# ------------------------- FLIGHT - loty (z API, można zasymulować dane [ np. dane z API powielić wiele razy dla różnych dat ] ) ---------------

# TODO: zrobic tabele na podstawie API (AirLabs?)
    
