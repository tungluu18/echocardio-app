from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    :param app: Flask app
    :return:
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "user"

    def __init__(self, id, name):
        self.id = id
        self.name = name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)