# coding=utf-8
import logging

import os

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

# DIRECTORY
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = 'data'
SESSION_DIR = 'sessions'
UPLOAD_DIR = 'data/tmp'

# DATABASE
DB_NAME = os.environ.get('ECHO_DB_NAME')
DB_USER = os.environ.get('ECHO_DB_USER')
DB_PWD = os.environ.get('ECHO_DB_PWD')
DB_HOST = os.environ.get('ECHO_DB_HOST')
DB_PORT = os.environ.get('ECHO_DB_PORT')

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % \
        (DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
