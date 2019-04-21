#coding=utf-8
import logging
from model import User as UserModel
from api.api_base import HandledError

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

def exist(active=False):
    def validate(func):
        def wrapper(self, **kwargs):
            try:
                user_id = kwargs.get('user_id', None)
                if not user_id:
                    raise HandledError(error_code=400, message='Thiếu user_id')
                user = UserModel.query.filter_by(id=user_id).first()
                if not user:
                    raise HandledError(error_code=404, message='Tài khoản không tồn tại')
                if active:
                    assert user.is_active()
                kwargs['user'] = user
                return func(self, **kwargs)
            except HandledError as err:
                _logger.error(str(err))
                return self.api_response(handled_error=err)
            except ValueError as err:
                _logger.error(str(err))
                return self.api_response(http_code=400, error=str(err))
        return wrapper

    return validate
