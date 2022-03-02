import json

import flask
from flask import Response, request

from Software.services_provider.notifier.notifier import Notifier

notifier = flask.Blueprint("notifier", __name__)
nf = Notifier()


@notifier.route("/save-alert", methods=["POST"])
def save_alert():
    data = request.get_json()

    if data:
        data = json.dumps(data)
        notify = f"data: {data}\nevent: alert\n\n"
        nf.publish(notify)

    return Response(status=200)


@notifier.route("/get-alerts", methods=["GET"])
def get_alerts():
    return Response(nf.subscribe(), content_type='text/event-stream')
