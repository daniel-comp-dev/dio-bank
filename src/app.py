"""

========================

Exemplos introdutórios

========================

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.route("/hello")
def hello():
    return "Hello, World"


@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile for that user
    return f"User {username}"


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f"Post {post_id}"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Método POST"
    else:
        return "Método GET"


@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()
"""

import os

from flask import Flask


# Factorie
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)  # Instancia arq. de conf.
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="diobank.sqlite",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db

    db.init_app(app)

    return app
