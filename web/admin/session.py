# coding=utf-8
import logging

from flask import request, redirect
from model import User as UserModel, Session as SessionModel
from web.admin import web, jinja_env
from web import routing_table
from module.file import resolve_from_link

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

@web.route(routing_table['admin']['session'] + '/<int:user_id>/session', methods=['GET'])
def view_session(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    sessions = SessionModel.query.filter_by(creator_id=user_id).all()
    session_template = jinja_env.get_template('session.html')
    return session_template.render({
        'user': user,
        'sessions': sessions
    })

@web.route(routing_table['admin']['session'] + '/<int:user_id>/session/<int:session_id>', methods=['GET'])
def view_session_detail(user_id, session_id):
    session = SessionModel.query.filter_by(id=session_id).first()
    session_detail_template = jinja_env.get_template('session_detail.html')
    link_files = session.get_all_files()
    files = [resolve_from_link(link) for link in link_files]
    print(files)
    return session_detail_template.render({'session': session, 'files': files})
