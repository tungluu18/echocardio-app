# coding=utf-8

import logging
from flask import Flask, redirect, url_for, send_from_directory, request
from flask_cors import CORS

import model
from api import api_blueprint


__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

app = Flask(__name__)

# config app from file config.py
app.config.from_pyfile("config.py", silent=True)

# databse setup
model.init_app(app)

# add blueprint apis
app.register_blueprint(api_blueprint)

# serve files
@app.route('/data/<path:filename>')
def download_file(filename):
    return send_from_directory(
        app.config['DATA_DIR'], filename, as_attachment=True)


# redirect to api page
@app.route('/')
def redirect_to_blueprint():
    return redirect(api_blueprint.url_prefix)

# cross origin resource sharing
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.logger.handlers.extend(_logger.handlers)
app.logger.setLevel(logging.DEBUG)

# run
if __name__ == "__main__":
    app.run()
