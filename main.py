from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import uvicorn
import socket
import io
import yaml
import qrcode
import hardware_info
import multiprocessing

app = FastAPI()

def get_config_file():
    if hasattr(sys, '_MEIPASS'):
        # Lors de l'exécution du programme packagé, les fichiers sont extraits ici
        base_path = sys._MEIPASS
    else:
        # En développement, utilise le chemin relatif classique
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'config.yaml')


with open(get_config_file(), 'r') as config_file:
    config = yaml.safe_load(config_file.read())

port = config.get("port", 8000)
web_folder = config.get("web_folder", "/static")
home_file = config.get("home_file","index.html")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_www_path():
    if hasattr(sys, '_MEIPASS'):
        # Lors de l'exécution packagée, www est dans ce chemin temporaire
        base_path = sys._MEIPASS
    else:
        # En développement, utilise le chemin relatif classique
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, 'www')

# Fonction pour monter dynamiquement tous les sous-répertoires de www
def mount_subdirectories(app, base_path):
    app.mount("/static", StaticFiles(directory=base_path), name="static")
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            mount_path = f"/{entry}"
            app.mount(mount_path, StaticFiles(directory=full_path), name=entry)
            print(f"Mounted {full_path} at {mount_path}")

www_path = get_www_path()
# Monter les sous-répertoires de www dynamiquement
mount_subdirectories(app, www_path)

# Exemple d'endpoint API
@app.get("/api/data")
async def get_all_data():
    return {
        "cpu": hardware_info.get_cpu_infos(),
        "memory": hardware_info.get_memory_info(),
        "disk": hardware_info.get_disk_info(),
        "gpu": hardware_info.get_gpu_info()
    }


def allow_external_requests(origin):
    if origin:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[origin], 
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


if __name__ == "__main__":
    external_origin = config.get("external_origin")
    if external_origin:
        allow_external_requests(external_origin)

    multiprocessing.freeze_support()

    local_ip = get_local_ip()

    print(f"Starting server on {local_ip}:{port}")

    qr = qrcode.QRCode()
    qr.add_data(f"http://{local_ip}:{port}{web_folder}/{home_file}")
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())

    #uvicorn.run("main:app", host=local_ip, port=port, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False, workers=1)