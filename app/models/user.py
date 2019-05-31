from app.database import db, DefaultTableMixin
from flask_login import UserMixin
from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from itsdangerous import URLSafeSerializer
from flask import current_app
from app.utils import AbstractHashID
from app.auth import login_manager


class User(db.Model, DefaultTableMixin, UserMixin):
    """
    User Model Class
    """
    __tablename__ = 'users'
    email = db.Column(db.String(240), unique=True, nullable=False)
    password = deferred(db.Column(db.String(240), nullable=False))
    user_status = db.Column(db.Boolean, default=False)
    details = db.relationship('UserDetails', backref='user', lazy=True)

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
        s = URLSafeSerializer(current_app.config['USERS_SALT'])
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

    @classmethod
    def hash(cls):
        secret = current_app.config['USERS_SALT']
        return cls.hash_provider(secret, 7)


@login_manager.user_loader
def load_user(user_id):
    s = URLSafeSerializer(current_app.config['USERS_SALT'])
    try:
        user = s.loads(user_id)
        return User.get(user[0])
    except Exception:
        return None
