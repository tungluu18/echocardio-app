# coding=utf-8

import logging
import json
from flask import request
from flask_restplus import Resource, fields
from api.user import api
from api.api_base import BaseApi
from model.user import User as UserModel, UserSchema
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


login_fields = api.model('login_fields', {
    'username': fields.String(255),
    'password': fields.String(255)
})

user_schema = UserSchema()


@api.route('/login')
class Login(Resource, BaseApi):
    @api.doc(description='Gửi username và password để đăng nhập')
    @api.expect(login_fields)
    def post(self):
        try:
            login_args = util.valid_req(
                request=request, comp_attr=['username', 'password'])
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)
        try:
            # find user by username
            user = UserModel.query.filter_by(
                username=login_args['username']).first()
            if not user:
                return self.api_response(
                    error='Tài khoản không tồn tại', http_code=400)

            # dump user to dict
            user_dump = user_schema.dump(user).data

            # check password
            if not UserModel._check_password(
                    pw_hash=user_dump['password'],
                    pw_raw=login_args['password']):
                return self.api_response(error='Sai mật khẩu', http_code=400)

            # filter before response
            resp = util.remove_attr(
                user_dump,
                ['password', 'created_at', 'updated_at'])
            return self.api_response(data=resp)
        except Exception as e:
            return self.api_response(
                error='Internal server error!', http_code=500)
