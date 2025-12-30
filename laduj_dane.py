from db.modele import db, User, newUser, Airport, newAirport, Flight, newFlight, Booking, newBooking
from pathlib import Path
import bcrypt
import csv
import json

# metody do endpointow?
def add_user(data: newUser):
    user = User(username=data.username, password=bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()), email=data.email, role=data.role)
    db.session.add(user)
    db.session.commit()

def add_airports(data: list[newAirport]):
    for air in data:
        airport = Airport(name=air.name,iata=air.iata)
        db.session.add(airport)
    db.session.commit()

def add_flights(data: list[newFlight]):
    for fl in data:
        flight = Flight(
            #flightIata=data.flightIata, 
            departureIata=fl.departureIata, departureDate=fl.departureDate, arrivalIata=fl.arrivalIata, arrivalDate=fl.arrivalDate)
        db.session.add(flight)
    db.session.commit()

def add_booking(data: newBooking): # nieużywane, ale przyda się w przyszłości
    booking = Booking(bookingId=data.bookingId, userId=data.userId, flightId=data.flightIata, locationId=data.locationId, departureDate=data.departureDate, returnDate=data.returnDate)
    db.session.add(booking)
    db.session.commit()


def load_data(app):
    with app.app_context():
        #db.drop_all()
        db.create_all()
        
        # przykładowi użytkownicy
        us1 = {
            "username": "user1",
            "password": "123",
            "email": "user1@gmail.com"}
        us2 = {
            "username": "user2",
            "password": "123",
            "email": "user2@gmail.com"}
        adm = {
            "username": "admin",
            "password": "admin123",
            "email": "admin@gmail.com",
            "role": "admin"}
        
        users = [us1,us2,adm]
        if User.query.count() == 0:
            for us in users:
                add_user(data=newUser(**us))

        # lotniska z pliku airports.csv (możecie dodać więcej)
        if Airport.query.count() == 0:
            lotniska_lista = []
            with open("./db/base_data/airports.csv","r", ) as file:
                reader = csv.DictReader(file, delimiter=";")

                for airport in reader:
                    lotniska_lista.append(newAirport(**airport))
            add_airports(lotniska_lista)

        # loty z responsow od api (db/base_data/api_data)
        if Flight.query.count() == 0:
            loty_folder = Path("./db/base_data/api_data")
            loty_lista = []
            for file in loty_folder.glob("*.json"):
                with file.open("r",) as f:
                    loty = json.load(f)
                    for lot in loty:
                        l = {
                            #"flightIata": lot['flight_iata'],  # czasami wywala błąd jeśli ładujemy kod iata lotu. TODO: naprawić?
                            "departureIata": lot['dep_iata'],
                            "departureDate": lot['dep_time'],
                            "arrivalIata": lot['arr_iata'],
                            "arrivalDate": lot['arr_time']}
                        loty_lista.append(newFlight(**l))
            add_flights(data=loty_lista)
    print("Załadowano dane")