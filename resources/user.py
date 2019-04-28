from flask_restful import Resource
from flask import request

from schemas.user import UserSchema
from models.user import UserModel

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

        if UserModel.verify_hash(data.get('password'), user.password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return {
                       'message': f'{user.username} welcome to server',
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 201
        return {"message": "User dosn`t exist"}, 401


class PairDevices(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = UserModel.find_by_name(data.get('username'))
        if not user:
            return {"message": f'{data.get("username")} doesn`t exist '}, 400

        if UserModel.verify_hash(data.get('password'), user.password):
            slider = DeviceModel.find_by_number(data.get('device_number'))
            if not slider:
                return {"message": f'device doesn`t exist in database'}, 400
            slider.owner_id = user.id
            slider.save_to_db()
            return {"message": 'device has been paired'}, 200
        return {"message": 'somethink went wrong'}, 405




