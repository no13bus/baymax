# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.user import User, UserDetail, ADMIN, ACTIVE
from fbone.monitor import Monitor
from fbone.utils import MALE


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run(host='0.0.0.0', port=5555)


@manager.command
def initdb():
    """Init/reset database."""
    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'admin123',
            role_code=ADMIN,
            status_code=ACTIVE,
            )

    # admin = User(
    #         name=u'admin',
    #         email=u'admin@example.com')
    # monitor = Monitor(name='nike', url='nike.com', introduction='famous sport company')
    db.session.add(admin)
    # db.session.add(monitor)
    db.session.commit()

@manager.command
def drop():
    db.drop_all()

@manager.command
def insert():
    # software
    m1 = Monitor(name='nike', url='http://dev.nike.com/', introduction='nike plus api')
    m2 = Monitor(name='rescuetime', url='https://www.rescuetime.com/developers', introduction='track your internet')
    m3 = Monitor(name='fitbit', url='https://dev.fitbit.com/', introduction='fitbit health')
    m4 = Monitor(name='withings', url='http://oauth.withings.com/api', introduction='withings health')
    m5 = Monitor(name='github', url='https://developer.github.com/', introduction='source code social network')
    m6 = Monitor(name='weibo', url='http://open.weibo.com/', introduction='twitter copy to china')
    # hardware ......
    m7 = Monitor(name='bong', url='http://www.bong.cn/share/', introduction='bong bracelet')
    m8 = Monitor(name='xiaomi', url='https://github.com/stormluke/Mili-iOS', introduction='xiaomi bracelet')

    db.session.add(m1)
    db.session.add(m2)
    db.session.add(m3)
    db.session.add(m4)
    db.session.add(m5)
    db.session.add(m6)
    db.session.add(m7)
    db.session.add(m8)
    db.session.commit()

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
