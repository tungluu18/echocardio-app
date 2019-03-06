import os

# DIRECTORY
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = 'data'
SESSION_DIR = 'sessions'
UPLOAD_DIR = 'data/tmp'

# DATABASE
_DB_NAME = 'echo_cardio'
_DB_USER = 'tungluu18'
_DB_PWD = 'tekovn1234'
_DB_HOST = 'localhost'
_DB_PORT = '3306'

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % \
        (_DB_USER, _DB_PWD, _DB_HOST, _DB_PORT, _DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'json', 'mp4'])
