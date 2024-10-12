# Gauge

## External dependencies

### Activate venv

* MacOS

`source env/bin/activate`

* Windows CMD :

`env/Scrpits/activate`

* Windows Powershell :

`.\env\Scripts\Activate.ps1`

* Winddows Git Bash:

`source env\Scripts\activate`

### Download dependencies

`pip install -r requirements.txt`

### Requirement.txt update

If you add dependencies to the venv project, don't forget to run :
`pip freeze > requirements.txt` to keep this file up to date.

### Deactivate venv

`deactivate` 

## Run projet

The project can be run using `python3 main.py`.

Then the front is available at your local machine IP `{IP}:8000/static/index.html`.

Data are served at your local machine IP `{IP}:8000/api/data`

## Packaging du projet 

- MacOS : `pyinstaller --add-data "config.yaml:." --add-data "www:www" --add-data "vendors:vendors" main.py`

- Windows : `pyinstaller --add-data "config.yaml;." --add-data "www;www" --add-data "vendors;vendors" main.py`
