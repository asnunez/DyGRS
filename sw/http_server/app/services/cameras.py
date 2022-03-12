import json
from typing import Dict

from sw.http_server.app import db
from sw.http_server.app.models import Camera


def active_cameras() -> str:
    cameras = Camera.query.filter_by(active=True).all()

    ret = {"cameras": [{"id": c.id, "alias": c.alias, "url": c.url} for c in cameras]}

    return json.dumps(ret)


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
