# coding=utf-8

import logging
from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class Annotation(Basemodel):
    __tablename__ = 'annotation'
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    json = db.Column(db.Text, nullable=False)
    data_path = db.Column(db.String(255), nullable=False)
    video = db.relationship('Video', backref='annotations')

    def __init__(self, video_id, json, data_path):
        self.video_id = video_id
        self.json = json
        self.data_path = data_path
