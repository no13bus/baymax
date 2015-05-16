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

class Tokens(db.Model):

    # __tablename__ = 'tokens'
    id = Column(db.Integer, primary_key=True)
    monitor_id = Column(db.Integer, db.ForeignKey('monitor.id'))
    user_id = Column(db.Integer, db.ForeignKey('user.id'))
    token = Column(db.String(300))
    datatype = Column(db.String(20))
    name = Column(db.String(20))
    created = Column(db.DateTime, default=get_current_time)

class MonitorValue(db.Model):
    id = Column(db.Integer, primary_key=True)
    value = Column(db.Float(20), default=0.0)
    datatype = Column(db.String(20)) # datatype 这个的值应该是steps water weight等等 或者是github的commit数量
    recode_date = Column(db.DateTime, default=get_current_time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = Column(db.DateTime, default=get_current_time)
#
#
# token = db.Table('tokens',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('monitor_id', db.Integer, db.ForeignKey('monitor.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('token', db.String(80)),
#     db.Column('datatype', db.String(20))
# )