from typing import List

from sw.services_provider import db


class Alert(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    type: str = db.Column(db.String(256))
    timestamp: int = db.Column(db.Integer)
    resolved: bool = db.Column(db.Boolean)
    camera: int = db.Column(db.Integer, db.ForeignKey('camera.id'))


class Camera(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    alias: str = db.Column(db.String(256))
    active: bool = db.Column(db.Boolean)
    alerts: List[Alert] = db.relationship('Alert')
