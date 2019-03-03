# coding=utf-8

import logging
import json
from flask import jsonify, request
from flask_restplus import Resource, fields
from api.user import api
from model.user import User as UserModel, UserSchema


__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


login_fields = api.model('Resource', {
    'username': fields.String(255),
    'password': fields.String(255)
})

user_schema = UserSchema()


@api.route('/login')
class Login(Resource):
    @api.doc(description='Gửi username và password để đăng nhập',
             body=login_fields)
    @api.expect(login_fields)
    def post(self):
        login_args = json.loads(request.data)
        try:
            self._is_valid(login_args)
        except ValueError as err:
            return str(err), 400
        try:
            user = UserModel.query.filter_by(
                username=login_args['username']).first()
            if not user:
                return 'Tài khoản không tồn tại', 404
            user_dump = user_schema.dump(user).data
            # check password
            if UserModel._check_password(
                    pw_hash=user_dump['password'],
                    pw_raw=login_args['password']):
                return 'Success'
            else:
                return 'Sai mật khẩu', 404
        except Exception as e:
            return 'Internal server error!', 500

    @staticmethod
    def _is_valid(login_args):
        if 'username' not in login_args:
            raise ValueError('Thiếu tên đăng nhập')
        if 'password' not in login_args:
            raise ValueError('Thiếu mật khẩu')
