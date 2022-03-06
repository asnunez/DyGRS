import flask
from flask import Response, request, render_template

streamer = flask.Blueprint("streamer", __name__)


@streamer.route("/")
def render_index():
    return render_template("index.html")
