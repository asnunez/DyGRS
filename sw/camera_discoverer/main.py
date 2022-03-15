from time import sleep
from typing import cast

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf, IPVersion

import tools


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    print(f"Service {name} of type {service_type} state changed: {state_change}")
    count = 0

    if state_change is ServiceStateChange.Added:
        count = count + 1
        info = zeroconf.get_service_info(service_type, name)

        if info:
            addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            print(addresses)
            tools.send_discover(addresses[0], info.name, True)

        #

    elif state_change is ServiceStateChange.Removed:
        count = count - 1
        print(f"Service {name} of type {service_type} state changed: {state_change}")


if __name__ == '__main__':

    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)

    services = ["_companion-link._tcp.local."]

    print("\nBrowsing %d service(s), press Ctrl-C to exit...\n" % len(services))
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
