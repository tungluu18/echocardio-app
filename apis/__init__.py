from flask_restplus import Api
from flask import Blueprint

from .user import api as api_user
from .session import api as api_session

api_blueprint = Blueprint(
    'blueprint',
    __name__,
    url_prefix='/api/v1'
)

api = Api(
    app=api_blueprint,
    title='Echocardio App Api',
    version='1.0'
)

api.add_namespace(api_user)
api.add_namespace(api_session)
