# Remote monitor

## Purpose

My goal with this project was to propose an interface to easily monitor PC data in real time.
Launching the application couldn't be simpler. Go to the [releases](https://github.com/acalandra/Remote-Monitor/releases) page and download the archive.
Extract it to your machine and run the main.exe file. When it launches, the program will probably ask you for access to your local network : this is normal, as it's how the data will be sent to another device.

When the program starts, it displays a QR Code. You can scan it with your phone or tablet to open the tracking page. If you prefer, you can use the url that also appears when the program starts up to paste it into your browser's url bar. 

Technically, by executing the main.exe file, the program starts a server to do two distinct things:
- expose an api method on `{your-ip}/api/data` which lists everything the program has managed to read from your machine.
- serve a web page on `{your-ip}/static/index.html` which will read this data and display it graphically.

As everything runs from your local IP, your device must be on the same network as the computer running the program. **DON'T FORGET TO TURN ON WIFI ON YOUR PHONE**

If you don't like the interface I've suggested, feel free to design your own! Simply replace the files in the www directory with your own.

As long as your site uses the `/api/data` route, you'll be able to display data from your machine.

You can also modify the program's access point by editing the `config.yaml` file in the project root.
- `port` : is the port number on which the application is served
- `web_folder` : is the name of the route on which the application is served
- `home_file` : is the name of the file to be served by the server
- `external_origin` : is useful if you wish to access `/api/data` from an address other than that of the server. This avoids CORS problems.

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

The project can be run using `python main.py`.

Then the front is available at your local machine IP `{IP}:{port}/static/index.html`.

Data are served at your local machine IP `{IP}:{port}/api/data`

## Packaging du projet 

- MacOS : `pyinstaller --clean --add-data "config.yaml:." --add-data "www:www" --add-data "vendors:vendors" main.py`

- Windows : `pyinstaller --clean --add-data "config.yaml;." --add-data "www;www" --add-data "vendors;vendors" main.py`
