# coding=utf-8

import logging
from flask_restplus import fields
from api import api

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class HandledError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return 'Error code [%s]: %s' % (self.error_code, self.message)

    def __repr__(self):
        return 'Error code [%s]: %s' % (self.error_code, self.message)


class BaseApi(object):
    GENERAL_RESP = api.model('GENERAL_RESP', {
        'error': fields.Integer(),
        'data': fields.String()
    })

    @staticmethod
    def api_response(http_code=200, data=None, error=None, handled_error=None):
        """ Return http response
        :param str error: error message, null if no error
        :param obj data: response data
        :param int http_code:
        """
        if isinstance(handled_error, HandledError):
            error, http_code = handled_error.message, handled_error.error_code
        if http_code == 500:
            error = error or 'Internal server error!'
        if http_code == 200:
            data = data or 'Success'
        return {
            'error': error,
            'data': data
        }, http_code
