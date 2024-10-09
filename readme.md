# Gauge

## venv lifecycle

`source env/bin/activate` to activae venv

`deactivate` to deactivate it


## Run projet

The project can be run using `python3 main.py`.

Then the front is available at your local machine IP `{IP}:8000/static/index.html`.

Data are served at your local machine IP `{IP}:8000/api/data`

## Packaging du projet 
`pyinstaller --add-data "config.yaml:." --add-data "www:www" main.py`

