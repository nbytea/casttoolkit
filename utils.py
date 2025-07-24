import logging
import os
import json
from datetime import datetime

def setup_logger(device_name, ts):
    safe_name = device_name.replace(" ", "_")
    log_path = f"logs/{safe_name}_{ts}.log"

    logger = logging.getLogger(safe_name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_path)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    return logger

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "time": datetime.now().isoformat(),
            **record.msg
        })

def generate_summary(log_path):
    events = []
    with open(log_path, "r") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except:
                continue

    if not events:
        return

    first = events[0]
    device_name = first.get("device", "unknown").replace(" ", "_")
    summary_file = os.path.splitext(log_path)[0] + "_summary.json"

    summary = {
        "device": device_name,
        "host": first.get("host", ""),
        "model": first.get("model", ""),
        "summary_time": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        "events": events
    }

    with open(summary_file, "w") as out:
        json.dump(summary, out, indent=2)

    print(f"[+] Summary written to {summary_file}")

