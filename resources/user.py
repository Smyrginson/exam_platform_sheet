from flask_restful import Resource
from flask import request

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = user_schema.load(data)
        if UserModel.find_by_name(user.username):
            return {"message": "user already exist"}, 400

        user.password = data['password']
        user.save_to_db()

    @classmethod
    def register(cls, username, password):
        user = UserModel(username=username, password=password)
        user.save_to_db()
        return user


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        return user_schema.dump(user), 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = UserModel.find_by_name(data.get('username'))

        if not user:
            return {"message": f'{data.get("username")} doesn`t exist '}, 400

        return {"message": "User does not exist"}, 401

    @classmethod
    def login(cls, username, password):
        user = UserModel.find_by_name(username)
        if not user:
            return None

        if str(user.password) == password:
            return user
        return None



