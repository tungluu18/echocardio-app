# coding=utf-8

import logging
import json
import util
from flask_restplus import Resource, Namespace, fields
from flask import jsonify, request
from model import db
from model.user import UserSchema, User as UserModel

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
class User(Resource):
    @api.doc(description='Lay danh sach toan bo user')
    def get(self):
        all_users = UserModel.query.all()
        all_users_dumped = users_schema.dump(all_users).data
        # remove attributes of users in response
        remove_attr = ['password', 'created_at', 'updated_at']
        resp = list(map(
            lambda user: util.remove_attr(user, remove_attr),
            all_users_dumped))
        return jsonify(resp)

    @api.doc(description='Tao moi 1 user', body=user_field)
    @api.expect(user_field)
    def post(self):
        new_user = self._parse_request_body(request)
        # verify compulsory args
        try:
            self._valid_signin(new_user)
        except ValueError as err:
            return str(err), 400

        # check if username is existed
        if UserModel.is_existed(new_user['username']):
            return 'Tên tài khoản đã tồn tại', 400

        try:
            new_user_model = UserModel(**new_user)
            db.session.add(new_user_model)
            db.session.commit()
            return 'Success', 200
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return 'Internal server error!', 500

    @api.doc(description='Cap nhat thong tin mot tai khoan', body=user_field)
    def put(self):
        update_user = self._parse_request_body(request)
        selected_user = UserModel.query.filter_by(
            username=update_user['username']).first()
        if not selected_user:
            return 'Tài khoản không tồn tại', 400

        update_user = util.remove_attr(update_user,
                                       ['id', 'username', 'email'])
        if 'password' in update_user:
            update_user['password'] = UserModel._encrypt_password(
                update_user['password'])

        try:
            for key, value in update_user.items():
                setattr(selected_user, key, value)
            db.session.commit()
            return 'Success'
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return 'Internal server error!', 500

    @staticmethod
    def _parse_request_body(request):
        data_dict = json.loads(request.data)
        return data_dict

    @staticmethod
    def _valid_signin(new_user):
        """ Verify 3 arguments that request must have to sign in:
                username, email, password
        """
        if 'username' not in new_user:
            raise ValueError('Thiếu tên tài khoản')
        if 'password' not in new_user:
            raise ValueError('Thiếu mật khẩu')
        if 'email' not in new_user:
            raise ValueError('Thiếu địa chỉ email')

from api.user import login
