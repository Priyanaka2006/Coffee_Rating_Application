# Good Cup Club

A small coffee tasting board built with Flask and SQLite. The coffee list is served by a JSON API, and every vote is committed to the local database.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. The SQLite database is created at `instance/coffee-ratings.sqlite` the first time the app starts.

## Run tests

```powershell
python -m unittest discover -s tests
```

## API

- `GET /api/coffees` returns the coffee list and current vote totals.
- `POST /api/coffees/<id>/vote` adds one vote and returns the updated total.
