# coding=utf-8
import logging
import json

from flask import request, redirect
from model import User as UserModel, Session as SessionModel, Video as VideoModel
from web.admin import web, jinja_env
from web import routing_table, web_blueprint
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
    try:
        link_files = session.get_all_files()
        files = [resolve_from_link(link) for link in link_files]
        for file in files:
            if file['type'] == 'video':
                file['data'] = dict({
                    "Auto ef": None,
                    "Manual ef": None,
                    "Number of chambers": None})
                video = VideoModel.query.filter_by(
                    session_id=session_id, name=file['name'].split('.')[0]).first()
                if video is not None:
                    annotation = video.annotation
                    try:
                        json_parsed = json.loads(annotation)
                        file['data']['Auto ef'] = json_parsed['auto_ef']
                        file['data']['Manual ef'] = json_parsed['man_ef']
                        file['data']['Number of chambers'] = json_parsed['chamber']
                    except Exception as err:
                        _logger.error(err)
    except ValueError as err:
        _logger.error(err)
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
    except Exception as err:
        _logger.error(err)
        return redirect(web_blueprint.url_prefix + routing_table['admin']['404'])
    return session_detail_template.render({'session': session, 'files': files})
