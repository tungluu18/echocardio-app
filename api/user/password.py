# coding=utf-8
import logging
from api.user import api, validation
from flask import request
from flask_restplus import Resource, fields
from api.api_base import BaseApi, HandledError
from model import db, User as UserModel
import util

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


change_password_fields = api.model('change_password_fields', {
    'old_password': fields.String(),
    'new_password': fields.String()
})

reset_password_fields = api.model('reset_password_fields', {
    'new_password': fields.String()
})

@api.route('/<int:user_id>/change-password')
class ChangePassword(Resource, BaseApi):
    @api.doc(description='Cho user doi mat khau')
    @api.expect(change_password_fields)
    def put(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                raise HandledError(
                    message='Tài khoản không tồn tại', error_code=404)
            assert user.is_active()
            payload = util.valid_req(
                request, comp_attr=['old_password', 'new_password'])
            if not UserModel._check_password(user.password, payload['old_password']):
                raise HandledError(
                    message='Mật khẩu cũ không đúng', error_code=400)
            setattr(user, 'password', UserModel._encrypt_password(
                payload['new_password']))
            db.session.commit()
            return self.api_response(data='Success')
        except HandledError as err:
            _logger.error(str(err))
            db.session.rollback()
            return self.api_response(handled_error=err)
        except Exception as err:
            _logger.error(str(err))
            print(str(err))
            db.session.rollback()
            return self.api_response(http_code=500, error='Internal server error!')


@api.route('<int:user_id>/reset-password')
class ResetPassword(Resource, BaseApi):
    @api.doc(description='Admin reset mật khẩu của người dùng.')
    @api.expect(reset_password_fields)
    @validation.exist()
    def put(self, user_id, user):
        try:
            payload = util.valid_req(request, comp_attr=['new_password'])
            setattr(user, 'password', UserModel._encrypt_password(payload['new_password']))
            db.session.commit()
            return self.api_response(data='Success')
        except Exception as err:
            _logger.error(str(err))
            db.session.rollback()
            return self.api_response(http_code=500)
