from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sw.http_server.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from sw.http_server.app import models, routes
