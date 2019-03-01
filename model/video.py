# coding=utf-8

import logging
from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

class Video(Basemodel):
    __tablename__ = 'video'
    name = db.Column(db.String(255), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    data_path = db.Column(db.String(255), nullable=False)
    ef = db.Column(db.Float, nullable=True)
    gls = db.Column(db.Float, nullable=True)
    annotations = db.relationship("Annotation", back_populates="video")

    def __init__(self, name, session_id, data_path):
        self.name = name
        self.session_id = session_id
        self.data_path = data_path
