# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from ..extensions import db
from ..utils import get_current_time, SEX_TYPE, STRING_LEN
from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS
# from ..monitor import Monitor, token

class DenormalizedText(Mutable, types.TypeDecorator):
    """
    Stores denormalized primary keys that can be
    accessed as a set.

    :param coerce: coercion function that ensures correct
                   type is returned

    :param separator: separator character
    """

    impl = types.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):

        self.coerce = coerce
        self.separator = separator

        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return set()
        return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)


class UserDetail(db.Model):

    # __tablename__ = 'user_details'

    id = Column(db.Integer, primary_key=True)

    age = Column(db.Integer)
    phone = Column(db.String(STRING_LEN))
    url = Column(db.String(STRING_LEN))
    deposit = Column(db.Numeric)
    location = Column(db.String(STRING_LEN))
    bio = Column(db.String(STRING_LEN))

    sex_code = db.Column(db.Integer)

    @property
    def sex(self):
        return SEX_TYPE.get(self.sex_code)

    created_time = Column(db.DateTime, default=get_current_time)


class User(db.Model, UserMixin):

    # __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = Column(db.String(STRING_LEN), nullable=True, unique=True)
    openid = Column(db.String(STRING_LEN), unique=True)
    activation_key = Column(db.String(STRING_LEN))
    created_time = Column(db.DateTime, default=get_current_time)

    avatar = Column(db.String(STRING_LEN))

    _password = Column('password', db.String(70), nullable=True)
    monitor_values = db.relationship('MonitorValue', backref = 'user', lazy = 'dynamic')

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password', descriptor=property(_get_password,  _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    # # ================================================================
    role_code = Column(db.SmallInteger, default=USER, nullable=True)
    # tokens = db.relationship('Monitor', secondary=token, backref=db.backref('user', lazy='dynamic'))
    

    def is_admin(self):
        return self.role_code == ADMIN


    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated
