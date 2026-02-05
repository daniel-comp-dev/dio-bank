from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


# @jwt_required()
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {"id": user.role.id, "name": user.role.name},
        }
        for user in users
    ]


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def list_or_created_user():
    print("teste")
    user_id = int(get_jwt_identity())
    user = db.get_or_404(User, user_id)
    print(user_id)
    if user.role.name != "admin":
        return {"message": "User dont have access"}, HTTPStatus.FORBIDDEN
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


@app.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "Delete", HTTPStatus.NO_CONTENT
