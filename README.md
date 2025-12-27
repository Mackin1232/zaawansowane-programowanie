UWAGA!!! Do pobierania lotow nie używać api AviationStack, podobno wykradają pieniądze;
Na razie szukam, jakiego API użyć, na razie ok wyglądają AeroDataBox, FlightLabs, AirLabs, FlightAPI.io, Aviyair

Progres:
  - zrobiono prostą bazę z tabelą Users
  - wstawiono przykładowe dane do bazy
  - po wejściu na 127.0.0.1:5000/users zwracani są wszyscy userzy
  - po wejściu na 127.0.0.1:5000/users/1 zwracany jest user o id = 1 (działa też dla innych id)
  - dodano klasę location, uporządkowano kod
  - pobrano dane lotów z api

TODO: uzupełnić bazę danych o loty, lotniska, lokacje
