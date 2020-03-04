from settings import db
from sqlalchemy import UniqueConstraint
from passlib.hash import pbkdf2_sha512
from .base import BaseModel

class User(BaseModel):
    first_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    _password = None

    UniqueConstraint(email, name='user_unique_email')
    UniqueConstraint(username, name='user_unique_username')
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_str):
        self._password = password_str
        self.password_hash = pbkdf2_sha512.hash(password_str)

    def verify_password(self, password_str):
        return pbkdf2_sha512.verify(password_str, self.password_hash)

