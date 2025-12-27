Używam api AirLabs - jeśli chcecie klucz to napiszcie na messengerze

Sugeruję żeby dane z API pobrać raz (albo raz na jakiś czas - 1 na dzień, na 2 dni?), zapisać do bazy danych (albo jako plik .json) i żeby aplikacja pobierała dane z bazy/pliku. Wtedy zużyjemy mniej requestów

Progres:
  - zrobiono prostą bazę z tabelą Users
  - wstawiono przykładowe dane do bazy
  - po wejściu na 127.0.0.1:5000/users zwracani są wszyscy userzy
  - po wejściu na 127.0.0.1:5000/users/1 zwracany jest user o id = 1 (działa też dla innych id)
  - dodano klasę location, uporządkowano kod
  - pobrano dane lotów z api (są w folderze api_data jako pliki .json)

TODO: uzupełnić bazę danych o loty, lotniska, lokacje
