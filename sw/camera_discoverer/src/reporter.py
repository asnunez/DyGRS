import requests

from .config import config
from .models import Camera


def send_discover(camera: Camera) -> None:
    endpoint = f"http://{config.HTTP_SERVER_IP}:{config.HTTP_SERVER_PORT}/register-camera"

    try:
        requests.post(endpoint, json=camera.to_dict())
    except (ConnectionError, OSError):
        pass
