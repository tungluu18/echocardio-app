import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# DATABASE
## SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://tungluu18:tekovn123@localhost:3306/echo_cardio'
SQLALCHEMY_TRACK_MODIFICATIONS = False