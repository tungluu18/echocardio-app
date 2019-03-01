# coding=utf-8

import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

db = SQLAlchemy()

def init_app(app):
    """
    :param app: Flask app
    :return:
    """
    db.app = app
    db.init_app(app)
    migrate = Migrate(app=app, db=db)
    _logger.info('Start app with database: %s' %
                 (app.config['SQLALCHEMY_DATABASE_URI']))


from model.basemodel import Basemodel
from model.user import User
from model.session import Session
from model.video import Video
from model.annotation import Annotation
