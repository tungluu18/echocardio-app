# coding=utf-8

import logging
from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

class Session(Basemodel):
    __tablename__ = 'session'
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    patient_age = db.Column(db.Integer, nullable=True)
    data_path = db.Column(db.String(255), nullable=False)
    videos = db.relationship("Video", back_populates="session")

    def __init__(self, creator_id, patient_name, patient_age, data_path):
        self.creator_id = creator_id
        self.patient_age = patient_age
        self.patient_name = patient_name
        self.data_path = data_path
