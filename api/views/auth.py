from settings import endpoint
from flask import request
from api.models import User
from api.schemas import UserSchema, LoginSchema
from api.utils.token_manager import TokenManager
from api.utils.messages import (
    SIGN_UP_SUCCESS, USER_ALREADY_EXISTS,
    LOGIN_FAILED, LOGIN_SUCCESS
)
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors
from .base import BaseView


@endpoint('/register')
class Register(BaseView):
    @staticmethod
    def post():
        schema = UserSchema()
        validated_data = schema.load(request.get_json())
        user = User(**validated_data)
        try:
            user.save()
        except IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                return {
                    'message': USER_ALREADY_EXISTS,
                }, 409

        return {
            'message': SIGN_UP_SUCCESS,
            'data': schema.dump(user)
        }, 201


@endpoint('/login')
class Login(BaseView):
    @staticmethod
    def post():
        validated_data = LoginSchema().load(request.get_json())
        username_or_email = validated_data['username_or_email']
        if '@' in username_or_email:
            user = User.query.filter_by(
                email=validated_data['username_or_email']).first()
        else:
            user = User.query.filter_by(
                username=validated_data['username_or_email']).first()

        if not user or not user.verify_password(validated_data['password']):
            return {'message': LOGIN_FAILED}, 404

        schema = UserSchema()
        data = schema.dump(user)
        token_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }
        data['token'] = TokenManager.create_token(token_data, days=3)
        return {
            'message': LOGIN_SUCCESS,
            'data': data
        }
