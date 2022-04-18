import flask
from flask import render_template

from . import app
from .services import cameras, alerts
from .services.cameras import frames_generator


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title='Home Page')


@app.route("/get-active-cameras", methods=["GET"])
def get_active_cameras():
    """Provides a JSON file containing information about active cameras with
     the following format:
      {"cameras":[
        {"id": 12,
         "alias": "camera-1",
         "url":"rtsp://camera-1 ..."
         },
          ...
          ]
      }"""
    data = cameras.active_cameras()

    return flask.jsonify(data)


@app.route("/register-camera", methods=["POST"])
def register_camera():
    """Consumes a JSON file with the following format:
     {"camera":
        {"alias": "camera-1",
        "url":"rtsp://camera-1 ...",
        "active": "True"
        }
     }
     and registers or updates this information into the database"""

    data = flask.request.get_json()
    cameras.register_camera(data)

    return flask.Response(status=200)


@app.route("/save-alert", methods=["POST"])
def save_alert():
    """Consumes a JSON file with the following format:
     {"alert":
        {"type": "no mask",
         "camera":"camera-1",
         "timestamp": 12345678}
     }
     and saves the alert with the status True"""
    data = flask.request.get_json()
    alerts.save_alert(data)

    return flask.Response(status=200)


@app.route("/resolve-alert", methods=["POST"])
def resolve_alert():
    """Consumes a JSON file with the following format:
     {"id": 12}
     and toggle the status of the alert to False"""
    data = flask.request.get_json()
    alerts.resolve_alert(data)

    return flask.Response(status=200)


@app.route("/get-unresolved-alerts", methods=["GET"])
def get_unresolved_alerts():
    """Provides a JSON file with the current active alerts. Following the format:
    { "alerts": [
            {
            "id": 12,
            "type": "No mask detected"
            "camera": "camera-1",
            "timestamp": 123124324
            },
                       {
            "id": 13,
            "type": "No mask detected"
            "camera": "camera-1",
            "timestamp": 123124322312
            },
            ...
        ]
    }
    """
    data = alerts.unresolved_alerts()

    return flask.jsonify(data)


@app.route("/camera-streaming", methods=["POST"])
def camera_streaming():
    """Consumes a JSON file with the following format:
    {"alias": "camera-1"}
    and returns a video streaming"""

    cam_url = cameras.get_url_from_alias(flask.request.get_json()["alias"])

    return flask.Response(frames_generator(cam_url), mimetype='multipart/x-mixed-replace; boundary=frame')
