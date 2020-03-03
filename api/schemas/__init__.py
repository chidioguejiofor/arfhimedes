from .custom_fields import StringField, fields
from marshmallow import Schema


class UserSchema(Schema):
    id = fields.Integer()
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(min_length=3, required=True, max_length=320)
    username = StringField(required=True)
    password = StringField(min_length=7, required=True,
                           load_only=True,)
    verified = StringField(required=True, dump_only=True)

