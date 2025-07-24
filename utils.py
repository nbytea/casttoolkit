import logging, os, json, datetime

def setup_logger(name):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = name.replace(" ", "_")
    logdir = "logs"
    os.makedirs(logdir, exist_ok=True)
    logfile = os.path.join(logdir, f"{safe_name}-{ts}.log")

    logger = logging.getLogger(safe_name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logfile)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(fh)

    return logger, ts

def write_summary(name, timestamp, data):
    safe_name = name.replace(" ", "_")
    os.makedirs("summaries", exist_ok=True)
    path = os.path.join("summaries", f"{safe_name}-{timestamp}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

