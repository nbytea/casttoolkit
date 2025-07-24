import requests
from utils import write_summary
from urllib.parse import urljoin

KNOWN_APPS = [
    "Netflix", "YouTube", "DisneyPlus", "PrimeVideo",
    "Hulu", "Spotify", "Plex", "HBO", "Backdrop"
]

SETUP_ENDPOINTS = [
    "eureka_info", "reboot", "factory_reset", "test_ota",
    "diag", "config", "wifi_scan"
]

def recon_device(device, timestamp, logger):
    """
    Perform recon on one device:
      - Check installed apps
      - Check setup endpoints
    Returns summary dict (updated)
    """
    host = device['host']
    base_url = f"http://{host}:8008/"
    summary = {
        "device": device['name'],
        "timestamp": timestamp,
        "ip": host,
        "model": device.get("model"),
        "apps": {},
        "setup_endpoints": {}
    }

    for app in KNOWN_APPS:
        url = urljoin(base_url, f"apps/{app}")
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                summary["apps"][app] = "installed"
                logger.info(f"[+] App {app} installed (200)")
            elif r.status_code == 404:
                summary["apps"][app] = "not_found"
                logger.debug(f"[-] App {app} not found (404)")
            else:
                summary["apps"][app] = f"status_{r.status_code}"
                logger.warning(f"[?] App {app} unknown status ({r.status_code})")
        except Exception as e:
            summary["apps"][app] = "error"
            logger.error(f"[!] Error checking {app}: {e}")

    for ep in SETUP_ENDPOINTS:
        ep_results = {}
        for method in ["GET", "POST"]:
            url = urljoin(base_url, f"setup/{ep}")
            try:
                if method == "GET":
                    r = requests.get(url, timeout=2)
                else:
                    r = requests.post(url, timeout=2)
                ep_results[method] = r.status_code
                logger.info(f"[SETUP] {method} {ep} -> {r.status_code}")
            except Exception as e:
                ep_results[method] = "error"
                logger.error(f"[!] Error {method} {ep}: {e}")
        summary["setup_endpoints"][ep] = ep_results

    return summary

