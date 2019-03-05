# coding=utf8

import logging
import os
import config
import shutil

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def get_session_folder_path(session_id):
    session_path = os.path.join(
        config.DATA_DIR, config.SESSION_DIR, str(session_id))
    return session_path


def create_session_folder(session_id):
    path = os.path.join(config.ROOT_DIR, get_session_folder_path(session_id))
    try:
        os.makedirs(path)
    except OSError:
        _logger.error('Creation of session folder %s failed' % path)
    else:
        _logger.info('Successfully created session folder %s' % path)


def remove_session_folder(session_id):
    path = os.path.join(config.ROOT_DIR, get_session_folder_path(session_id))
    try:
        shutil.rmtree(path)
    except OSError:
        _logger.error('Removal of session folder %s failed' % path)
    else:
        _logger.info('Successfully removed session folder %s' % path)
