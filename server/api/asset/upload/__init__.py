# coding=utf-8

import logging
import os
import config
from flask import request, url_for
from flask_restplus import Resource
from api.asset import api
from api.api_base import BaseApi
from module.file import save_file_to_dir

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'json', 'mp4'])


def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/upload')
class Upload(Resource, BaseApi):
    def post(self):
        if not len(request.files):
            return self.api_response(error="There is no file", http_code=400)
        resp = []
        for _ in request.files:
            file = request.files[_]
            try:
                saved_file_path = save_file_to_dir(
                    dir='testasd/user_1',
                    file=file)
                resp.append(saved_file_path)
            except Exception as err:
                _logger.error(err)
        return self.api_response(data=resp)
