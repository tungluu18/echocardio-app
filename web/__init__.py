# coding=utf-8
import logging
from flask import Blueprint

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

web_blueprint = Blueprint('web_v1', __name__, url_prefix='/website', static_folder='test', static_url_path='/test')

from web.routes import routing_table
from web import admin
