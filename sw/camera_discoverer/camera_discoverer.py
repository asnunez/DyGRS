import logging
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf, IPVersion, ZeroconfServiceTypes
from src.listener import on_service_state_change


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(message)s")
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)

    services = ["_rtsp._tcp.local."]

    logging.info("Browsing %d service(s), press Ctrl-C to exit...\n" % len(services))
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    browser.join()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()


if __name__ == '__main__':
    main()
