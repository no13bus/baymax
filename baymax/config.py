# -*- coding: utf-8 -*-

import os
from datetime import timedelta
from utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):

    PROJECT = "baymax"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['youremail@yourdomain.com']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'huihfiushdfy8shfurh7s8gibejhr387y98y8**&%'

    # LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)

    # Fild upload, should override in production.
    # Limited the maximum allowed payload to 16 megabytes.
    # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'uploads')
    make_dir(UPLOAD_FOLDER)


class DefaultConfig(BaseConfig):

    DEBUG = True
    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = False
    echo=True
    # SQLITE for prototyping.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # MYSQL for production.
    #SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/baymax?charset=utf8'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['zh']
    BABEL_DEFAULT_LOCALE = 'en'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-mail: http://pythonhosted.org/flask-mail/
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # Should put MAIL_USERNAME and MAIL_PASSWORD in production under instance folder.
    MAIL_USERNAME = 'yourmail@gmail.com'
    MAIL_PASSWORD = 'yourpass'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Flask-openid: http://pythonhosted.org/Flask-OpenID/
    OPENID_FS_STORE_PATH = os.path.join(INSTANCE_FOLDER_PATH, 'openid')
    make_dir(OPENID_FS_STORE_PATH)

    # flask-rq
    # RQ_DEFAULT_HOST = 'localhost'
    # RQ_DEFAULT_PORT = 6379
    # RQ_DEFAULT_PASSWORD = None
    # RQ_DEFAULT_DB = 1

    # celery
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERYBEAT_SCHEDULE = {
    'baymax_rescuetime': {
        'task': 'baymax.monitor.task.rescuetime_task',
        'schedule': timedelta(seconds=3600*24)
        },
    'baymax_github': {
        'task': 'baymax.monitor.task.github_task',
        'schedule': timedelta(seconds=3600*24)
        },
    'baymax_fitbit': {
        'task': 'baymax.monitor.task.fitbit_task',
        'schedule': timedelta(seconds=3600*24)
        }
    }

    CALLBACK_URL = 'http://baymax.ninja/%s/callback'
    # github api
    GITHUB_KEY = ''
    GITHUB_SECRET = ''
    # fitbit
    FITBIT_KEY = ''
    FITBIT_SECRET = ''




class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
