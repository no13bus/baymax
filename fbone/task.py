#coding: utf-8
import datetime
from .monitor import Tokens, MonitorValue
from .user import User
from .extensions import celery, db
from .libs.github import GitHub
from .libs.fitbit import Fitbit
from .libs.rescuetime import RescueTime


# 每天中午更新一次
@celery.task
def rescuetime_task():
    tokens = Tokens.query.filter_by(datatype='webtimer').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='webtimer', user_id=token.user_id).order_by('recode_date desc').first()
        rescue_time = RescueTime(token.token)
        if not one_mv:
            datas = rescue_time.get_datas()
            for data in datas:
                recode_date = datetime.datetime.strptime(data['data'], '%Y-%m-%d')
                mv = MonitorValue(value=data['communication_and_scheduling'], datatype='communication_and_scheduling_time', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv)
            db.session.commit()
        else:
            data = rescue_time.get_data()[0]
            recode_date = datetime.datetime.now() - datetime.timedelta(days=1)
            mv = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='communication_and_scheduling_time').first()
            if not mv:
                recode_date = datetime.datetime.strptime(data['data'], '%Y-%m-%d')
                mv = MonitorValue(value=data['communication_and_scheduling'], datatype='communication_and_scheduling_time', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv)
                db.session.commit()

@celery.task
def github_task():
    tokens = Tokens.query.filter_by(datatype='coding').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='coding', user_id=token.user_id).order_by('recode_date desc').first()
        user = User.query.filter_by(id=token.user_id)
        github = GitHub(token, user.name)
        if not one_mv:
            datas = github.get_datas()
            for data in datas:
                recode_date, value = data
                recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
                mv = MonitorValue(value=value, datatype='coding', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv)
            db.session.commit()
        else:
            start_day = one_mv.recode_date.strftime('%Y-%m-%d')
            data = github.get_data(start_day=start_day)
            if not data:
                continue
            recode_date, value = data[0]
            recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
            mv = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='coding').first()
            if not mv:
                mv = MonitorValue(value=value, datatype='coding', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv)
                db.session.commit()

@celery.task
def fitbit_task():
    tokens = Tokens.query.filter_by(datatype='health').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='steps', user_id=token.user_id).order_by('recode_date desc').first()
        fitbit = Fitbit(token.token)
        if not one_mv:
            datas = fitbit.get_steps_datas()
            if not datas:
                continue
            for data in datas:
                steps, calories_out, distance, recode_date = data['steps'], data['calories_out'], data['distance'], data['recode_date']
                recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
                mv_steps = MonitorValue(value=steps, datatype='steps', recode_date=recode_date, user_id=token.user_id)
                mv_water = MonitorValue(value=water, datatype='water', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_calories_in)
                db.session.add(mv_water)
            db.session.commit()
        else:
            data = fitbit.get_calories_water_data()
            if not data:
                continue
            calories_in, water, recode_date = data['calories_in'], data['water'], data['recode_date']
            recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
            mv_calories_in = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='calories_in').first()
            mv_water = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='water').first()
            if not mv_calories_in:
                mv_calories_in_one = MonitorValue(value=calories_in, datatype='calories_in', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_calories_in_one)
            if not mv_water:
                mv_water_one = MonitorValue(value=water, datatype='water', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_water_one)
            db.session.commit()


















