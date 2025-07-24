from recon import discover_devices, recon_device
from control import set_volume, mute, stop_app, launch_app, play_media
from fuzz import fuzz_device
from utils import setup_logger, write_summary, apply_control

def main():
    devices = discover_devices()
    if not devices:
        print("[!] No Chromecast devices found.")
        return

    print("[*] Devices discovered:")
    for i, d in enumerate(devices):
        print(f"[{i}] {d['name']} ({d['host']}) - {d['model']}")

    choice = input("[*] Enter device number or 'all': ").strip().lower()
    targets = devices if choice == "all" else [devices[int(choice)]]

    # Recon + Auto fuzz
    for dev in targets:
        logger, ts = setup_logger(dev["name"])
        summary = recon_device(dev, ts, logger)
        write_summary(dev["name"], ts, summary)

        fuzz_results = fuzz_device(dev, ts, logger, recon_summary=summary)
        write_summary(dev["name"], ts, fuzz_results)

        print(f"[+] Recon + fuzz complete for {dev['name']}")

    # Control menu
    control_menu(targets)

def control_menu(targets):
    while True:
        print("""
Control Options:
[1] Set Volume
[2] Mute/Unmute
[3] Stop Current App
[4] Launch App
[5] Play Media URL
[6] Manual Fuzz
[7] Exit
""")
        choice = input("> ").strip()

        logger, ts = setup_logger(targets[0]["name"])  # unified log per session

        if choice == "1":
            percent = int(input("Set volume % (0-100): "))
            apply_control(targets, set_volume, percent, logger)
        elif choice == "2":
            state = input("Mute? (y/n): ").lower() == "y"
            apply_control(targets, mute, state, logger)
        elif choice == "3":
            apply_control(targets, stop_app, logger)
        elif choice == "4":
            app_id = input("App ID to launch: ")
            apply_control(targets, launch_app, app_id, logger)
        elif choice == "5":
            url = input("Media URL: ")
            apply_control(targets, play_media, url, "video/mp4", logger)
        elif choice == "6":
            for dev in targets:
                fuzz_results = fuzz_device(dev, ts, logger)
                write_summary(dev["name"], ts, fuzz_results)
                print(f"[+] Manual fuzz complete for {dev['name']}")
        elif choice == "7":
            break

if __name__ == "__main__":
    main()

