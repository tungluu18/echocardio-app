# coding=utf-8

import logging
from flask_restplus import Namespace, Resource
from api.api_base import BaseApi

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

api = Namespace('assets')


@api.route('/')
class Asset(Resource, BaseApi):
    def post(self):
        pass

from . import upload
