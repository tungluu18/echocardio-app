# coding=utf-8
from flask import Flask
from apis import api_blueprint
from model import db, init_app
from flask_migrate import Migrate

app = Flask(__name__)

# config app from file config.py
app.config.from_pyfile("config.py", silent=True)

# databse setup
init_app(app)
# db.create_all()
migrate = Migrate(app, db)
migrate.init_app(app)

# add blueprint
app.register_blueprint(api_blueprint)

# run
app.run(
    debug=True,
    port=5001
)
