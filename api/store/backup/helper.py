# coding=utf-8
import logging

import os
import json
from flask import current_app as app
from model import db
from model.session import Session as SessionModel
from module.file import save_file_to_dir
from module.dir import clear_dir

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def resolve_session_data(session, request):
    if len(request.files) == 0:
        raise ValueError('Không có file nào!')
    uploaded_files = list(request.files.values())
    filenames = [file.filename for file in uploaded_files]
    save_path = SessionModel._data_path(session.creator_id, session.name)
    try:
        for file in uploaded_files:
            save_file_to_dir(save_path, file)
    except Exception as err:
        _logger.error(err)
        raise err
    # filter session.json file
    session_json = [f for f in filenames if f == 'session.json']
    if len(session_json):
        update_session_info(session, os.path.join(save_path, session_json[0]))
    # filter video

    # clear files in session folder
    clear_dir(
        path=os.path.join(*[app.config['ROOT_DIR'], app.config['DATA_DIR'], save_path]),
        except_filename=filenames)

def update_session_info(session, session_json):
    file_path = os.path.join(
        *[app.config['ROOT_DIR'], app.config['DATA_DIR'], session_json])
    with open(file_path) as f:
        session_info = json.load(f)
    try:
        session.num_video = session_info['num_video']
        session.man_ef = session_info['man_ef']
        session.auto_ef = session_info['auto_ef']
        db.session.commit()
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        raise err

def update_video_info(session, video, annotation):
    pass
