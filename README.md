Strona usługi wyszukującej nadchodzące loty samolotowe

Aby zobaczyć stronę należy uruchomić plik Aplikacja.py, a następnie w przeglądarce wpisać url http://127.0.0.1:5000/

Osobno uruchamiany plik api_request.py powoduje pobranie z API FlightLabs nadchodzących lotów (z zakresu do 8 godzin od godziny uruchomienia) - dane zapisywane w db/base_data/api_data
(UWAGA: Do tego pliku potrzebny jest klucz darmowego tieru API FlightLabs, zamieszczony jako API_KEY w pliku api_key.py -> ten plik nie jest zamieszczony na GitHub'ie aby uniknąć wycieku klucza)

Domyślnie można się zalogować na następujące konta (nie wliczając kont utworzonych przy rejestracji):
    user1@gmail.com ; hasło: 123
    user2@gmail.com ; hasło: 123
    admin@gmail.com ; hasło: admin123 <- konto admina ze specjalnym panelem do edytowania bazy danych

[TODO]

    w README opisać prepływ danych (gdzie użytkownik klika, co jest wysyłane do backendu)
    dodać więcej lokacji (w domu zrobię -- Maciek)

Przepływ danych:
## Start aplikacji
- `aplication.py` inicjalizuje Flask, rejestruje blueprint `views`, ładuje konfigurację, inicjalizuje bazę SQLAlchemy i zasila bazę danymi przez load_data() w 'load_data.py' .

## Źródła danych
- Lotniska i lokalizacje są ładowane z plików CSV (`db/base_data/airports.csv`, `db/base_data/locations.csv`).
- Loty są ładowane z plików JSON w `db/base_data/api_data`. 
- Opcjonalnie: skrypt `api_request.py` pobiera rozkłady lotów z Airlabs API i zapisuje je do JSON, które później są importowane do bazy przy uruchomieniu aplikacji.   

## Przepływ żądania (UI renderowane po stronie serwera)
0. Jeśli jest to wymagane, sprawdzane są uprawnienia użytkownika (użytkownik przechowywany w sesji).
1. Przeglądarka wysyła żądanie HTTP do endpointów zdefiniowanych w `views.py`.
2. Widoki pobierają/zapisują dane w bazie przez query do modeli SQLAlchemy (`User`, `Airport`, `Location`, `Flight`, `Booking`).
3. Dane są filtrowane i przygotowywane do wyświetlenia
4. Flask renderuje szablony i zwraca odpowiedź HTML.

## Przykład: rezerwacja lotu
1. `POST /reserve/<flight_id>` wymaga zalogowanej sesji (`session['user_id']`).
2. Aplikacja pobiera `Flight` po ID, tworzy rekord `Booking`, commituje do bazy danych i przekierowuje na `/rezerwacje`.   
3. `/rezerwacje` pobiera rezerwacje użytkownika i ręcznie „łączy” je z lotami, żeby wyświetlić szczegóły na stronie.
