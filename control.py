from fuzz import fuzz_cast_v2, fuzz_dial_endpoints

def show_menu():
    print("""
[1] Show Status
[2] Launch Netflix
[3] Stop Current App
[4] Volume Up
[5] Volume Down
[6] Mute/Unmute
[7] Cast Custom Media (MP4 URL)
[9] Set Volume (0-100%)
[F] Fuzz Mode (Cast v2 + DIAL)
[Q] Quit
""")

def control_device(devices):
    # Handle multi or single device control
    single_device = len(devices) == 1

    while True:
        show_menu()
        choice = input("Select action: ").strip().upper()

        if choice == "Q":
            break

        # Iterate over selected devices
        for cast, logger in devices:
            cast.wait()

            if choice == "1":
                print(f"[{cast.cast_info.friendly_name}] Status: {cast.status}")
                logger.info({"event": "status", "data": str(cast.status)})

            elif choice == "2":
                print(f"[{cast.cast_info.friendly_name}] Launching Netflix...")
                cast.start_app("Netflix")
                logger.info({"event": "launch_netflix"})

            elif choice == "3":
                print(f"[{cast.cast_info.friendly_name}] Stopping app...")
                cast.quit_app()
                logger.info({"event": "stop_app"})

            elif choice == "4":
                cast.volume_up()
                logger.info({"event": "volume_up", "level": cast.status.volume_level})

            elif choice == "5":
                cast.volume_down()
                logger.info({"event": "volume_down", "level": cast.status.volume_level})

            elif choice == "6":
                cast.set_volume_muted(not cast.status.volume_muted)
                logger.info({"event": "mute_toggle", "muted": cast.status.volume_muted})

            elif choice == "7":
                url = input("Enter MP4 URL: ")
                mc = cast.media_controller
                mc.play_media(url, "video/mp4")
                mc.block_until_active()
                mc.play()
                logger.info({"event": "cast_media", "url": url})

            elif choice == "9":
                level = float(input("Enter volume (0-100): ")) / 100
                cast.set_volume(level)
                logger.info({"event": "set_volume", "level": level})

            elif choice == "F":
                host = cast.cast_info.host
                fuzz_cast_v2(host, logger)
                fuzz_dial_endpoints(host, logger)

        # If multi-device, loop continues; single exits on Q


