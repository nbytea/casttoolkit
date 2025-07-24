import logging, os
from datetime import datetime
from urllib.parse import quote_plus

def setup_logger(device_name: str):
    os.makedirs("logs", exist_ok=True)
    safe_name = quote_plus(device_name.lower().replace(" ", "-"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/{safe_name}_{timestamp}.log"

    logger = logging.getLogger(device_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename)
    fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(fh)
    return logger

