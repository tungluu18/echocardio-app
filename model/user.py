# coding=utf-8

import logging
from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

class User(Basemodel):
    __tablename__ = 'user'

    username = db.Column(db.String(255), primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), primary_key=True, unique=True)
    phone = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    organization = db.Column(db.String(255), nullable=True)
    job = db.Column(db.String(255), nullable=True)
    sessions = db.relationship("Session", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
