# Climate Adaptations

A Django web app to store and filter climate adaptation solutions by
climate impact, type and sector. Data is collected from the EU Climate-ADAPT
platform via an automation script that returns a normalised CSV file, that can be uplaoded into the database in the app.

## stack
Python / Django, SQLite, plain HTML templates

## workflow
1. Run the script to generate the CSV
2. Upload that CSV in the app under `/upload/`

## CSV columns
| Field                | Description                                   |
|----------------------|-----------------------------------------------|
| name                 | Name of the adaptation option                 |
| climate_impact       | Primary climate impact (fixed choices)        |
| type                 | Nature-based / structural / organisational    |
| sector               | Affected sector (fixed choices)               |


## Setup
```bash
git clone https://github.com/genrihleifried/climate-adaptations.git
cd climate-adaptations
python -m venv venv
source venv/bin/activate (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open the sites:
- `/` — list with filters
- `/upload/` — CSV import(also possible with the button in '/' )
- `/admin/` — djangos database managment-site

## Collect data
```bash
python import_climate_adapt.py
```
->
Generates `adaptations_import.csv` upload it under `/upload/`.


## Tests
```bash
python manage.py test
```
