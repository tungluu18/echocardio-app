# coding=utf-8
import logging

from flask import request, redirect
from model import db
from model.user import User as UserModel
from web.admin import web, jinja_env
from web import web_blueprint, routing_table
from api.user import validation

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

error_404_template = jinja_env.get_template('404.html')


@web.route(routing_table['admin']['reset-password'] + '/<int:user_id>',
           methods=['GET'])
def reset_password_view(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    if not user:
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
    reset_password_template = jinja_env.get_template('reset-password.html')
    return reset_password_template.render({'user': user})


@web.route(routing_table['admin']['reset-password'] + '/<int:user_id>',
           methods=['POST'])
def reset_password(user_id):
    try:
        payload = request.form
        new_password = payload.get('new_password', None)
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            raise Exception
        setattr(user, 'password', UserModel._encrypt_password(new_password))
        db.session.commit()
        return redirect(web_blueprint.url_prefix + routing_table['admin']['homepage'])
    except Exception as err:
        _logger.error(str(err))
        db.session.rollback()
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
