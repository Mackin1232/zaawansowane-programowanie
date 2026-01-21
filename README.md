# Strona firmy Travel - usługi wyszukującej nadchodzące loty samolotowe

Wymagane biblioteki są zawarte w pliku 'requirements.txt'.

Aby zobaczyć stronę należy uruchomić plik 'aplication.py', a następnie w przeglądarce wpisać url http://127.0.0.1:5000/
!UWAGA! - Uruchamiając `aplication.py` należy mieć jako bieżący katalog folder główny projektu: `zaawansowane-programowane-main`

Osobno uruchamiany plik api_request.py powoduje pobranie z API FlightLabs nadchodzących lotów (z zakresu do 8 godzin naprzód) - dane zapisywane w db/base_data/api_data
(UWAGA: Do tego pliku potrzebny jest klucz darmowego tieru API FlightLabs, zamieszczony jako API_KEY w pliku api_key.py -> ten plik nie jest zamieszczony na GitHub'ie aby uniknąć wycieku klucza)

Domyślnie można się zalogować na następujące konta (nie wliczając kont utworzonych przy rejestracji):
- user1@gmail.com ; hasło: 123
- user2@gmail.com ; hasło: 123
- admin@gmail.com ; hasło: admin123 <- konto admina ze specjalnym panelem do edytowania bazy danych

# Przepływ danych
## Start aplikacji
- `aplication.py` inicjalizuje Flask, rejestruje blueprint `views`, ładuje konfigurację, inicjalizuje bazę SQLAlchemy i zasila bazę danymi przez load_data() w 'load_data.py' - po uruchomieniu tego pliku można uzyskać dostęp do strony internetowej

## Źródła danych
- Lotniska i lokalizacje są ładowane z plików CSV (`db/base_data/airports.csv`, `db/base_data/locations.csv`).
- Loty są ładowane z plików JSON w `db/base_data/api_data`. 
- Opcjonalnie: skrypt `api_request.py` pobiera rozkłady lotów z API FlightLabs i zapisuje je do plików JSON (db/base_data/api_data), które później są importowane do bazy przy uruchomieniu aplikacji.

## Logowanie i uwierzytelnianie
- Niektóre akcje wymagają zalogowania (np. rezerwacja lotu)
- Rejestracja (`/register`) tworzy rekord w tabeli `User` (gdzie hasło jest zahaszowane za pomocą bcrypt).
- Aplikacja używa sesji Flask do uwierzytelniania: po poprawnym logowaniu w sesji zapisywane jest ID użytkownika.  
- Logowanie (`/login`) wyszukuje użytkownika po emailu i weryfikuje hasło zawarte w bazie danych.
- Wylogowanie (`/logout`) usuwa `user_id` z sesji.
- Dostęp do panelu administratora jest chroniony dekoratorem `admin_required`, który sprawdza, czy użytkownik zapisany w sesji ma uprawnienia administratora (z pola 'role' w modelu 'User')

## Przepływ żądania (UI renderowane po stronie serwera)
0. Jeśli jest to wymagane (np. przy dostępie do dashboarda admina), sprawdzane są uprawnienia użytkownika (użytkownik przechowywany w sesji).
1. Przeglądarka wysyła żądanie HTTP do endpointów zdefiniowanych w `views.py`.
2. Widoki pobierają/zapisują dane w bazie przez query do modeli SQLAlchemy (do jednej z tabel: `User`, `Airport`, `Location`, `Flight`, `Booking`).
3. Dane są filtrowane i przygotowywane do wyświetlenia
4. Flask renderuje szablony i zwraca odpowiedź HTML.

## Przykład - rezerwacja lotu
1. Użytkownik wchodzi na stronę główną
2. Użytkownik wybiera w wyszukiwarce filtry, po jakich chce szukać lotu (miejsce wylotu, miejsce przylotu, data)
3. Użytkownik wyszukuje loty przez `/search`.
4. Backend filtruje rekordy w tabeli/modelu `Flight` i renderuje `results.html` z listą wyników.
5. Przyciski Zarezerwuj są widoczne tylko dla zalogowanych (sprawdzany user_id w sesji).
6. Kliknięcie Zarezerwuj wysyła `POST /reserve/<flight_id>`:
   - pobierany jest lot `Flight` po `flight_id`,
   - tworzony jest rekord `Booking` (powiązany z użytkownikiem i lotem),
   - dane są zapisywane w bazie.
7. Użytkownik jest przekierowany na `/rezerwacje`, gdzie endpoint renderuje `reservations.html` z listą rezerwacji
