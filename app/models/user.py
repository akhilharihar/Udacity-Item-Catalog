from os import getenv
from app.database import db, DefaultTableMixin
from flask_login import UserMixin
from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from itsdangerous import URLSafeSerializer
from app.utils import AbstractHashID
from app.auth import login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta


class User(db.Model, DefaultTableMixin, UserMixin):
    """
    User Model Class
    """
    __tablename__ = 'users'
    email = db.Column(db.String(240), unique=True, nullable=False)
    password = deferred(db.Column(db.String(240), nullable=False))
    user_status = db.Column(db.Boolean, default=False)
    details = db.relationship('UserDetails', backref='user', lazy=True)
    token_provider = db.Column(db.String(30), default='local')
    token = db.relationship('OAuth2Token', backref='user', uselist=False,
                            lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.email)

    @property
    def hash_id(self):
        if self.id:
            return UserIDHash.encode(self.id)
        else:
            return None

    def set_password(self, password):
        """
        Set user password. This function takes care of the password hashing.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the given password matches with user password on the database.
        """
        return check_password_hash(self.password, password)

    def set_random_password(self):
        """
        Set random password to user.
        """
        self.set_password(str(uuid4()))

    @property
    def is_active(self):
        """
        Return the status of the user account.
        return type: bool.
        """
        return self.user_status

    def get_id(self):
        """
        obfuscated user info generated with user id and password.
        """
        s = URLSafeSerializer(getenv('USERS_SALT'))
        return str(s.dumps([self.id, self.password]))

    @classmethod
    def by_email_address(cls, email_id):
        return cls.query.filter_by(email=email_id).first()

    @property
    def info(self):
        """
        Get user details.
        rtype:  (class)_UserDetailsHandler.
        """
        return _UserDetailsHandler(self, self.details)

    def add_or_update_token(self, name, token):
        """
        Add or update user token.
        """
        if self.token_provider == 'local' or self.token_provider != name:
            return False

        if not self.token:
            self.token = OAuth2Token()

        user_token = self.token

        if token.get('refresh_token'):
            user_token.refresh_token = token['refresh_token']

        user_token.token_type = token['token_type']
        user_token.access_token = token['access_token']
        user_token.expires_at = token['expires_in']

        return self.commit_changes()


class UserDetails(db.Model, DefaultTableMixin):
    """
    User Details.
    """
    __tablename__ = 'user_details'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    key = db.Column(db.String(240), nullable=False)
    value = db.Column(db.String(240), default=None)


class OAuth2Token(db.Model, DefaultTableMixin):
    """
    User Oauth2 tokens
    """
    __tablename__ = 'oauth2_tokens'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False, unique=True)
    token_type = db.Column(db.String(50))
    access_token = db.Column(db.String(240), nullable=False)
    refresh_token = db.Column(db.String(240))
    _expires_at = db.Column(db.DateTime, nullable=False)

    def to_token(self):
        """
        Get user token.
        rtype: dict
        """
        return {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'refresh_token': self.refresh_token,
            'expires_in': int(self.expires_at_in_sec)
        }

    @hybrid_property
    def expires_at(self):
        return self._expires_at

    @expires_at.setter
    def expires_at(self, in_seconds=0):
        expires_in = int(in_seconds)
        self._expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    @property
    def expires_at_in_sec(self):
        return (datetime.utcnow() - self.expires_at).seconds


class _UserDetailsHandler():
    """
    Class used internally by User model to
    handle operations on user details.
    """
    def __init__(self, user, details):
        self.__user = user
        self.__user_details = details
        self.__data = {}

        for x in self.__user_details:
            self.__data[x.key] = x.value

    def all(self):
        """
        Get User details as a dictionary of key, value
        """
        return self.__data

    def get(self, key):
        """
        Get value from user_details table key.
        """
        return self.__data.get(key)

    def put(self, key, value=None):
        """
        Add or Update a row in user_details table.
        """
        updated = False

        for x in self.__user_details:
            if x.key == key:
                x.value = value
                updated = True

        if not updated:
            new_info = UserDetails()
            new_info.key = key
            new_info.value = value

            self.__user.details.append(new_info)

        return self.__user.commit_changes()

    def delete(self, key):
        for x in self.__user_details:
            if x.key == key:
                db.session.delete(x)

        return self.__user.commit_changes()


class UserIDHash(AbstractHashID):
    salt = getenv('USERS_SALT')
    min_length = 7


@login_manager.user_loader
def load_user(user_id):
    """
    User loader for flask login.
    """
    s = URLSafeSerializer(getenv('USERS_SALT'))
    try:
        user = s.loads(user_id)
        return User.get(user[0])
    except Exception:
        return None


def create_oauth_user(user_id, name):
    """
    Create a new oauth user
    """
    user_email = '{}@{}'.format(str(user_id), name)
    new_user = User(email=user_email, user_status=True, token_provider=name)
    new_user.set_random_password()

    db.session.add(new_user)

    try:
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
