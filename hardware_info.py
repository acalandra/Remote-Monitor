import os
import clr
import psutil

def initialize_hardware_monitor(dll):
    """
    Initialize OpenHardwareMonitor or other hardware monitoring libraries by passing the DLL filename.
    """
    try:
        clr.AddReference(dll)

        from OpenHardwareMonitor import Hardware

        handle = Hardware.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.RAMEnabled = True
        handle.GPUEnabled = True
        handle.HDDEnabled = True
        handle.FanControllerEnabled = True
        handle.Open()

        return handle
    except Exception as e:
        print(f"Error initializing {dll}: {e}")
        return None

def parse_sensor_to_dict(sensor):
    """
    Convert sensor data to a dictionary format.
    """
    return {
        "name": sensor.Name,
        "value": str(sensor.Value) if sensor.Value is not None else None,
        "type": str(sensor.SensorType)
    }
  
def hardware_to_dict(hardware):
    """
    Convert the hardware data to a dictionary, including CPU, GPU, RAM, storage, etc.
    """
    hardware_data = []

    for i in hardware.Hardware:
        i.Update()
    
        hardware_info = {
            "label": i.Name,
            "type": type_for_hardware(str(i)),
            "sensors": [parse_sensor_to_dict(sensor) for sensor in i.Sensors],
            "subhardware": []
        }

        for j in i.SubHardware:
            j.Update()
            subhardware_info = {
                "name": j.Name,
                "sensors": [parse_sensor_to_dict(subsensor) for subsensor in j.Sensors]
            }
            hardware_info["subhardware"].append(subhardware_info)

        hardware_data.append(hardware_info)

    disk = psutil.disk_usage('/')
    storage_data = {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

    result = {
        "cpu": next(x for x in hardware_data if x["type"] == "cpu"),
        "gpu": next(x for x in hardware_data if x["type"] == "gpu"),
        "storage": storage_data,
        "ram": next(x for x in hardware_data if x["type"] == "ram"),
        "motherboard": next(x for x in hardware_data if x["type"] == "motherboard"),
    }

    return result

def get_storage_info():
    """
    Retrieve storage information using psutil.
    """
    try:
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    except Exception as e:
        print(f"Error retrieving storage information: {e}")
        return {}

def type_for_hardware(hardware_name):
    """
    Return the type of hardware based on the name.
    """
    if "CPU" in hardware_name:
        return "cpu"
    elif "GPU" in hardware_name:
        return "gpu"
    elif "HDD" in hardware_name:
        return "storage"
    elif "RAM" in hardware_name:
        return "ram"
    elif "Mainboard" in hardware_name:
        return "motherboard"
    else:
        return hardware_name
