# coding=utf-8

import logging
import os

from model import db, Basemodel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class Session(Basemodel):
    __tablename__ = 'session'

    creator_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(length=255, collation='utf8_general_ci'), primary_key=True, nullable=False)
    patient_name = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)
    num_video = db.Column(db.Integer(), nullable=True)
    auto_ef = db.Column(db.Float(), nullable=True)
    man_ef = db.Column(db.Float(), nullable=True)
    user = db.relationship('User', backref='sessions')

    def __init__(self, creator_id, name):
        self.creator_id = creator_id
        self.name = name
        patient_name, patient_age = name.split('_')[:2]
        self.patient_age = int(patient_age)
        self.patient_name = patient_name

    @staticmethod
    def _data_path(creator_id, session_name):
        return os.path.join(*['backup', str(creator_id), session_name])
