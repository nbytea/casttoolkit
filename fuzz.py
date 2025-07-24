import requests
import time
from urllib.parse import urljoin

COMMON_PATHS = [
    "setup/eureka_info", "setup/debug", "setup/status",
    "setup/reboot", "setup/factory_reset", "setup/test_ota",
    "setup/diag", "setup/config", "setup/wifi_scan"
]

COMMON_APPS = [
    "Netflix", "YouTube", "DisneyPlus", "PrimeVideo",
    "Hulu", "Spotify", "Plex", "HBO", "Backdrop"
]

PAYLOADS = [
    "../../../../etc/passwd", "%0a", "%00", "<script>alert(1)</script>",
    "AAAA" * 1000
]

def fuzz_device(device, timestamp, logger, recon_summary=None):
    base_url = f"http://{device['host']}:8008/"
    results = {
        "device": device["name"],
        "timestamp": timestamp,
        "ip": device["host"],
        "fuzz_results": []
    }

    # Passive fuzz
    for path in COMMON_PATHS:
        _fuzz_path(urljoin(base_url, path), path, logger, results)

    # Active fuzz (param injection)
    for path in COMMON_PATHS:
        for payload in PAYLOADS:
            _fuzz_path(urljoin(base_url, f"{path}?test={payload}"), f"{path}?payload", logger, results)

    # App fuzz (GET/POST/DELETE)
    apps_to_test = set(COMMON_APPS)
    if recon_summary and "apps" in recon_summary:
        apps_to_test |= set(recon_summary["apps"].keys())

    for app in apps_to_test:
        app_url = urljoin(base_url, f"apps/{app}")
        _fuzz_path(app_url, f"apps/{app} GET", logger, results, method="GET")
        for payload in PAYLOADS:
            _fuzz_path(app_url, f"apps/{app} POST {payload}", logger, results, method="POST", data={"v": payload})
        _fuzz_path(app_url, f"apps/{app} DELETE", logger, results, method="DELETE")

    # TODO: WebSocket fuzz (port 8009)
    # Could use websockets lib to send malformed Cast v2 frames

    return results

def _fuzz_path(url, label, logger, results, method="GET", data=None):
    try:
        start = time.time()
        if method == "GET":
            r = requests.get(url, timeout=3)
        elif method == "POST":
            r = requests.post(url, data=data, timeout=3)
        elif method == "DELETE":
            r = requests.delete(url, timeout=3)
        else:
            return
        duration = round(time.time() - start, 3)

        entry = {
            "endpoint": label,
            "method": method,
            "status": r.status_code,
            "length": len(r.text),
            "time": duration
        }
        results["fuzz_results"].append(entry)

        if r.status_code not in [404, 405] or duration > 1.0:
            logger.warning(f"[Fuzz] {label} -> {r.status_code}, {duration}s")

    except Exception as e:
        logger.error(f"[Fuzz] {label} error: {e}")

