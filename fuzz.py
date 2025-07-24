import ssl, socket, requests

def fuzz_cast_v2(host, logger):
    logger.info("[*] Fuzzing Cast v2 (8009)...")
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
            logger.info(f"Sending {len(p)} bytes to Cast v2")
            try:
                ssl_sock.send(p)
                resp = ssl_sock.recv(64)
                logger.info(f"Response: {resp}")
            except Exception as e:
                logger.warning(f"No response / error: {e}")

        ssl_sock.close()

    except Exception as e:
        logger.error(f"Cast v2 fuzz failed: {e}")

def fuzz_dial_endpoints(host, logger):
    logger.info("[*] Fuzzing DIAL endpoints (8008)...")
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
    results = {}
    for ep in endpoints:
        url = f"http://{host}:8008/{ep}"
        try:
            r_get = requests.get(url, timeout=3)
            r_post = requests.post(url, timeout=3)
            results[ep] = {"GET": r_get.status_code, "POST": r_post.status_code}
            logger.info(f"[GET] {ep} -> {r_get.status_code}, [POST] -> {r_post.status_code}")
        except Exception as e:
            logger.warning(f"Error fuzzing {ep}: {e}")
    return results

