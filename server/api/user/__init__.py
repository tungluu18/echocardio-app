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

user_fields = api.model('user_fields', {
    'password': fields.String(),
    'job': fields.String(),
    'organization': fields.String(),
    'address': fields.String(),
    'phone': fields.String()
})


@api.route('/<int:user_id>')
class UserDetail(Resource, BaseApi):
    @api.doc(description='Trả về thông tin cụ thể của user theo user_id')
    def get(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                return self.api_response(error='Tài khoản không tồn tại',
                                         http_code=404)
            user_dump = user_schema.dump(user).data
            resp = util.remove_attr(user_dump,
                                    ['password', 'created_at', 'updated_at'])
            return self.api_response(data=resp)
        except Exception as err:
            _logger.error(err)
            return self.api_response(error='Internal server error!',
                                     http_code=500)

    @api.doc(description='Cập nhật thông tin cho user theo user_id')
    @api.expect(user_fields)
    def put(self, user_id):
        try:
            update_args = util.valid_req(
                request=request,
                ext_attr=['password', 'job', 'organization',
                          'phone', 'address'])
        except ValueError as err:
            return self.api_response(error=str(err), http_code=400)

        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return self.api_response(error='Tài khoản không tồn tại',
                                     http_code=404)

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


@api.route('/')
class Users(Resource, BaseApi):
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


from api.user import signup
from api.user import login
