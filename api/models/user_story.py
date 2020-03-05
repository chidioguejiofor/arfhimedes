import enum
from settings import db
from datetime import datetime, timezone
from .base import BaseModel


class StatusEnum(enum.Enum):
    APPROVED = 1
    REJECTED = 2


class UserStory(BaseModel):
    summary = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    complexity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    estimated_complete_time = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at = db.Column(db.DateTime(timezone=True), )
    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='CASCADE'))
    status = db.Column(db.Enum(StatusEnum, name='status_enum'), )
    assignee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='CASCADE'))

    assignee = db.relationship("User", foreign_keys=[assignee_id])
    created_by = db.relationship("User", foreign_keys=[created_by_id])
