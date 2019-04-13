# coding=utf-8
import logging

from flask import request, redirect, make_response
from model import db
from model.user import User as UserModel
from web.admin import web
from web import web_blueprint, routing_table

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

@web.route(routing_table['admin']['activate'], methods=['GET', 'POST'])
def activate_user():
    user_id = request.args.get('user_id', None)
    if not user_id:
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
    try:
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
        user.status = 'active'
        db.session.commit()
        return redirect(web_blueprint.url_prefix + routing_table['admin']['homepage'])
    except Exception as err:
        _logger.error(err)
        db.session.rollback()
        # return make_response('', 500)
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])