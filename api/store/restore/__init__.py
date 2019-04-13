# coding=utf-8
import logging
import os

from flask import current_app as app
from flask_restplus import Resource

from model.user import User as UserModel
from model.session import Session as SessionModel
from api.api_base import BaseApi
from api.store import api

_author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


@api.route('/restore/<int:user_id>')
class Restore(Resource, BaseApi):
    @api.doc(description='Restore data đã backup theo user_id')
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return self.api_response(error='Người dùng không tồn tại!', http_code=400)
        try:
            assert user.is_active()
        except ValueError as err:
            _logger.error(err)
            return self.api_response(http_code=400, error=str(err))
        resp = []
        sessions = SessionModel.query.filter_by(creator_id=user_id)
        for session in sessions:
            session_data = {
                'name': session.name,
                'patient_name': session.patient_name,
                'patient_age': session.patient_age,
                'created_at': str(session.created_at),
                'man_ef': session.man_ef,
                'auto_ef': session.auto_ef,
                'data': []
            }
            session_path = SessionModel._data_path(session.creator_id, session.name)
            for file in os.listdir(os.path.join(
                *[app.config['ROOT_DIR'], app.config['DATA_DIR'], session_path])):
                file__download_link = os.path.join(
                    *[app.config['HOST_URL'], app.config['DATA_DIR'], session_path, file])
                session_data['data'].append(file__download_link)
            resp.append(session_data)
        return self.api_response(data=resp)

