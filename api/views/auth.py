from settings import endpoint
from flask import request
from flask_restplus import Resource
from api.models import User
from api.schemas import UserSchema, LoginSchema
from api.utils.token_manager import TokenManager
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors


@endpoint('/register')
class Register(Resource):
    @staticmethod
    def post():
        schema = UserSchema()
        validated_data  = schema.load(request.get_json())
        user = User(**validated_data)
        try:
            user.save()
        except IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                return {
                    'message': 'Either the email or the username already exists',
                }, 409

        return {
            'message': 'You have been successfully registered',
            'data': schema.dump(user)
        }


@endpoint('/login')
class Login(Resource):
    @staticmethod
    def post():

        validated_data  = LoginSchema().load(request.get_json())
        username_or_email = validated_data['username_or_email']
        if '@' in username_or_email:
            user = User.query.filter_by(email=validated_data['username_or_email']).first()
        else:
            user = User.query.filter_by(username=validated_data['username_or_email']).first()

        if not user or not user.verify_password(validated_data['password']):
            return {
                'message': "Credentials not found"
            }, 404

        schema = UserSchema()
        data = schema.dump(user)
        token_data = {
            'id':user.id,
            'email': user.email,
            'username': user.username,
        }
        data['token'] = TokenManager.create_token(token_data, days=3)
        return {
            'message': 'You have been successfully registered',
            'data': data
        }
