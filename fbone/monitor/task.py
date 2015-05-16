# coding: utf-8
from ..extensions import db, mail, login_manager, oid, celery
from ..monitor import Monitor, Tokens

@celery.task
def get_github_data():
    tokens = Tokens.query.filter_by(datatype='coding')
    for token in tokens:
        pass

@celery.task
def get_health_data():
    tokens = Tokens.query.filter_by(datatype='health')
    for token in tokens:
        pass

@celery.task
def get_webtimer_data():
    tokens = Tokens.query.filter_by(datatype='webtimer')
    for token in tokens:
        pass