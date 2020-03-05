from .custom_fields import StringField, fields, DateTimeField
from api.models import StatusEnum
from marshmallow import Schema
from .user import UserSchema
from marshmallow_enum import EnumField


class UserStorySchema(Schema):
    id = fields.Integer()
    summary = StringField(required=True)
    description = StringField(required=True)
    type = StringField(required=True)
    complexity = fields.Integer()
    cost = fields.Integer()
    estimated_complete_time = DateTimeField(
        required=True, must_be_in_future=True,
        tz='utc'
    )
    created_at = DateTimeField(dump_only=True)
    updated_at = DateTimeField(dump_only=True)
    created_by = fields.Nested(UserSchema)
    assignee = fields.Nested(UserSchema)
    status = EnumField(enum=StatusEnum, by_value=False, dump_only=True)


class StatusSchema(Schema):
    status = EnumField(enum=StatusEnum, by_value=False, required=True)


class AssignUserStorySchema(Schema):
    admin_id = fields.Integer(strict=True, required=True)
