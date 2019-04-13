# coding=utf-8

import logging
import random
import string
from model import db, User
from echo_cardio import app

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def seed_users():
    new_users = []
    for _ in range(20):
        new_users.append(User(
            username=randomString(10),
            password='123456',
            email=randomString(10) + '@gmail.com',
            job=randomString(5),
            organization=randomString(20),
            department=randomString(20),
            address=randomString(10),
            phone=randomString(10)))
    print('Seeding users...')
    for user in new_users:
        db.session.add(user)
    db.session.commit()
    print('Completed!')


seed_users()
