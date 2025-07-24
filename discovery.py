import pychromecast
import requests

def discover_devices():
    chromecasts, _ = pychromecast.get_chromecasts()
    devices = []
    for cast in chromecasts:
        info = {
            "name": cast.cast_info.friendly_name,
            "host": cast.cast_info.host,
            "model": cast.cast_info.model_name,
            "manufacturer": cast.cast_info.manufacturer
        }

        try:
            r = requests.get(f"http://{info['host']}:8008/setup/eureka_info", timeout=5)
            if r.status_code == 200:
                info.update(r.json())
        except Exception:
            pass
        devices.append(info)
    return devices

