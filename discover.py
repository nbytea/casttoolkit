import pychromecast

def discover_devices():
    chromecasts, browser = pychromecast.get_chromecasts()
    if not chromecasts:
        return []
    print("[*] Devices discovered:")
    for i, cc in enumerate(chromecasts):
        print(f"[{i}] {cc.cast_info.friendly_name} ({cc.cast_info.host}) - {cc.cast_info.model_name}")
    return chromecasts

def select_devices(devices):
    choice = input("[*] Enter device number or 'all': ").strip().lower()
    if choice == "all":
        return "all"
    return choice

