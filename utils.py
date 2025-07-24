import os, json
from urllib.parse import quote_plus

def safe_device_name(name: str) -> str:
    return quote_plus(name.lower().replace(" ", "-"))

def write_summary(device_name: str, timestamp: str, data: dict):
    os.makedirs("summaries", exist_ok=True)
    filename = f"summaries/{safe_device_name(device_name)}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    return filename

