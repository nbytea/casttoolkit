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
[8] Quit
""")

def control_device(cast, logger):
    while True:
        show_menu()
        choice = input("Select action: ")

        if choice == "1":
            print(f"Status: {cast.status}")
            print(f"Current app: {cast.app_display_name} ({cast.app_id})")

        elif choice == "2":
            print("[*] Launching Netflix...")
            cast.start_app("Netflix")

        elif choice == "3":
            print("[*] Stopping current app...")
            cast.quit_app()

        elif choice == "4":
            cast.volume_up()
            print(f"Volume: {cast.status.volume_level}")

        elif choice == "5":
            cast.volume_down()
            print(f"Volume: {cast.status.volume_level}")

        elif choice == "6":
            cast.set_volume_muted(not cast.status.volume_muted)
            print(f"Muted: {cast.status.volume_muted}")

        elif choice == "7":
            url = input("Enter media URL: ")
            mc = cast.media_controller
            mc.play_media(url, "video/mp4")
            mc.block_until_active()
            mc.play()
            print("[*] Media casting started.")

        elif choice == "9":
            level = float(input("Enter volume (0-100): ")) / 100
            cast.set_volume(level)
            print(f"Volume set to {level*100:.0f}%")

        elif choice.upper() == "F":
            from fuzz import fuzz_cast_v2, fuzz_dial_endpoints
            fuzz_cast_v2(cast.cast_info.host, logger)
            fuzz_dial_endpoints(cast.cast_info.host, logger)

        elif choice == "8":
            break
        else:
            print("Invalid option.")

