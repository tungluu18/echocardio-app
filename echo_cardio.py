# coding=utf-8
import logging
from flask import Flask, redirect, url_for
from apis import api_blueprint
import model

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

app = Flask(__name__)

# config app from file config.py
app.config.from_pyfile("config.py", silent=True)

# databse setup
model.init_app(app)

# add blueprint apis
app.register_blueprint(api_blueprint)

@app.route('/')
def redirect_to_blueprint():
    return redirect(api_blueprint.url_prefix)

# run
if __name__ == "__main__":
    app.run(port=5001)
