#!/usr/bin/env bash
#activate venv
source ./venv/bin/activate

#start flask app
export FLASK_APP=echo_cardio
export FLASK_ENV=development
export FLASK_DEBUG=true
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app --reload
