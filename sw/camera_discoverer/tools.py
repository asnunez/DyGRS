import json
import requests


def create_json(ip: str, state: bool, number: int) -> json:
    if state:
        camera_info = {
            "camera":
                {
                    "alias": "camera%d" % number,
                    "url": "rtsp://%s:554" % ip,
                    "active": "True"
                }
        }
    else:
        camera_info = {
            "camera":
                {
                    "alias": "camera%d" % number,
                    "url": "rtsp://%s:554" % ip,
                    "active": "False"
                }
        }

    return json.dumps(camera_info)


def send_discover(ip: str, state: bool, number: int) -> None:
    camera_info = create_json(ip, state, number)
    requests.post("http://10.254.14.117:80/register-camera", json=camera_info)
