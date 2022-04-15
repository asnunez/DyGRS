import logging
from typing import cast

from zeroconf import ServiceStateChange, Zeroconf

from .reporter import send_discover
from .models import Camera


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    logging.info(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added or state_change is ServiceStateChange.Removed:
        info = zeroconf.get_service_info(service_type, name)

        if info:
            addresses = ["%s:%d" % (address, cast(int, info.port)) for address in info.parsed_scoped_addresses()]
            if state_change is ServiceStateChange.Added:
                camera = Camera(host=addresses[0], alias=info.name, active=True)
            else:
                camera = Camera(host=addresses[0], alias=info.name, active=False)

            send_discover(camera)
