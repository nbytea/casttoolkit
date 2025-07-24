def recon_device(device, ts, logger):
    device.wait()
    status = device.status
    info = {
        "device": device.cast_info.friendly_name,
        "host": device.cast_info.host,
        "model": device.cast_info.model_name,
        "volume": status.volume_level,
        "muted": status.volume_muted,
        "app_id": device.app_id,
        "app_name": device.app_display_name,
    }

    logger.info({
        "event": "recon",
        "timestamp": ts,
        **info
    })

    print(f"[+] Recon for {info['device']} ({info['host']}):")
    print(f"    Volume: {info['volume']}, Muted: {info['muted']}")
    print(f"    Current App: {info['app_name']} ({info['app_id']})")

