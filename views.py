from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from db.modele import db, User, Location, Airport, Flight, Booking
import bcrypt
import re
from functools import wraps
from datetime import datetime, timedelta # <--- To jest kluczowe
from ftfy import fix_text

views = Blueprint(__name__, "views")


# --- DEKORATOR: WYMAGANY ADMIN ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Sprawdzamy czy użytkownik jest w ogóle zalogowany
        if 'user_id' not in session:
            flash("Musisz się zalogować, aby wejść do panelu.", "error")
            return redirect(url_for('views.login'))

        # 2. Pobieramy użytkownika z bazy i sprawdzamy rolę
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash("Brak uprawnień administratora!", "error")
            return redirect(url_for('views.home'))

        return f(*args, **kwargs)

    return decorated_function


# ==========================================
#              TRASY PUBLICZNE
# ==========================================

@views.route("/")
def home():
    # 1. Pobieramy wszystkie lokalizacje (do dropdowna Cel podróży)
    all_locations_raw = Location.query.all()

    # Debug: Sprawdźmy w konsoli czy w ogóle są dane
    print(f"DEBUG: Znaleziono {len(all_locations_raw)} lokalizacji w bazie.")

    # Filtrujemy duplikaty miast (żeby nie było dwa razy Barcelony)
    unique_destinations = {}
    for loc in all_locations_raw:
        # Używamy nazwy miasta jako klucza
        if loc.city not in unique_destinations:
            unique_destinations[loc.city] = loc

    # Tworzymy listę unikalnych celów podróży
    destinations = list(unique_destinations.values())

    # Naprawa specjalnych znaków do utf-8
    fixed_destinations = []
    for location in destinations:
        location.name = fix_text(location.name)
        location.country = fix_text(location.country)
        location.city = fix_text(location.city)
        fixed_destinations.append(location)
    destinations = list(fixed_destinations)

    # 2. Pobieramy lotniska wylotu (Origins) - te, z których są loty
    existing_origins_query = db.session.query(Flight.departureIata).distinct().all()
    origin_iatas = [r[0] for r in existing_origins_query]

    if origin_iatas:
        origins = Airport.query.filter(Airport.iata.in_(origin_iatas)).all()
    else:
        origins = []

    # 3. Pobieramy dostępne daty (bez godzin)
    raw_dates = db.session.query(Flight.departureDate).all()
    # Spłaszczamy listę, ucinamy godzinę (split) i sortujemy unikalne daty
    available_dates = sorted(list(set([d[0].split(' ')[0] for d in raw_dates])))

    # 4. Sekcja Popularne (Recommended) - POPRAWKA
    # Zamiast filtrować po lotach (co może zwracać 0 wyników),
    # bierzemy po prostu 4 pierwsze miasta z naszej listy celów.
    # Dzięki temu sekcja zawsze będzie wypełniona, o ile w bazie są jakiekolwiek miasta.
    recommended = destinations[:4]

    # 5. Obsługa usera
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("index.html",
                           destinations=destinations,
                           origins=origins,
                           dates=available_dates,
                           recommended=recommended,
                           user=user)


@views.route("/search")
def search():
    origin_iata = request.args.get('origin_iata')
    destination_id = request.args.get('destination_id')
    date = request.args.get('date')

    query = Flight.query

    # Filtrowanie po lotnisku wylotu
    if origin_iata:
        query = query.filter(Flight.departureIata == origin_iata)

    # Filtrowanie po celu podróży
    destination_obj = None
    if destination_id:
        destination_obj = Location.query.filter_by(id=destination_id).first()
        if destination_obj:
            query = query.filter(Flight.arrivalIata == destination_obj.airport)

    # Filtrowanie po dacie
    if date:
        query = query.filter(Flight.departureDate.like(f"{date}%"))

    results = query.all()
    available_locations, available_airports, departure_times, arrival_times = [], [], [], []

    # Dla każdego lotu filtrowanie po obługiwanych lokacjach i lotniskach
    for flight in results:
        all_locations=Location.query.filter_by(airport=flight.arrivalIata).all()
        all_airports=Airport.query.filter_by(iata=flight.departureIata).all()
        if len(all_locations)!=0 and len(all_airports)!=0:
            available_locations.append(all_locations[0])
            available_airports.append(all_airports[0])
            departure_times.append(flight.departureDate)
            arrival_times.append(flight.arrivalDate)

    available_flights = []
    # Zwracamy liste rzeczy do wyświetlenia
    for x in range(len(available_locations)):
        available_flights.append([fix_text(available_airports[x].name),
                                  available_airports[x].iata,
                                  available_locations[x].airport,
                                  fix_text(available_locations[x].city),
                                  fix_text(available_locations[x].country),
                                  departure_times[x],
                                  arrival_times[x]
                                  ])

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("results.html",
                           flights=available_flights,
                           user=user,
                           search_origin=origin_iata,
                           search_dest=destination_obj)


@views.route("/kraje")
def kraje():
    # Pobieramy unikalne lokalizacje
    all_locations_raw = Location.query.all()
    unique_locations = {}
    for loc in all_locations_raw:
        if loc.city not in unique_locations:
            unique_locations[loc.city] = loc
    locations_list = list(unique_locations.values())

    # Dane do formularza wyszukiwania
    existing_origins_query = db.session.query(Flight.departureIata).distinct().all()
    origin_iatas = [r[0] for r in existing_origins_query]
    if origin_iatas:
        origins = Airport.query.filter(Airport.iata.in_(origin_iatas)).all()
    else:
        origins = []

    # Naprawa specjalnych znaków do utf-8
    fixed_locations_list = []
    for location in locations_list:
        location.name = fix_text(location.name)
        location.country = fix_text(location.country)
        location.city = fix_text(location.city)
        fixed_locations_list.append(location)
    locations_list = list(fixed_locations_list)

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("kraje.html",
                           locations=locations_list,
                           origins=origins,
                           destinations=locations_list,
                           user=user)


@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        error_message = None

        if password != confirm_password:
            error_message = "Hasła nie są takie same!"
        elif User.query.filter_by(email=email).first():
            error_message = "Ten email jest już zajęty!"

        if error_message:
            flash(error_message, "error")
        else:
            username = f"{first_name} {last_name}"
            # Haszowanie hasła
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            new_user = User(
                username=username,
                email=email,
                password=hashed_pw,
                role="user"
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Konto zostało utworzone! Możesz się zalogować.", "success")
                return redirect(url_for('views.login'))
            except Exception as e:
                db.session.rollback()
                flash("Wystąpił błąd przy zapisie do bazy.", "error")
                print(e)

    return render_template("register.html")


@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            # Weryfikacja hasła
            # Upewniamy się, że hasło z bazy jest w formacie bajtów dla bcrypt
            stored_password = user.password
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')

            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    session['user_id'] = user.id

                    # Jeśli admin, można przekierować od razu do panelu (opcjonalne)
                    if user.role == 'admin':
                        return redirect(url_for('views.admin_dashboard'))

                    return redirect(url_for('views.home'))
                else:
                    flash("Nieprawidłowe dane!", "error")
            except ValueError:
                # Fallback dla haseł w starym formacie (jeśli istnieją)
                flash("Błąd weryfikacji hasła (niepoprawny format w bazie).", "error")
        else:
            flash("Nieprawidłowe dane!", "error")

    return render_template("login.html")


@views.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Wylogowano pomyślnie.", "success")
    return redirect(url_for('views.login'))


# ==========================================
#              PANEL ADMINISTRATORA
# ==========================================

@views.route("/admin")
@admin_required
def admin_dashboard():
    current_user = User.query.get(session['user_id'])
    return render_template("admin_dashboard.html", user=current_user)


# --- UŻYTKOWNICY ---
@views.route("/admin/users")
@admin_required
def admin_users():
    current_user = User.query.get(session['user_id'])
    users = User.query.all()
    return render_template("admin_users.html", users=users, user=current_user)


@views.route("/admin/users/delete/<int:id>")
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    nazwa_uzytkownika = user.username  # Pobieramy nazwę przed usunięciem

    if user.email == 'admin@gmail.com':
        flash("Nie można usunąć głównego administratora!", "error")
    else:
        db.session.delete(user)
        db.session.commit()
        # Dynamiczny komunikat
        flash(f"Pomyślnie usunięto użytkownika: {nazwa_uzytkownika}", "success")

    return redirect(url_for('views.admin_users'))


# --- LOKALIZACJE ---
@views.route("/admin/locations", methods=['GET', 'POST'])
@admin_required
def admin_locations():
    current_user = User.query.get(session['user_id'])

    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        city = request.form.get('city')
        airport = request.form.get('airport')
        desc = request.form.get('desc')

        new_loc = Location(name=name, country=country, city=city, airport=airport, desc=desc)
        db.session.add(new_loc)
        db.session.commit()
        # Dynamiczny komunikat
        flash(f"Dodano nową lokalizację: {city} ({country})", "success")
        return redirect(url_for('views.admin_locations'))

    locations = Location.query.all()

    # Naprawa specjalnych znaków do utf-8
    fixed_locations = []
    for location in locations:
        location.name = fix_text(location.name)
        location.country = fix_text(location.country)
        location.city = fix_text(location.city)
        fixed_locations.append(location)
    locations = list(fixed_locations)

    return render_template("admin_locations.html", locations=locations, user=current_user)


@views.route("/admin/locations/delete/<int:id>")
@admin_required
def delete_location(id):
    loc = Location.query.get_or_404(id)
    nazwa_miasta = loc.city  # Pobieramy nazwę

    db.session.delete(loc)
    db.session.commit()
    # Dynamiczny komunikat
    flash(f"Usunięto lokalizację: {nazwa_miasta}", "success")
    return redirect(url_for('views.admin_locations'))


# --- LOTNISKA ---
@views.route("/admin/airports", methods=['GET', 'POST'])
@admin_required
def admin_airports():
    current_user = User.query.get(session['user_id'])

    if request.method == 'POST':
        name = request.form.get('name')
        iata = request.form.get('iata')

        if Airport.query.filter_by(iata=iata).first():
            flash(f"Lotnisko z kodem {iata} już istnieje!", "error")
        else:
            new_airport = Airport(name=name, iata=iata)
            db.session.add(new_airport)
            db.session.commit()
            # Dynamiczny komunikat
            flash(f"Dodano lotnisko: {name} ({iata})", "success")
            return redirect(url_for('views.admin_airports'))

    airports = Airport.query.all()
    return render_template("admin_airports.html", airports=airports, user=current_user)


@views.route("/admin/airports/delete/<int:id>")
@admin_required
def delete_airport(id):
    air = Airport.query.get_or_404(id)
    kod_iata = air.iata  # Pobieramy kod

    db.session.delete(air)
    db.session.commit()
    # Dynamiczny komunikat
    flash(f"Usunięto lotnisko o kodzie: {kod_iata}", "success")
    return redirect(url_for('views.admin_airports'))


# W pliku views.py

# W pliku views.py

# W pliku views.py

@views.route("/kierunek/<int:id>/loty")
def city_flights(id):
    location = Location.query.get_or_404(id)
    # Pobieramy loty (w bazie departureDate i arrivalDate to pełne napisy "YYYY-MM-DD HH:MM")
    flights = Flight.query.filter_by(arrivalIata=location.airport).all()

    # Naprawa specjalnych znaków do utf-8
    location.name = fix_text(location.name)
    location.country = fix_text(location.country)
    location.city = fix_text(location.city)

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("loty.html",
                           location=location,
                           flights=flights,
                           user=user)


@views.route("/rezerwacje")
def my_reservations():
    # Sprawdzamy czy użytkownik jest zalogowany
    if 'user_id' not in session:
        flash("Zaloguj się, aby zobaczyć swoje rezerwacje.", "error")
        return redirect(url_for('views.login'))

    # 1. Pobierz rezerwacje usera (szukamy po stringu userId)
    # UWAGA: Upewnij się, że masz import Booking na górze pliku!
    user_bookings = Booking.query.filter_by(userId=str(session['user_id'])).all()

    # 2. Ręczne łączenie danych
    data_to_show = []

    for booking in user_bookings:
        try:
            f_id = int(booking.flightIata)
            flight = Flight.query.get(f_id)

            if flight:
                flight.price = 350  # Wirtualna cena
                data_to_show.append((booking, flight))
        except:
            continue

    user = User.query.get(session['user_id'])
    return render_template("rezerwacje.html", bookings=data_to_show, user=user)

# W pliku views.py

@views.route("/reserve/<int:flight_id>", methods=['POST'])
def reserve_flight(flight_id):
    # 1. Sprawdzamy czy użytkownik jest zalogowany
    if 'user_id' not in session:
        flash("Musisz się zalogować, aby zarezerwować lot!", "error")
        return redirect(url_for('views.login'))

    # 2. Pobieramy lot z bazy, żeby mieć jego dane
    flight = Flight.query.get(flight_id)
    if not flight:
        flash("Błąd: Taki lot nie istnieje.", "error")
        return redirect(url_for('views.home'))

    # 3. Tworzymy rezerwację
    # WAŻNE: W polu flightIata zapisujemy ID lotu (jako tekst),
    # żeby wiedzieć dokładnie, o który lot chodzi (data, godzina).
    new_booking = Booking(
        userId=str(session['user_id']),
        flightIata=str(flight.flightId),    # <--- TUTAJ JEST KLUCZOWY ELEMENT
        locationId=flight.arrivalIata,      # Kod lotniska docelowego
        departureDate=flight.departureDate, # Data wylotu
        returnDate=flight.arrivalDate       # Data przylotu
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
        flash("Lot został pomyślnie zarezerwowany!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Błąd bazy: {e}")
        flash("Wystąpił błąd podczas rezerwacji.", "error")

    # 4. Przekierowanie do strony z rezerwacjami
    return redirect(url_for('views.my_reservations'))


@views.route('/regulamin')
def terms():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template("regulamin.html", user=user)

# W pliku views.py

@views.route("/rezerwacje/delete/<int:booking_id>")
def delete_reservation(booking_id):
    # 1. Sprawdzamy logowanie
    if 'user_id' not in session:
        flash("Musisz być zalogowany.", "error")
        return redirect(url_for('views.login'))

    # 2. Pobieramy rezerwację
    booking = Booking.query.get_or_404(booking_id)

    # 3. ZABEZPIECZENIE: Czy ta rezerwacja należy do obecnego użytkownika?
    # Konwertujemy na string, bo w modelu userId to String, a w sesji może być różnie
    if str(booking.userId) != str(session['user_id']):
        flash("Nie masz uprawnień do usunięcia tej rezerwacji!", "error")
        return redirect(url_for('views.my_reservations'))

    # 4. Usuwanie
    try:
        db.session.delete(booking)
        db.session.commit()
        flash("Rezerwacja została anulowana.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Wystąpił błąd podczas anulowania rezerwacji.", "error")

    return redirect(url_for('views.my_reservations'))
