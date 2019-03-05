# coding=utf-8

import logging
from flask_restplus import fields
from api import api

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class BaseApi(object):
    GENERAL_RESP = api.model('GENERAL_RESP', {
        'error': fields.Integer(),
        'data': fields.String()
    })

    @staticmethod
    def api_response(data=None, error=None, http_code=200):
        """ Return http response
        :param str error: error message, null if no error
        :param obj data: response data
        :param int http_code:
        """
        return {
            'error': error,
            'data': data
        }, http_code
