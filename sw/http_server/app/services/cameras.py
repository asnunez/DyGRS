import json
from typing import Dict

import cv2

from sw.http_server.app import db
from sw.http_server.app.models import Camera


def active_cameras() -> Dict:
    cameras = Camera.query.filter_by(active=True).all()

    ret = {"cameras": [{"id": c.id, "alias": c.alias, "url": c.url} for c in cameras]}

    return ret


def register_camera(data: Dict) -> None:
    """
    {"camera":
        {"alias": "camera-1",
        "url":"rtsp://camera-1 ...",
        "active": "True"
        }
     }
    """
    data_dict = data

    camera_dict = data_dict["camera"]

    camera = Camera.query.filter_by(alias=camera_dict["alias"]).first()

    if not camera:
        new_camera = Camera(alias=camera_dict["alias"], url=camera_dict["url"], active=camera_dict["active"] == "True")
        db.session.add(new_camera)
        db.session.commit()
        return

    camera.url = camera_dict["url"]
    camera.active = camera_dict["active"] == "True"
    db.session.commit()


def frames_generator(rtsp_url: str):
    camera = cv2.VideoCapture(rtsp_url)

    while True:
        success, frame = camera.read()
        if not success:
            return
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


def get_url_from_alias(camera_alias: str):
    camera = Camera.query.filter_by(alias=camera_alias).first()

    return camera.url
