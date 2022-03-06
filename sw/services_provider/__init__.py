from wsgiref.simple_server import WSGIServer

from flask import Flask, Response, render_template, stream_with_context, request
from flask_sqlalchemy import SQLAlchemy

from notifier import notifier
from streamer import streamer

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    DB_NAME = "database.db"

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    app.register_blueprint(notifier, url_prefix="/")
    app.register_blueprint(streamer, urlprefix="/")

    return app
