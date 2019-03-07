# coding=utf-8
import logging

import os
import json
from flask import current_app as app
from model import db
from model.session import Session as SessionModel
from model.video import Video as VideoModel
from module.file import save_file_to_dir
from module.dir import clean_dir

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
    # filter video and annotation
    video_annotation = [
        (x, y)
        for x in filenames
        for y in filenames
        if x < y and x.split('.')[0] == y.split('.')[0]]
    video_files = [update_video_annotation(session, save_path, _)
                  for _ in video_annotation]

    # clean files in session folder
    clean_backup_data(session, save_path, filenames, video_files)

def update_video_annotation(session, save_path, files):
    if files[0][-4::] == 'json':
        annotation_file, video_file = files
    else:
        video_file, annotation_file = files
    video_name = annotation_file[:-5]
    # create video on db if not existed
    video = VideoModel.query.filter_by(name=video_name).first()
    if not video:
        video = VideoModel(name=video_name, session_id=session.id)
        db.session.add(video)
    # load annotation file
    try:
        file_path = os.path.join(
            *[app.config['ROOT_DIR'], app.config['DATA_DIR'], save_path, annotation_file])
        with open(file_path) as f:
            annotation = json.load(f)
        annotation_dumped = json.dumps(annotation)
        video.annotation = annotation_dumped
        db.session.commit()
        return video_name
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        raise err

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

def clean_backup_data(session, save_path, filenames, video_files):
    # clean old files
    clean_dir(
        path=os.path.join(*[app.config['ROOT_DIR'], app.config['DATA_DIR'], save_path]),
        except_filename=filenames)
    # clean old video in db
    videos_by_session = VideoModel.query.filter_by(session_id=session.id)
    print('cleaning', video_files)
    for video in videos_by_session:
        print(video.name)
        if video.name not in video_files:
            db.session.delete(video)
    db.session.commit()
