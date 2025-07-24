def set_volume(device, percent, logger):
    cc = _get_cc(device)
    cc.set_volume(percent / 100)
    logger.info(f"Set volume {percent}%")

def mute(device, state, logger):
    cc = _get_cc(device)
    cc.set_volume_muted(state)
    logger.info(f"Mute set to {state}")

def stop_app(device, logger):
    cc = _get_cc(device)
    cc.quit_app()
    logger.info("Stopped current app")

def launch_app(device, app_id, logger):
    cc = _get_cc(device)
    cc.start_app(app_id)
    logger.info(f"Launched app {app_id}")

def play_media(device, url, content_type, logger):
    cc = _get_cc(device)
    mc = cc.media_controller
    mc.play_media(url, content_type)
    mc.block_until_active()
    mc.play()
    logger.info(f"Started media playback: {url}")

def _get_cc(device):
    import pychromecast
    cc = pychromecast.Chromecast(device["host"])
    cc.wait()
    return cc

