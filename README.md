Aby odpalić strone należy wykonać flask --app Aplikacja.py run

W static/Styles będą style css strony

W templates są wszystkie pliki html, proponuję rozbić je na layout gdzie będą elementy znajdujące się na każdej podstronie (tło itp.), natomiast w poszczególnych plikach będą elementy każdej podstrony tak jak jest to w przykładowym indexie

Wszystko inne (pliki py i baza itp.) chyba w ogólnym folderze

Jakbyście mieli jakiekolwiek pytania piszcie na grupie na mess - Kuba

[30.12.2025] Zrobiłem pierwszą wersję bazy danych, myślę że można już coś z tym kombinować. Dane o lotniskach i lotach są w folderze db/base_data . Jeśli chcecie nowe dane pobrać, najpierw uruchomcie plik api_request.py, a potem główną aplikację. W razię wątpliwości śmiało piszcie pytania. (P.S. - do zobaczenia wartości w pliku .db polecam DB Browser for SQLite) -- Maciek
