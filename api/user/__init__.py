# coding=utf-8

import logging
import json
from flask_restplus import Resource, Namespace, fields
from flask import jsonify, request
from model import db
from model.user import UserSchema, User as UserModel

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

api = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_fields = api.model('Resource', {
    'username': fields.String(255),
    'password': fields.String(255),
    'email': fields.String(255)
})


@api.route('/')
class User(Resource):
    @api.doc(description='Lay danh sach toan bo user')
    def get(self):
        all_users = UserModel.query.all()
        all_users_dumped = users_schema.dump(all_users).data
        return jsonify(all_users_dumped)

    @api.doc(description='Tao moi 1 user', body=user_fields)
    @api.expect(user_fields)
    def post(self):
        new_user = self._parse_request_body(request)
        # check is username is existed
        if UserModel.is_existed(new_user['username']):
            return 'Tên tài khoản đã tồn tại', 400

        try:
            new_user_model = UserModel(
                username=new_user['username'],
                password=new_user['password'],
                email=new_user['email'])
            db.session.add(new_user_model)
            db.session.commit()
            return 'Success', 200
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            return 'Internal server error!', 500

    @staticmethod
    def _parse_request_body(request):
        data_dict = json.loads(request.data)
        return data_dict
