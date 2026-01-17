Aby odpalić strone należy wykonać flask --app Aplikacja.py run

W static/Styles będą style css strony

W templates są wszystkie pliki html, proponuję rozbić je na layout gdzie będą elementy znajdujące się na każdej podstronie (tło itp.), natomiast w poszczególnych plikach będą elementy każdej podstrony tak jak jest to w przykładowym indexie

Wszystko inne (pliki py i baza itp.) chyba w ogólnym folderze

Jakbyście mieli jakiekolwiek pytania piszcie na grupie na mess - Kuba

[30.12.2025] Zrobiłem pierwszą wersję bazy danych, myślę że można już coś z tym kombinować. Dane o lotniskach i lotach są w folderze db/base_data . Jeśli chcecie pobrać nowe dane, najpierw uruchomcie plik api_request.py, a potem główną aplikację (napiszcie na messengerze po kod do api). Przez najbliższe dni dodam lokacje, które będą celem podróży (może też więcej lotnisk). W razię wątpliwości śmiało piszcie pytania. (P.S. - do zobaczenia wartości w pliku .db polecam DB Browser for SQLite) -- Maciek

[12.01.2026] Dodałem frontend i dodałem troche rzeczy do views.py aby przetestować czy wszystko działa. Trzeba jeszcze dodać funkcjonalności do pola wyszukiwania aby działało i aby pokazywało prawidłowe dane z bazy. Jeśli zauważycie, że coś nie działa, trzeba będzie coś zmienić w wyglądzie albo dodać jakieś podstrony to można pisać. - Paweł

[13.01.2026] W branchu backend-kuba będe pracował nad wyszukiwaniem, filtrowaniem i testowaniem i dopracowaniem ostatecznej wersji strony. - Kuba

[13.01.2026] Dodałem wyszukiwanie, filtrowanie i kilka małych poprawek. Nie jestem pewny czy w zakładce Kraje ma być dokładna kopia wyszukiwania z indexu, więc na razie jej nie tykałem, jutro możemy się dogadać jaki jest z tym plan. Jutro jeszcze potestuje stronę i w razie czego naniosę poprawki. W razie pytań piszcie. - Kuba

[16.01.2026] Naprawiłem wyszukiwanie w podstronie kraje. Jak by coś jeszcze nie działało to piszcie. - Kuba

[17.01.2026] Dodałem cenę lotów do tabeli Locations (jako cena zwykłego lotu z Polski do podanego lotniska). Większy sens miałoby dodanie tego do Flights, ale tak było łatwiej - mniej rekordów do edytowania. [UWAGA: trzeba również dodać pole do wpisywania ceny w panelu admina] Usunąłem także duplikaty z tabeli Flights. Później jeszcze spróbuję dodać więcej rekordów do Locations - Maciek
