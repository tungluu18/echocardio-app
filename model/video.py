# coding=utf-8

import logging
from model import db, Basemodel
from util import video_exts

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class Video(Basemodel):
    __tablename__ = 'video'
    name = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    auto_ef = db.Column(db.Float(), nullable=True)
    man_ef = db.Column(db.Float(), nullable=True)
    annotation = db.Column(db.Text(collation='utf8_general_ci'), nullable=True)
    session = db.relationship('Session', backref='videos')

    def __init__(self, name, session_id):
        self.name = name
        self.session_id = session_id

    @staticmethod
    def _is_video(filename):
        i = filename.rfind('.')
        return filename[i+1:] in video_exts

    @staticmethod
    def _get_video_name(filename):
        i = filename.rfind('.')
        if filename[i+1:] not in video_exts:
            return None
        return filename[:i]

    @staticmethod
    def _create(session_id, name, annotation=None):
        video = Video.query.filter_by(session_id=session_id, name=name).first()
        if video:
            return video
        video = Video(name, session_id)
        if annotation:
            video.annotation = annotation
        db.session.add(video)
        db.session.commit()
        return video

    @staticmethod
    def _update(session_id, name, annotation):
        video = Video.query.filter_by(
            session_id=session_id,
            name=name
        ).first()
        video.annotation = annotation
        db.session.commit()
        return video
