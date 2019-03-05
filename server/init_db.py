# coding=utf-8

import os
import logging
from model import db
from echo_cardio import app

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

# print
_logger.info('Creating database...')
db.create_all()
_logger.info('Database created!')
