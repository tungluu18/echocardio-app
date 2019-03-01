# coding=utf-8

import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate(db=db)


def init_app(app):
    """
    :param app: Flask app
    :return:
    """
    db.app = app
    db.init_app(app)
    migrate.init_app(app)
    ma.init_app(app)

    _logger.info('Start app with database: %s' %
                 (app.config['SQLALCHEMY_DATABASE_URI']))


from model.basemodel import Basemodel
from model.annotation import Annotation
from model.video import Video
from model.session import Session
from model.user import User
