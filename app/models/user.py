import base64
import os

from datetime import datetime, timedelta
from hashlib import md5
from uuid import uuid4

from flask_security import UserMixin
from flask_security.utils import hash_password, verify_password, \
    verify_and_update_password, verify_hash

from sqlalchemy.ext.serializer import Serializer

from app import db
from config import Config


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(512), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=uuid4().hex)
    about_me = db.Column(db.String(255), default="")

    # SECURITY_TRACKABLE
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    last_login = db.Column(db.DateTime, default=datetime.utcnow())

    # SECURITY_CONFIRMABLE
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role',
                            secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    posts = db.relationship('Post',
                            backref=db.backref('author_id'))

    # def __init__(self, fs_uniquifier):
        # self.fs_uniquifier = uuid4().hex if None else fs_uniquifier

    def __repr__(self):
        return f"<User id: {self.id}, email: {self.email}>"

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_token(self, expiration=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expiration)
        db.session.add(self.token)

        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)

    @staticmethod
    def verify_auth_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(id=id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_user_by_email(email=email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def email_exists(email=email):
        if User.get_user_by_email(email) is not None:
            return True
        return False
