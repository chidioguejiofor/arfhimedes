from marshmallow import Schema, fields
from .custom_fields import StringField


class UserSchema(Schema):
    id = fields.Integer()
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(min_length=3, required=True, max_length=320)
    username = StringField(required=True)
    password = StringField(
        min_length=7,
        required=True,
        load_only=True,
    )
    is_admin = fields.Boolean(dump_only=True)
    verified = StringField(required=True, dump_only=True)


class LoginSchema(Schema):
    username_or_email = StringField(min_length=3,
                                    required=True,
                                    max_length=320)
    password = StringField(
        min_length=7,
        required=True,
        load_only=True,
    )
