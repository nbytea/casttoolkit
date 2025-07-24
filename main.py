#!/usr/bin/env python3
import os
import json
from datetime import datetime
from discover import discover_devices, select_devices
from recon import recon_device
from control import control_device
from utils import setup_logger, generate_summary

def main():
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Discover devices
    devices = discover_devices()
    if not devices:
        print("[-] No devices found.")
        return

    # Select single or multiple devices
    selection = select_devices(devices)
    selected_devices = []

    if selection == "all":
        print("[*] Reconning all devices...")
        for dev in devices:
            logger = setup_logger(dev.cast_info.friendly_name, timestamp)
            recon_device(dev, timestamp, logger)
            selected_devices.append((dev, logger))
        print("[*] Recon complete. Use single selection for control.")
    else:
        dev = devices[int(selection)]
        logger = setup_logger(dev.cast_info.friendly_name, timestamp)
        recon_device(dev, timestamp, logger)
        selected_devices.append((dev, logger))
        control_device(selected_devices)  # control single OR multiple

    # Generate summaries
    print("[*] Generating summaries...")
    for _, logger in selected_devices:
        log_path = logger.handlers[0].baseFilename
        generate_summary(log_path)

if __name__ == "__main__":
    main()

