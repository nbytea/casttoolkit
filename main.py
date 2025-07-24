from discovery import discover_devices
from logger_setup import setup_logger
from utils import write_summary

def main():
    devices = discover_devices()
    if not devices:
        print("[!] No devices found.")
        return

    print("[*] Devices found:")
    for i, d in enumerate(devices):
        print(f"[{i}] {d['name']} ({d['host']}) - {d['model']}")

    choice = input("[*] Enter device number or 'all' for multi-device: ")
    targets = devices if choice.lower() == "all" else [devices[int(choice)]]

    for dev in targets:
        logger, ts = setup_logger(dev['name'])
        logger.info(f"Recon started for {dev['name']}")

        summary = recon_device(dev, ts, logger)
        write_summary(dev['name'], ts, summary)

        logger.info(f"Recon completed for {dev['name']}")
        print(f"[+] Recon complete for {dev['name']} (summary saved)")

if __name__ == "__main__":
    main()

