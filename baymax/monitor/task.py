#coding: utf-8
import datetime
from .models import Tokens, MonitorValue
from ..user import User
from ..extensions import celery, db
from ..libs.github import GitHub
from ..libs.fitbit import Fitbit
from ..libs.rescuetime import RescueTime


@celery.task
def rescuetime_task_func(token, username):
    user = User.query.filter_by(name=username).first()
    rescue_time = RescueTime(token)
    datas = rescue_time.get_datas()
    for data in datas:
        recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
        mv_communication_and_scheduling = MonitorValue(value=data['communication_and_scheduling'], datatype='communication_and_scheduling', recode_date=recode_date, user_id=user.id)
        mv_software_development = MonitorValue(value=data['software_development'], datatype='software_development', recode_date=recode_date, user_id=user.id)
        mv_news = MonitorValue(value=data['news'], datatype='news', recode_date=recode_date, user_id=user.id)
        mv_entertainment = MonitorValue(value=data['entertainment'], datatype='entertainment', recode_date=recode_date, user_id=user.id)
        db.session.add(mv_communication_and_scheduling)
        db.session.add(mv_software_development)
        db.session.add(mv_news)
        db.session.add(mv_entertainment)
    db.session.commit()

# 每天中午更新一次
@celery.task
def rescuetime_task():
    tokens = Tokens.query.filter_by(datatype='webtimer').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='communication_and_scheduling', user_id=token.user_id).order_by('recode_date desc').first()
        rescue_time = RescueTime(token.token)
        if not one_mv:
            datas = rescue_time.get_datas()
            for data in datas:
                recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                mv_communication_and_scheduling = MonitorValue(value=data['communication_and_scheduling'], datatype='communication_and_scheduling', recode_date=recode_date, user_id=token.user_id)
                mv_software_development = MonitorValue(value=data['software_development'], datatype='software_development', recode_date=recode_date, user_id=token.user_id)
                mv_news = MonitorValue(value=data['news'], datatype='news', recode_date=recode_date, user_id=token.user_id)
                mv_entertainment = MonitorValue(value=data['entertainment'], datatype='entertainment', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_communication_and_scheduling)
                db.session.add(mv_software_development)
                db.session.add(mv_news)
                db.session.add(mv_entertainment)
            db.session.commit()
        else:
            data = rescue_time.get_data()
            recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
            mv_communication_and_scheduling = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='communication_and_scheduling').first()
            mv_software_development = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='software_development').first()
            mv_news = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='news').first()
            mv_entertainment = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='entertainment').first()
            if not mv_communication_and_scheduling:
                recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                mv = MonitorValue(value=data['communication_and_scheduling'], datatype='communication_and_scheduling', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv)

            if not mv_software_development:
                recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                mv_software_development = MonitorValue(value=data['software_development'], datatype='software_development', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_software_development)

            if not mv_news:
                recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                mv_news = MonitorValue(value=data['news'], datatype='news', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_news)

            if not mv_entertainment:
                recode_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                mv_entertainment = MonitorValue(value=data['entertainment'], datatype='entertainment', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_entertainment)
            db.session.commit()

@celery.task
def github_task_func(token, username):
    user = User.query.filter_by(name=username).first()
    github = GitHub(token, username)
    datas = github.get_datas()
    for data in datas:
        recode_date, value = data
        recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
        mv = MonitorValue(value=value, datatype='coding', recode_date=recode_date, user_id=user.id)
        db.session.add(mv)
    db.session.commit()



@celery.task
def github_task():
    tokens = Tokens.query.filter_by(datatype='coding').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='coding', user_id=token.user_id).order_by('recode_date desc').first()
        user = User.query.filter_by(id=token.user_id).first()
        github = GitHub(token.token, user.name)
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
def fitbit_task_func(token, username):
    user = User.query.filter_by(name=username).first()
    fitbit = Fitbit(token)
    datas = fitbit.get_steps_datas()
    for data in datas:
        steps, calories_out, distance, recode_date = data['steps'], data['calories_out'], data['distance'], data['date']
        recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
        mv_steps = MonitorValue(value=steps, datatype='steps', recode_date=recode_date, user_id=user.id)
        mv_calories_out = MonitorValue(value=calories_out, datatype='calories_out', recode_date=recode_date, user_id=user.id)
        mv_distance = MonitorValue(value=distance, datatype='distance', recode_date=recode_date, user_id=user.id)
        db.session.add(mv_steps)
        db.session.add(mv_calories_out)
        db.session.add(mv_distance)
    db.session.commit()

@celery.task
def fitbit_task():
    tokens = Tokens.query.filter_by(datatype='health').all()
    for token in tokens:
        one_mv = MonitorValue.query.filter_by(datatype='steps', user_id=token.user_id).order_by('recode_date desc').first()
        # update token
        user_token, user_refresh_token = Fitbit.get_refresh_token(token.token, token.refresh_token)
        token.token = user_token
        token.refresh_token = user_refresh_token
        db.session.commit()
        fitbit = Fitbit(token.token)
        if not one_mv:
            datas = fitbit.get_steps_datas()
            if not datas:
                continue
            for data in datas:
                steps, calories_out, distance, recode_date = data['steps'], data['calories_out'], data['distance'], data['date']
                recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
                mv_steps = MonitorValue(value=steps, datatype='steps', recode_date=recode_date, user_id=token.user_id)
                mv_calories_out = MonitorValue(value=calories_out, datatype='calories_out', recode_date=recode_date, user_id=token.user_id)
                mv_distance = MonitorValue(value=distance, datatype='distance', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_steps)
                db.session.add(mv_calories_out)
                db.session.add(mv_distance)
            db.session.commit()
        else:
            data = fitbit.get_steps_data()
            if not data:
                continue
            steps, calories_out, distance, recode_date = data['steps'], data['calories_out'], data['distance'], data['date']
            recode_date = datetime.datetime.strptime(recode_date, '%Y-%m-%d')
            mv_steps = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='steps').first()
            mv_calories_out = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='calories_out').first()
            mv_distance = MonitorValue.query.filter_by(recode_date=recode_date, user_id=token.user_id, datatype='distance').first()
            if not mv_steps:
                mv_steps_one = MonitorValue(value=steps, datatype='steps', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_steps_one)
            if not mv_calories_out:
                mv_calories_out_one = MonitorValue(value=calories_out, datatype='calories_out', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_calories_out_one)
            if not mv_distance:
                mv_distance_one = MonitorValue(value=distance, datatype='distance', recode_date=recode_date, user_id=token.user_id)
                db.session.add(mv_distance_one)
            db.session.commit()


# refresh_token = resp_json['refresh_token']
# profile_url = 'https://api.fitbit.com/1/user/-/profile.json'
# actvity_url = 'https://api.fitbit.com/1/user/-/activities/date/2015-04-21.json'
# food_url = 'https://api.fitbit.com/1/user/-/foods/log/date/2015-04-22.json'
# body_url = 'https://api.fitbit.com/1/user/-/body/date/2015-04-22.json'
# actvity_stat_url = 'https://api.fitbit.com/1/user/-/activities.json'
# auth_str = 'Bearer %s' % token
# headers_json = {'Authorization':auth_str}
# r = requests.get(actvity_stat_url, headers=headers_json)
# user_json = json.loads(r.content)