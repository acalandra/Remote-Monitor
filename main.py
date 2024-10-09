from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import socket
import io
import yaml
import qrcode
import hardware_info

app = FastAPI()

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

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

# Monter le répertoire "www" comme un serveur de fichiers statiques
app.mount("/_nuxt", StaticFiles(directory="www/_nuxt"), name="_nuxt")
app.mount(web_folder, StaticFiles(directory="www"), name="static")

# Exemple d'endpoint API
@app.get("/api/data")
async def get_all_data():
    return {
        "cpu": hardware_info.get_cpu_info(),
        "memory": hardware_info.get_memory_info(),
        "disk": hardware_info.get_disk_info()
    }

if __name__ == "__main__":
    local_ip = get_local_ip()

    print(f"Starting server on {local_ip}:{port}")

    qr = qrcode.QRCode()
    qr.add_data(f"http://{local_ip}:{port}{web_folder}/{home_file}")
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())

    uvicorn.run("main:app", host=local_ip, port=port, reload=True)