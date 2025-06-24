# Flask CRUD App

### Uruchomienie lokalnie

1. Stwórz wirtualne środowisko i zainstaluj wymagania:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Skonfiguruj bazę danych w `config.py`

3. Uruchom migracje:

```
flask db init
flask db migrate -m "initial"
flask db upgrade
```

4. Uruchom serwer:

```
python run.py
```
