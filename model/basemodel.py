# coding=utf-8

import logging
from datetime import datetime
from model import db

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

class Basemodel(db.Model):
    """
        Abstract model chứa id, created_at, updated_at
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now())
