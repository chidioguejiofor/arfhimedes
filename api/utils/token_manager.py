import os
import jwt
from datetime import datetime, timedelta


class TokenManager:
    SECRET = os.getenv('JWT_SECRET')

    @classmethod
    def decode_token_data(cls, token, verify=True):
        return cls.decode_token(token, verify)['data']

    @classmethod
    def decode_token(cls, token, verify=True):
        token_data = jwt.decode(token,
                                cls.SECRET,
                                algorithms=['HS256'],
                                verify=verify)
        return token_data

    @classmethod
    def create_token(cls, token_data, **timedelta_kwargs):
        if not timedelta_kwargs:
            timedelta_kwargs = {'days': 2}
        current_time = datetime.utcnow()
        payload = {
            'data': token_data,
            'exp': current_time + timedelta(**timedelta_kwargs),
            'iat': current_time,
        }
        return jwt.encode(payload, cls.SECRET,
                          algorithm='HS256').decode('utf-8')
