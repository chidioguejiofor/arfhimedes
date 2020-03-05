from functools import wraps
from flask import request
from flask_restplus import Resource
from api.models import User
import jwt
from api.utils.token_manager import TokenManager
from api.utils.exceptions import ResponseException


class AuthenticationDecorator:
    def __init__(self, view):
        self.view = view

    def _decode_token(self, check_user_is_verified=False):
        """Decoded a token and returns the decoded data

        Args:
            token_type (int, optional): The type of token being decoded
                Defaults to `1`(LOGIN_TOKEN)
            check_user_is_verified (bool): When this is true, this ensures that
                the user is also verified

        Returns:
            dict, str: The decoded token data
        """
        auth = request.headers.get('Authorization')
        if not auth:
            raise ResponseException(
                message='Please provided a valid token',
                status_code=401,
            )
        auth = auth.split(' ')
        if len(auth) != 2 or auth[0] != 'Bearer':
            raise ResponseException(
                message='Please provided a valid token',
                status_code=401,
            )
        try:
            return TokenManager.decode_token_data(auth[1])

        except jwt.exceptions.PyJWTError as e:
            raise ResponseException(
                message='Token provided is invalid',
                status_code=401,
            )

    def _authenticate_user(self):
        view = self.view
        method = request.method.upper()
        method_is_protected = method in view.PROTECTED_METHODS
        method_is_admin_only = method in view.ADMIN_METHODS
        decoded_data = None

        if method_is_protected:
            decoded_data = self._decode_token()
            return decoded_data
        if method_is_protected and method_is_admin_only:
            user = User.query.filter_by(id=decoded_data.get('id'),
                                        is_admin=True).first()
            if not user:
                raise ResponseException(
                    message='You dont have permission to perform this action',
                    status_code=401,
                )
        return decoded_data

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_data = self._authenticate_user()
            if user_data:
                return func(*args, **kwargs, user_data=user_data)
            return func(*args, **kwargs)

        return wrapper


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class BaseView(Resource):
    PROTECTED_METHODS = []
    ADMIN_METHODS = []

    @classproperty
    def method_decorators(self):
        return [AuthenticationDecorator(self)]
