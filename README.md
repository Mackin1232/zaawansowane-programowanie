UWAGA!!! Do pobierania lotow nie używać api AviationStack, podobno wykradają pieniądze;
Ja zrobię na podstawie AeroDataBox (dostępne za darmo na RapidAPI)

Progres:
  - zrobiono prostą bazę z tabelą Users
  - wstawiono przykładowe dane do bazy
  - po wejściu na 127.0.0.1:5000/users zwracani są wszyscy userzy
  - po wejściu na 127.0.0.1:5000/users/1 zwracany jest user o id = 1 (działa też dla innych id)
  - dodano klasę location, uporządkowano kod
