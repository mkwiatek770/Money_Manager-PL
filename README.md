# Money_Manager-PL-
Currently only in polish language / Obecnie tylko w jezyku poslkim

## O czym jest aplikacja ? 
Aplikacja jest menedżerem wydatków i finansów: 
* możemy kontrolować stan naszego konnta 
* sprawdzać historię naszych wydatków
* dodawać / usuwać wydatki
* generować raporty pdf naszych wydatków 
* generować raporty XLS naszych wydatków 
* szukać konkretnych wydatków po nazwie w wyszukiwarce

## Instalacja
* zklonuj repozytorium na GitHubie 
* zainstaluj psql jeśli nie masz apt-get install psql 
* zrób backup bazy danych wchodząc w katalog database i wpisując: psql -U postgres -f active.sql -h localhost active_db
* stwórz wirtualne środowisko virtualenv -p python3 venv
* zainstaluj wymagane paczki: pip install -r requirements.txt
* Wejdź do katalogu gdzie znajduje się plik run.py i wpisz python3 run.py 
* w przeglądarce wpisz adres: http://localhost:5000/

## Kontrybuowanie 
Pull requesty są mile widziane :)

## Author 
* Michał Kwiatek 
* kontakt: michalkwiatek8@o2.pl

## Licencja 
[MIT](https://choosealicense.com/licenses/mit/)

