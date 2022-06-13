# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from ..utils import get_current_time, SEX_TYPE, STRING_LEN


class User(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = Column(db.String(STRING_LEN), nullable=True, unique=True)
    created_time = Column(db.DateTime, default=get_current_time)
    avatar = Column(db.String(STRING_LEN), default='')
    monitor_values = db.relationship('MonitorValue', backref='user', lazy='dynamic')

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    # def is_admin(self):
    #     return self.role_code == ADMIN

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated
