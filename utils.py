import logging
import json
import os
from datetime import datetime

def setup_logger(device_name):
    safe_name = device_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = f"logs/{safe_name}-{timestamp}.log"
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(f"{safe_name}-{timestamp}")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)

    return logger, timestamp

def write_summary(device_name, timestamp, data):
    safe_name = device_name.replace(" ", "_")
    os.makedirs("summaries", exist_ok=True)
    file_path = f"summaries/{safe_name}-{timestamp}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    return file_path

def apply_control(devices, func, *args):
    """
    Automatically handles single vs multiple devices
    """
    if len(devices) == 1:
        func(devices[0], *args)
    else:
        for dev in devices:
            func(dev, *args)

