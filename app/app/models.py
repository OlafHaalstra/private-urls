# models.py

from datetime import datetime

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    suffix = db.Column(db.String(6), unique=True)
    views = db.relationship('View', backref=db.backref('views', lazy=True))


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    link = db.relationship('Link', backref=db.backref('links', lazy=True))
