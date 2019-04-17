# coding=utf-8
import logging
import os
from datetime import datetime

from model import db, Basemodel
from config import HOST_URL, ROOT_DIR, DATA_DIR

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
        patient_name, patient_age, created_at = name.split('_', 2)
        self.patient_age = int(patient_age)
        self.patient_name = patient_name
        self.created_at = datetime.strptime(created_at, '%Y_%m_%d_%H_%M_%S')

    @staticmethod
    def _data_path(creator_id, session_name):
        return os.path.join(*['backup', str(creator_id), session_name])

    def get_all_files(self):
        session_path = self._data_path(self.creator_id, self.name)
        result = []
        for file in os.listdir(os.path.join(*[ROOT_DIR, DATA_DIR, session_path])):
            file_download_link = os.path.join(*[HOST_URL, DATA_DIR, session_path, file])
            result += [file_download_link]
        return result
