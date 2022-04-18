import time
from typing import List
import json
import requests
import logging

from .config import config
from .models import Camera


def notify_alert(camera_alias) -> None:
    alert = {
        "alert":
            {
                "type": "no mask",
                "camera": f"{camera_alias}",
                "timestamp": f"{time.time()}"
            }
    }

    endpoint = f"http://{config.HTTP_SERVER_IP}:{config.HTTP_SERVER_PORT}/save-alert"

    try:
        requests.post(endpoint, json=alert)
    except (OSError, ConnectionError) as e:
        logging.error(e)


def get_active_cameras() -> List:
    endpoint = f"http://{config.HTTP_SERVER_IP}:{config.HTTP_SERVER_PORT}/get-active-cameras"

    ret = []
    try:
        response = requests.get(endpoint)
    except (OSError, ConnectionError) as e:
        logging.error(e)
        return ret

    for entity in response.json().get("cameras"):
        cam = Camera(alias=entity["alias"], host=entity["url"], active=True)
        ret.append(cam)

    return ret