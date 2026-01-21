Strona usługi wyszukującej nadchodzące loty samolotowe

Aby zobaczyć stronę należy uruchomić plik Aplikacja.py, a następnie w przeglądarce wpisać url http://127.0.0.1:5000/

Uruchomienie pliku api_request.py powoduje pobranie z API FlightLabs nadchodzących lotów (z zakresu do 8 godzin od godziny uruchomienia) - dane zapisywane w db/base_data/api_data

Domyślnie można się zalogować na następujące konta:
  - user1@gmail.com ; hasło: 123
  - user2@gmail.com ; hasło: 123
  - admin@gmail.com ; hasło: admin123  <- konto admina ze specjalnym panelem do edytowania bazy danych

Wymagane biblioteki (do zainstalowania poprzez pip):
- flask
- flask-sqlalchemy
- ftfy
- pydantic
- bcrypt

[TODO]
- plik .db przenieść do folderu db
- ujednolicić nazwy plików (angielski)
- w README opisać prepływ danych (gdzie użytkownik klika, co jest wysyłane do backendu)
- komentarze w kodzie (dodać/usunąć?)
