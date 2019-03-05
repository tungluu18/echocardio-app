# coding=utf-8

import logging
import json
from flask import request
from flask_restplus import Resource, fields
from api.user import api, user_fields
from api.api_base import BaseApi
from model import db
from model.user import User as UserModel
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


@api.route('/signup')
class Signup(Resource, BaseApi):
    @api.doc(description='Đăng ký tài khoản')
    @api.expect(user_fields)
    def post(self):
        try:
            signup_args = util.valid_req(
                request,
                comp_attr=['username', 'password', 'email'],
                ext_attr=['job', 'organization', 'phone', 'address'])
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)

        # check if username is existed
        if UserModel.is_existed(signup_args['username']):
            return self.api_response(error='Tên tài khoản đã tồn tại',
                                     http_code=400)

        try:
            new_user = UserModel(**signup_args)
            db.session.add(new_user)
            db.session.commit()
            return self.api_response(data="Success")
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return self.api_response(error='Internal server error!',
                                     http_code=500)
