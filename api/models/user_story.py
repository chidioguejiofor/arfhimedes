from settings import db
from datetime import  datetime, timezone


class UserStory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.String,nullable=False)
    complexity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer,nullable=False)
    estimated_complete_time = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
    )
    created_by_id = db.Column(
        db.Integer,db.ForeignKey('user.id', ondelete='RESTRICT',onupdate='CASCADE')
    )

    created_by = db.relationship("User")

    def save(self):
        db.session.add(self)
        db.session.commit()
