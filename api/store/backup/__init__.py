# coding=utf-8
import logging
import os

from flask_restplus import Resource, fields
from flask import request

from api.store import api
from api.store.backup.helper import resolve_session_data
from api.api_base import BaseApi

from model import db
from model.user import User as UserModel
from model.session import Session as SessionModel
from module.dir import create_folder

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


@api.route('/backup/<int:creator_id>/<string:session_name>')
class Backup(Resource, BaseApi):
    @api.doc(description='Backup data của một session')
    def post(self, creator_id, session_name):
        try:
            session = self._valid_params(creator_id, session_name)
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)
        if not SessionModel.query.filter_by(creator_id=creator_id,
                patient_name=session.patient_name, patient_age=session.patient_age).first():
            # session has not existed
            try:
                # add new session to database and create backup folder
                create_folder(SessionModel._data_path(creator_id, session_name))
                db.session.add(session)
                db.session.commit()
            except Exception as err:
                _logger.error(err)
                db.session.rollback()
                return self.api_response(http_code=500, error='Internal server error!')
        else:
            # session has existed
            session = SessionModel.query.filter_by(creator_id=creator_id,
                patient_name=session.patient_name, patient_age=session.patient_age).first()

        try:
            resolve_session_data(session=session, request=request)
            return self.api_response(data='Success', http_code=200)
        except ValueError as err:
            pass
        except Exception as err:
            _logger.error(err)
            return self.api_response(http_code=500, error='Internal server error!')

    @staticmethod
    def _valid_params(creator_id, session_name):
        if not creator_id or not session_name:
            raise ValueError('Thiếu tham số!')
        if not UserModel.query.filter_by(id=creator_id).first():
            raise ValueError('Người dùng không tồn tại!')
        try:
            session = SessionModel(creator_id, session_name)
            return session
        except Exception as err:
            raise ValueError('Tên session không hợp lệ!')
