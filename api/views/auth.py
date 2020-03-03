from settings import endpoint
from flask import request
from flask_restplus import Resource
from api.models import User
from api.schemas import UserSchema
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
