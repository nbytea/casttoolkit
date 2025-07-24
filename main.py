from discovery import discover_devices
from logger_setup import setup_logger
from utils import write_summary

def main():
    devices = discover_devices()
    if not devices:
        print("[!] No devices found.")
        return

    print("[*] Devices discovered:")
    for i, d in enumerate(devices):
        print(f"[{i}] {d['name']} ({d['host']}) - {d['model']}")

    choice = input("[*] Enter device number or 'all' for multi-device: ")
    targets = devices if choice.lower() == "all" else [devices[int(choice)]]

    for dev in targets:
        logger, ts = setup_logger(dev['name'])
        logger.info(f"Selected device: {dev['name']} ({dev['host']})")

        summary = {
            "device": dev['name'],
            "timestamp": ts,
            "model": dev.get("model"),
            "ip": dev['host'],
            "build_version": dev.get("build_version"),
            "apps": {}
        }
        write_summary(dev['name'], ts, summary)

        # TODO: integrate control, recon, fuzz menus
        print(f"[+] Logger and summary initialized for {dev['name']}")

if __name__ == "__main__":
    main()

