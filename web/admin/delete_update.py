# coding=utf-8
import logging
import json

from flask import redirect, request, url_for
from api.user import api as api_user, UserDetail
from model import db
from model.user import User as UserModel, UserSchema
from web.routes import routing_table
from web.admin import web
from web import web_blueprint
from web.admin import jinja_env

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


UserDetailApi = UserDetail(api_user)
user_schema = UserSchema()


@web.route(routing_table['admin']['delete'], methods=['POST'])
def delete_user():
    user_id = request.args.get('user_id', None)
    if not user_id:
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
    try:
        UserDetailApi.delete(user_id)
        return redirect(web_blueprint.url_prefix + routing_table['admin']['homepage'])
    except Exception as err:
        _logger.error(err)
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])


@web.route(routing_table['admin']['update'] + '/<int:user_id>', methods=['GET'])
def render_update_user_form(user_id):
    css_url = url_for('static', filename='bootstrap.min.css')
    update_user_template = jinja_env.get_template('update_user.html')
    return update_user_template.render({
        'user': UserModel.query.filter_by(id=user_id).first(),
        'update_user_url': web_blueprint.url_prefix + routing_table['admin']['update'] + '/' + str(user_id),
        'css_url': css_url
    })


@web.route(routing_table['admin']['update'] + '/<int:user_id>', methods=['POST'])
def update_user(user_id):
    content = request.form
    user_fields = ['email', 'organization', 'department', 'job', 'phone', 'address']
    try:
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            raise Exception()
        for key in user_fields:
            value = content.get(key, None)
            if value:
                setattr(user, key, value)
        db.session.commit()
        return redirect(web_blueprint.url_prefix + routing_table['admin']['homepage'])
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
