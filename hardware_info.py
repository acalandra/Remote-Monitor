import platform
import psutil
from cpuinfo import get_cpu_info
import gpustat

current_platform = platform.system()

def get_cpu_infos():
    info = get_cpu_info()
    
    cpu_temp = -1
    if (current_platform == "Windows"):
        cpu_temp = psutil.sensors_temperatures()
    
    cpu_fan = -1
    if (current_platform == "Windows"):
        cpu_fan = psutil.sensors_fans()

    return {
        "cpu_name": info['brand_raw'],
        "cpu_frequency": info['hz_actual'][0],
        "cpu_usage": psutil.cpu_percent(),
        "cpu_temp": cpu_temp,
        "cpu_fan": cpu_fan
    }

def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percent": memory.percent
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

def get_gpu_info():
    if (current_platform == "Windows"):
        gpu_stats = gpustat.GPUStatCollection.new_query()
        for gpu in gpu_stats.gpus:
            print(f"GPU {gpu.index}: {gpu.name}, Utilization: {gpu.utilization}%")
    return {}