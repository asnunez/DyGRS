import logging
from typing import cast

from zeroconf import ServiceStateChange, Zeroconf

from .models import Camera
from .reporter import send_discover


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    logging.info(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            addresses = ["%s:%d" % (address, cast(int, info.port)) for address in info.parsed_scoped_addresses()]
            camera = Camera(host=addresses[0], alias=info.name, active=True)
            send_discover(camera)

    elif state_change is ServiceStateChange.Removed:
        camera = Camera(host="", alias=name, active=False)
        send_discover(camera)
