import pychromecast

def discover_devices():
    chromecasts, browser = pychromecast.get_chromecasts()
    return [{
        "name": c.cast_info.friendly_name,
        "host": c.cast_info.host,
        "model": c.cast_info.model_name,
        "uuid": str(c.cast_info.uuid),
    } for c in chromecasts]

def recon_device(device, timestamp, logger):
    """
    Collects device info, status, and installed apps.
    """
    cc = pychromecast.Chromecast(device["host"])
    cc.wait()

    status = cc.status
    apps = {}
    if status.app_id:
        apps[status.app_display_name] = {"app_id": status.app_id, "state": "running"}
    else:
        apps["None"] = {"app_id": None, "state": "stopped"}

    summary = {
        "device": device["name"],
        "ip": device["host"],
        "model": device["model"],
        "uuid": device["uuid"],
        "status": {
            "active_input": status.is_active_input,
            "standby": status.is_stand_by,
            "volume": status.volume_level,
            "muted": status.volume_muted
        },
        "apps": apps
    }

    logger.info(f"Recon summary: {summary}")
    return summary

