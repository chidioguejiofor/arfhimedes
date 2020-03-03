from settings import db
from sqlalchemy import UniqueConstraint
from passlib.hash import pbkdf2_sha512


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    _password = None

    UniqueConstraint(email, name='user_unique_email')
    UniqueConstraint(username, name='user_unique_email')
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_str):
        self._password = password_str
        self.password_hash = pbkdf2_sha512.hash(password_str)

    def verify_password(self, password_str):
        return pbkdf2_sha512.verify(password_str, self.password_hash)

    def save(self):
        db.session.add(self)
        db.session.commit()
