# coding=utf-8

import logging
import os
from flask import current_app as app
# import config
import shutil

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

def create_folder(path):
    path = os.path.join(
        *[app.config['ROOT_DIR'], app.config['DATA_DIR'], path])
    try:
        os.makedirs(path)
    except OSError:
        _logger.error('Creation of session folder %s failed' % path)
    else:
        _logger.info('Successfully created session folder %s' % path)

def clean_dir(path, except_filename):
    try:
        for f in os.listdir(path):
            if f not in except_filename:
                os.remove(os.path.join(path, f))
    except Exception as err:
        _logger.error(err)

def remove_folder(path):
    path = os.path.join(
        *[app.config['ROOT_DIR'], app.config['DATA_DIR'], path])
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except OSError:
        _logger.error('Removal of session folder %s failed' % path)
    else:
        _logger.info('Successfully removed session folder %s' % path)

