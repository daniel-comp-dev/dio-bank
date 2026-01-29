from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
        }
        for user in users
    ]


@app.route("/", methods=["GET", "POST"])
def handle_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}


@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    print(user)
    print(type(user))
    return {
        "id": user.id,
        "username": user.username,
    }


# UMA FORMA DE REALIZAR O PATCH

# @app.route("/<int:user_id>", methods=["PATCH"])
# def update_user(user_id):
#     user = db.get_or_404(User, user_id)
#     data = request.json

#     if "username" in data:
#         user.username = data["username"]
#         db.session.commit()

#     return {
#         "id": user.id,
#         "username": user.username,
#     }

# OUTRA FORMA DE REALIZAR PATCH
from sqlalchemy import inspect


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    print(mapper)
    print(type(mapper))

    for column in mapper.attrs:
        if column.key in data:
            print(column)
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }
