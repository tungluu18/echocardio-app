# coding=utf-8
import logging
import os

from flask_restplus import Resource, fields
from flask import request

from api.store import api
from api.store.backup.helper import resolve_session_data, clean_backup_data
from api.api_base import BaseApi, HandledError

from model import db
from model.user import User as UserModel
from model.session import Session as SessionModel
from model.video import Video as VideoModel
from module.dir import create_folder, remove_folder
from module.file import sol_ext
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

filenames_fields = api.model('filenames_fields', {
    'filenames': fields.List(
        fields.String(),
        description='tên các file có trong thư mục của session')
})


@api.route('/backup/<int:creator_id>/<string:session_name>')
class Backup(Resource, BaseApi):
    @api.doc(description='Xóa session')
    def delete(self, creator_id, session_name):
        try:
            session = SessionModel.query.filter_by(
                creator_id=creator_id,
                name=session_name
            ).first()
            if not session:
                raise HandledError(error_code=404, message='Session không tồn tại')
            clean_backup_data(session, filenames=[], video_files=[])
            remove_folder(SessionModel._data_path(creator_id, session_name))
            db.session.delete(session)
            db.session.commit()
            return self.api_response()
        except HandledError as err:
            _logger.error(err)
            return self.api_response(handled_error=err)
        except Exception as err:
            _logger.error(err)
            return self.api_response(http_code=500)

    @api.doc(description='Backup data của một session')
    @api.expect(filenames_fields)
    def post(self, creator_id, session_name):
        print('Received backup request!')
        user = UserModel.query.filter_by(id=creator_id).first()
        if not user:
            return self.api_response(http_code=400,
                                     error='Người dùng không tồn tại!')
        try:
            assert user.is_active()
        except ValueError as err:
            _logger.error(err)
            return self.api_response(http_code=400, error=str(err))

        session = SessionModel.query.filter_by(name=session_name).first()
        if not session:  # session has not existed
            try:
                # add new session to database and create backup folder
                session = SessionModel(creator_id, session_name)
            except Exception as err:
                _logger.error(err)
                return self.api_response(http_code=400,
                                         error='Tên session không hợp lệ!')
            try:
                create_folder(SessionModel._data_path(
                    creator_id, session_name))
                db.session.add(session)
                db.session.commit()
            except Exception as err:
                _logger.error(err)
                db.session.rollback()
                return self.api_response(http_code=500)
        try:
            resolve_session_data(session=session, request=request)
            return self.api_response(data='Success', http_code=200)
        except ValueError as err:
            _logger.error(err)
            return self.api_response(http_code=400, error=str(err))
        except Exception as err:
            _logger.error(err)
            return self.api_response(http_code=500)

    @staticmethod
    def _valid_params(creator_id, session_name):
        if not creator_id or not session_name:
            raise ValueError('Thiếu tham số!')
        if not UserModel.query.filter_by(id=creator_id).first():
            raise ValueError('Người dùng không tồn tại!')


@api.route('/backup/<int:creator_id>/<string:session_name>/clean-up')
class Clean(Resource, BaseApi):
    @api.doc(description='Xóa các file rác trong một session')
    def put(self, creator_id, session_name):
        try:
            payload = util.valid_req(request, comp_attr=['filenames'])
            filenames = payload['filenames']
            session = SessionModel.query.filter_by(
                creator_id=creator_id, name=session_name).first()
            if not session:
                raise HandledError(404, 'Session không tồn tại!')
            video_files = [f for f in filenames if VideoModel._is_video(f)]
            clean_backup_data(
                session=session,
                filenames=filenames,
                video_files=[sol_ext(f)[0] for f in video_files]
            )
            return self.api_response()
        except HandledError as err:
            _logger.error(err)
            return self.api_response(handled_error=err)
        except Exception as err:
            _logger.error(err)
            return self.api_response(http_code=500, error=str(err))
