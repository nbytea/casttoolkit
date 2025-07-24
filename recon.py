import pychromecast
from utils import write_summary

def discover_devices():
    """Return list of Chromecast objects"""
    chromecasts, browser = pychromecast.get_chromecasts()
    if not chromecasts:
        print("[-] No Chromecast devices found.")
    else:
        for i, cc in enumerate(chromecasts):
            print(f"[{i}] {cc.cast_info.friendly_name} ({cc.cast_info.host}) - {cc.cast_info.model_name}")
    return chromecasts

def recon_device(cast, timestamp, logger):
    """Dump device status + installed app info"""
    cast.wait()
    status = cast.status

    summary = {
        "device": cast.cast_info.friendly_name,
        "host": cast.cast_info.host,
        "model": cast.cast_info.model_name,
        "uuid": str(cast.cast_info.uuid),
        "status": {
            "active_input": status.is_active_input,
            "standby": status.is_stand_by,
            "volume": status.volume_level,
            "muted": status.volume_muted,
            "app": status.display_name,
            "app_id": status.app_id
        }
    }
    logger.info(f"Recon summary: {summary}")
    write_summary(cast.cast_info.friendly_name, timestamp, summary)
    return summary

