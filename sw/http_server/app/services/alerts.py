import json
from typing import Dict

from sw.http_server.app import db
from sw.http_server.app.models import Alert, Camera


def save_alert(data: Dict):
    """
    {"alert":
        {"type": "no mask",
         "camera":"camera-1",
         "timestamp": 12345678}
     }
    """

    alert_data = data["alert"]

    camera_id = Camera.query.filter_by(alias=alert_data["camera"]).first().id

    new_alert = Alert(type=alert_data["type"], camera=camera_id, timestamp=alert_data["timestamp"], resolved=False)

    db.session.add(new_alert)
    db.session.commit()


def resolve_alert(data: Dict):
    """{"id": 12}"""
    alert = Alert.query.filter_by(id=data["id"]).resolved = True
    db.session.commit()


def unresolved_alerts() -> str:
    """Returns a list of unresolved alerts."""
    alerts = Alert.query.filter_by(resolved=False).all()

    alerts_dict = {"alerts": []}

    for a in alerts:
        camera_alias = Camera.query.filter_by(id=a.camera).first().alias
        [alerts_dict["alerts"].append({"id": a.id, "type": a.type, "camera": camera_alias, "timestamp": a.timestamp})
         for a in alerts]

    return json.dumps(alerts_dict)
