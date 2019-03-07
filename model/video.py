# coding=utf-8

import logging
from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

class Video(Basemodel):
    __tablename__ = 'video'
    name = db.Column(db.String(255), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    auto_ef = db.Column(db.Float(), nullable=True)
    man_ef = db.Column(db.Float(), nullable=True)
    annotation = db.Column(db.Text(), nullable=True)
    session = db.relationship('Session', backref='videos')

    def __init__(self, name, session_id):
        self.name = name
        self.session_id = session_id
