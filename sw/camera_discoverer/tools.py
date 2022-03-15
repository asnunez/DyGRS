import json
from typing import Dict

import requests


def bool2str(b: bool) -> str:
    return "True" if b else "False"


def create_json(host: str, alias: str, state: bool) -> Dict:
    camera_info = {
        "camera":
            {
                "alias": alias,
                "url": f"rtsp://{host}",
                "active": bool2str(state)
            }
    }

    return camera_info


def send_discover(host: str, alias: str, state: bool) -> None:
    camera_info = create_json(host, alias, state)
    requests.post("http://10.109.76.15:5000/register-camera", json=camera_info)
    print(camera_info)
