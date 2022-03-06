import argparse
import logging
import tools
from time import sleep
from typing import cast
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes


def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    print(f"Service {name} of type {service_type} state changed: {state_change}")
    count = 0

    if state_change is ServiceStateChange.Added:
        count = count + 1
        info = zeroconf.get_service_info(service_type, name)

        if info:
            addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            print("  Addresses: %s" % ", ".join(addresses))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print(f"    {key}: {value}")
            else:
                print("  No properties")
        else:
            print(" No info")
        print('\n')
        tools.send_discover(addresses[0], True, count)

    elif state_change is ServiceStateChange.Removed:
        count = count - 1
        print(f"Service {name} of type {service_type} state changed: {state_change}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--find', action='store_true', help='Browse all available services')
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--v6', action='store_true')
    version_group.add_argument('--v6-only', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    if args.v6:
        ip_version = IPVersion.All
    elif args.v6_only:
        ip_version = IPVersion.V6Only
    else:
        ip_version = IPVersion.V4Only

    zeroconf = Zeroconf(ip_version=ip_version)

    services = ["_http._tcp.local.", "_rstp._tcp.local."]
    if args.find:
        services = list(ZeroconfServiceTypes.find(zc=zeroconf))

    print("\nBrowsing %d service(s), press Ctrl-C to exit...\n" % len(services))
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
