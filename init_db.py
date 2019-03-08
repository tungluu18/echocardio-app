# coding=utf-8

import logging
from model import db
from echo_cardio import app

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

print('Clearing data...')
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
db.drop_all()

print('Creating database...')
db.create_all()
print('Database created!')
