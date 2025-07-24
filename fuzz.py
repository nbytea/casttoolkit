import ssl, socket, requests

def fuzz_cast_v2(host, logger):
    print(f"[*] Fuzzing Cast v2 on {host}:8009...")
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        sock = socket.create_connection((host, 8009), timeout=5)
        ssl_sock = context.wrap_socket(sock, server_hostname=host)

        payloads = [
            b"\x00\x00\x00\x10FAKEPROTOBUF",
            b"\x00\x00\x00\x05\xff\xff\xff\xff\xff",
            b"\x00\x00\x00\x20" + b"A"*32
        ]

        for p in payloads:
            print(f"[*] Sending {len(p)} bytes...")
            try:
                ssl_sock.send(p)
                resp = ssl_sock.recv(64)
                print(f"[+] Response: {resp}")
                logger.info({"event": "fuzz_cast_v2", "payload_len": len(p), "response": str(resp)})
            except Exception as e:
                print(f"[!] Error: {e}")
                logger.info({"event": "fuzz_cast_v2_error", "payload_len": len(p), "error": str(e)})

        ssl_sock.close()
    except Exception as e:
        print(f"[!] Cast v2 fuzz failed: {e}")
        logger.info({"event": "fuzz_cast_v2_failed", "error": str(e)})

def fuzz_dial_endpoints(host, logger):
    print(f"[*] Fuzzing DIAL endpoints on {host}:8008...")
    endpoints = [
        "setup/eureka_info",
        "setup/reboot",
        "setup/factory_reset",
        "setup/diag",
        "setup/test_ota",
        "apps/Netflix",
        "apps/YouTube",
        "apps/Backdrop"
    ]

    for ep in endpoints:
        url = f"http://{host}:8008/{ep}"
        try:
            r = requests.get(url, timeout=3)
            logger.info({"event": "fuzz_dial_get", "endpoint": ep, "status": r.status_code})
            print(f"[GET] {ep} -> {r.status_code}")

            r = requests.post(url, timeout=3)
            logger.info({"event": "fuzz_dial_post", "endpoint": ep, "status": r.status_code})
            print(f"[POST] {ep} -> {r.status_code}")
        except Exception as e:
            logger.info({"event": "fuzz_dial_error", "endpoint": ep, "error": str(e)})
            print(f"[!] Error fuzzing {ep}: {e}")

