from recon import discover_devices, recon_device
from control import control_device
from utils import setup_logger

def main():
    chromecasts = discover_devices()
    if not chromecasts:
        return

    choice = input("[*] Enter device number or 'all': ").strip().lower()
    targets = chromecasts if choice == "all" else [chromecasts[int(choice)]]

    for cast in targets:
        logger, ts = setup_logger(cast.cast_info.friendly_name)
        recon_device(cast, ts, logger)

    # If only one device, auto control menu
    if len(targets) == 1:
        control_device(targets[0], logger)
    else:
        print("[*] Multiple devices recon complete. Use single selection for control.")

if __name__ == "__main__":
    main()

