# coding=utf-8

import logging
from model import db, Basemodel, ma
from flask_bcrypt import generate_password_hash, \
    check_password_hash

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)
_round_number = 10


class User(Basemodel):
    __tablename__ = 'user'

    username = db.Column(db.String(length=255, collation='utf8_general_ci'), primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=True)
    organization = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=True)
    department = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=True)
    job = db.Column(db.String(length=255, collation='utf8_general_ci'), nullable=True)
    status = db.Column(db.String(length=20), default='inactive', nullable=False)

    def __init__(self, username, email, password,
                 job=None, address=None,
                 phone=None, organization=None,
                 department=None):
        self.username = username
        self.email = email
        self.password = self._encrypt_password(password)
        self.job = job
        self.phone = phone
        self.address = address
        self.organization = organization
        self.department = department

    @classmethod
    def is_existed(self, username):
        return bool(self.query.filter_by(username=username).first())

    def is_active(self):
        if self.status != 'active':
            raise ValueError('User %s has not been activated by admin.' % (self.username))
        return True

    @staticmethod
    def _encrypt_password(password):
        pw_hashed = generate_password_hash(password, _round_number)
        pw_hashed_decoded = pw_hashed.decode("utf-8")
        return pw_hashed_decoded

    @staticmethod
    def _check_password(pw_hash, pw_raw):
        return check_password_hash(pw_hash, pw_raw)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
