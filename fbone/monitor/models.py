#coding: utf-8
from sqlalchemy import Column
from ..extensions import db
from ..utils import get_current_time, SEX_TYPE, STRING_LEN

class Monitor(db.Model):

    # __tablename__ = 'monitors'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), default='')
    url = Column(db.String(50), default='')
    introduction = Column(db.String(100), default='')
    created = Column(db.DateTime, default=get_current_time)


token = db.Table('tokens',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('monitor_id', db.Integer, db.ForeignKey('monitor.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('token', db.String(80))
)
