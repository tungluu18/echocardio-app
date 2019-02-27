# coding=utf-8
from flask import Flask
from apis import api_blueprint

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(api_blueprint)

    @app.route("/")
    def get():
        return "test"

    app.run(
        debug=True,
        port=5000
    )
