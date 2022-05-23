import logging

import requests

from .config import config
from .models import Camera

back_up = []


def send_discover(camera: Camera) -> None:
    endpoint = f"http://{config.HTTP_SERVER_IP}:{config.HTTP_SERVER_PORT}/register-camera"

    logging.info(f"Sending camera info to sever {camera}")

    try:

        resp = requests.post(endpoint, json=camera.to_dict())

        if back_up:
            [requests.post(endpoint, json=camera.to_dict()) for c in back_up]

        logging.info(f"Sending success: {resp.status_code}")
    except (ConnectionError, OSError):
        logging.info(f"Sending failed")
        back_up.append(camera)
