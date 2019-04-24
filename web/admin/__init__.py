# coding=utf-8
import logging
import os

from flask import jsonify, url_for
from jinja2 import FileSystemLoader, Environment

from web import web_blueprint as web, routing_table
from model.user import User as UserModel, UserSchema

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_dir))


@web.route(routing_table['admin']['homepage'])
def get_homepage():
    users = UserModel.query.all()
    all_users = users_schema.dump(users).data
    homepage_template = jinja_env.get_template('homepage.html')
    css_url = url_for('static', filename='bootstrap.min.css')
    return homepage_template.render({
        'users': all_users,
        'css_url': css_url
    })


@web.route(routing_table['admin']['404'])
def get_404():
    error_404_template = jinja_env.get_template('404.html')
    css_url = url_for('static', filename='404/style.css')
    return error_404_template.render({
        'homepage_url': web.url_prefix + routing_table['admin']['homepage'],
        'css_url': css_url
    })

from web.admin import activate
from web.admin import delete_update
from web.admin import reset_password
from web.admin import session
