# coding=utf-8
import logging

import os
import json
from flask import current_app as app
from model import db
from model.session import Session as SessionModel
from model.video import Video as VideoModel
from module.file import save_file_to_dir, sol_ext
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
        # update session.json file
        if 'session.json' in filenames:
            update_session_info(session)

        video_files = [f for f in filenames if VideoModel._is_video(f)]
        video_names = [sol_ext(f)[0] for f in video_files]
        json_files = [f for f in filenames if sol_ext(f)[1] == 'json']

        for name in video_names:
            VideoModel._create(session_id=session.id, name=name)

        for filename in json_files:
            name, ext = sol_ext(filename)
            if name in video_names:
                update_video_annotation(
                    session=session,
                    video_name=name,
                    annotation_file=filename
                )

    except Exception as err:
        _logger.error(err)
        raise err


def update_video_annotation(session, video_name, annotation_file):
    try:
        save_path = SessionModel._data_path(
            creator_id=session.creator_id,
            session_name=session.name
        )
        file_path = os.path.join(
            *[app.config['ROOT_DIR'], app.config['DATA_DIR'],
              save_path, annotation_file])
        with open(file_path) as f:
            annotation = json.load(f)
        annotation_dumped = json.dumps(annotation)
        VideoModel._update(
            session_id=session.id,
            name=video_name,
            annotation=annotation_dumped
        )
        return video_name
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        raise err


def update_session_info(session):
    session_save_path = SessionModel._data_path(
        session.creator_id, session.name)
    file_path = os.path.join(
        *[app.config['ROOT_DIR'], app.config['DATA_DIR'],
          session_save_path, 'session.json'])
    try:
        with open(file_path) as f:
            session_info = json.load(f)
    except Exception as err:
        raise ValueError('File session không đúng định dạng')

    try:
        session.num_video = session_info.get('num_video', None)
        session.man_ef = session_info.get('man_ef', None)
        session.auto_ef = session_info.get('auto_ef', None)
        db.session.commit()
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        raise err


def clean_backup_data(session, filenames, video_files):
    # clean old files
    save_path = SessionModel._data_path(
        creator_id=session.creator_id,
        session_name=session.name
    )
    clean_dir(
        path=os.path.join(*[app.config['ROOT_DIR'],
                            app.config['DATA_DIR'],
                            save_path]),
        except_filename=filenames
    )
    # clean old video in db
    videos_by_session = VideoModel.query.filter_by(session_id=session.id)
    for video in videos_by_session:
        if video.name not in video_files:
            db.session.delete(video)
    db.session.commit()
