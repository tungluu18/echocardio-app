# coding=utf-8

import logging
import json
import util
from flask_restplus import Resource, Namespace, fields
from flask import jsonify, request
from api.api_base import BaseApi
from model import db
from model.user import UserSchema, User as UserModel
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

api = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_field = api.model('Resource', {
    'username': fields.String(255),
    'password': fields.String(255),
    'email': fields.String(255),
    'job': fields.String(255),
    'organization': fields.String(255),
    'address': fields.String(255),
    'phone': fields.String(20)
})


@api.route('/')
class User(Resource, BaseApi):
    @api.doc(description='Lay danh sach toan bo user')
    def get(self):
        all_users = UserModel.query.all()
        all_users_dumped = users_schema.dump(all_users).data
        # remove attributes of users in response
        remove_attr = ['password', 'created_at', 'updated_at']
        resp = list(map(
            lambda user: util.remove_attr(user, remove_attr),
            all_users_dumped))
        return self.api_response(data=resp)

    @api.doc(description='Cap nhat thong tin mot tai khoan')
    @api.expect(user_field)
    def put(self):
        try:
            update_args = util.valid_req(
                request=request,
                ext_attr=['password', 'job', 'organization',
                          'phone', 'address', 'email'],
                comp_attr=['username'])
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)

        if not UserModel.is_existed(username=update_args['username']):
            return self.api_response(error='Tài khoản không tồn tại',
                                     http_code=400)

        user = UserModel.query.filter_by(
            username=update_args['username']).first()

        if 'password' in update_args:
            update_args['password'] = UserModel._encrypt_password(
                update_args['password'])

        try:
            for key, value in update_args.items():
                setattr(user, key, value)
            db.session.commit()
            return self.api_response(data="Success")
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return self.api_response(error='Internal server error!',
                                     http_code=500)

from api.user import signup
from api.user import login
