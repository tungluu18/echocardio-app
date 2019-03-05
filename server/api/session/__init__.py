# coding=utf-8

import logging
from flask import request
from flask_restplus import Resource, Namespace, fields
from api.api_base import BaseApi
from model import db
from model.user import User as UserModel
from model.session import Session as SessionModel
from module.dir import create_session_folder, \
    get_session_folder_path, remove_session_folder
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

api = Namespace('sessions')

session_field = api.model('session_fields', {
    'patient_name': fields.String(required=True),
    'patient_age': fields.String(required=True),
    'creator_id': fields.Integer(required=True)
})


@api.route('/')
class Session(Resource, BaseApi):
    def get(self):
        return "OK"

    @api.doc(desciption='Tạo mới 1 session')
    @api.expect(session_field)
    def post(self):
        try:
            create_args = util.valid_req(
                request=request,
                comp_attr=['creator_id', 'patient_name', 'patient_age'])
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)

        if not UserModel.query.filter_by(
                id=int(create_args['creator_id'])).first():
            return self.api_response(error='Người tạo không hợp lệ',
                                     http_code=400)

        try:
            session = SessionModel(**create_args)
            db.session.add(session)
            db.session.commit()
            data_path = create_session_folder(session.id)
            setattr(session, 'data_path', get_session_folder_path(session.id))
            db.session.commit()
            return self.api_response(data={'session_id': session.id})
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return self.api_response(error='Internal server error!',
                                     http_code=500)
