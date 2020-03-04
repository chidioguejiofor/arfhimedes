from .custom_fields import StringField, fields
from api.models import StatusEnum
from marshmallow import Schema
from marshmallow_enum import  EnumField

class UserSchema(Schema):
    id = fields.Integer()
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(min_length=3, required=True, max_length=320)
    username = StringField(required=True)
    password = StringField(min_length=7, required=True,
                           load_only=True,)
    verified = StringField(required=True, dump_only=True)


class LoginSchema(Schema):
    username_or_email = StringField(min_length=3, required=True, max_length=320)
    password = StringField(min_length=7, required=True,
                           load_only=True,)


class UserStorySchema(Schema):
    id = fields.Integer()
    summary = StringField(required=True)
    description = StringField(required=True)
    type = StringField(required=True)
    complexity = fields.Integer()
    cost = fields.Integer()
    estimated_complete_time = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by = fields.Nested(UserSchema)
    assignee = fields.Nested(UserSchema)
    status = EnumField(enum=StatusEnum,
                       by_value=False, dump_only=True)

class StatusSchema(Schema):
    status = EnumField(enum=StatusEnum,
              by_value=False,
              required=True)



class AssignUserStorySchema(Schema):
    admin_id = fields.Integer(required=True)

