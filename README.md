Aby odpalić strone należy wykonać flask --app Aplikacja.py run

W static/Styles będą style css strony

W templates są wszystkie pliki html, proponuję rozbić je na layout gdzie będą elementy znajdujące się na każdej podstronie (tło itp.), natomiast w poszczególnych plikach będą elementy każdej podstrony tak jak jest to w przykładowym indexie

Wszystko inne (pliki py i baza itp.) chyba w ogólnym folderze

Jakbyście mieli jakiekolwiek pytania piszcie na grupie na mess - Kuba

[30.12.2025] Zrobiłem pierwszą wersję bazy danych, myślę że można już coś z tym kombinować. Dane o lotniskach i lotach są w folderze db/base_data . Jeśli chcecie pobrać nowe dane, najpierw uruchomcie plik api_request.py, a potem główną aplikację (napiszcie na messengerze po kod do api). Przez najbliższe dni dodam lokacje, które będą celem podróży (może też więcej lotnisk). W razię wątpliwości śmiało piszcie pytania. (P.S. - do zobaczenia wartości w pliku .db polecam DB Browser for SQLite) -- Maciek

[12.01.2026] Dodałem frontend i dodałem troche rzeczy do views.py aby przetestować czy wszystko działa. Trzeba jeszcze dodać funkcjonalności do pola wyszukiwania aby działało i aby pokazywało prawidłowe dane z bazy. Jeśli zauważycie, że coś nie działa, trzeba będzie coś zmienić w wyglądzie albo dodać jakieś podstrony to można pisać. - Paweł