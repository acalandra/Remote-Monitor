from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import clr
import uvicorn
import socket
import yaml
import qrcode
import hardware_info
import multiprocessing

app = FastAPI()

def get_base_path():
    """Helper function to get the base path for accessing resources."""
    return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")

def load_config():
    """Load configuration from config.yaml file."""
    config_path = os.path.join(get_base_path(), 'config.yaml')
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

config = load_config()
port = config.get("port", 8000)
web_folder = config.get("web_folder", "/static")
home_file = config.get("home_file", "index.html")
dll_path = os.path.join(get_base_path(), 'vendors', 'Python.Runtime.dll')

def get_local_ip():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def mount_subdirectories(app, base_path):
    """Dynamically mount subdirectories in the www folder."""
    app.mount("/static", StaticFiles(directory=base_path), name="static")
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            mount_path = f"/{entry}"
            app.mount(mount_path, StaticFiles(directory=full_path), name=entry)
            print(f"Mounted {full_path} at {mount_path}")

www_path = os.path.join(get_base_path(), 'www')
mount_subdirectories(app, www_path)

@app.on_event("startup")
async def startup_event():
    try:
        dll_filename = os.path.join(get_base_path(), 'vendors/OpenHardwareMonitorLib.dll')
        app.state.HardwareHandle = hardware_info.initialize_hardware_monitor(dll_filename)
    except Exception as e:
        print(f"Error initializing OpenHardwareMonitor: {e}")

@app.get("/api/data")
async def get_all_data():
    hardware_data = hardware_info.hardware_to_dict(app.state.HardwareHandle)
    return hardware_data

def allow_external_requests(origin):
    """Allow external requests from specified origins."""
    if origin:
        if not any(isinstance(m, CORSMiddleware) for m in app.user_middleware):
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[origin],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

if __name__ == "__main__":
    try:
        clr.AddReference(dll_path)
        
        external_origin = config.get("external_origin")
        if external_origin:
            allow_external_requests(external_origin)

        multiprocessing.freeze_support()

        local_ip = get_local_ip()
        print(f"Starting UI server on {local_ip}:{port}{web_folder}/{home_file}")
        print(f"Starting API server on {local_ip}:{port}/api/data")

        qr = qrcode.QRCode()
        qr.add_data(f"http://{local_ip}:{port}{web_folder}/{home_file}")
        qr.print_ascii()

        uvicorn.run(app, host="0.0.0.0", port=port, reload=False, workers=1)

    except Exception as e:
        print(f"An error occurred: {e}")

    # Add this line to prevent window closure
    input("Press Enter to exit...")     