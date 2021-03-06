import os
import logging
from dotenv import load_dotenv

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

load_dotenv()

# URL
HOST_URL = 'http://localhost:5000'

# DIRECTORY
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = 'data'
UPLOAD_DIR = 'data/tmp'

# DATABASE
_DB_NAME = os.getenv('DB_NAME', 'echo_cardio')
_DB_USER = os.getenv('DB_USER', 'tungluu18')
_DB_PWD =  os.getenv('DB_PWD', 'tekovn1234')
_DB_HOST = os.getenv('DB_HOST', 'localhost')
_DB_PORT = os.getenv('DB_PORT', '3306')

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % \
        (_DB_USER, _DB_PWD, _DB_HOST, _DB_PORT, _DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'json', 'mp4'])

# UPLOAD FILES
MAX_CONTENT_LENGTH = 1000 * 1024 * 1024
