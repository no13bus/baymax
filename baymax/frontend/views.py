# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify)
from flask_login import login_required, login_user, current_user, logout_user
from ..user import User
from ..monitor import Tokens
from ..extensions import db
from ..monitor import github_task_func, fitbit_task_func
import requests
import json
import base64


frontend = Blueprint('frontend', __name__)

@frontend.route('/<username>/show', methods=['GET'])
def user_show(username):
    user = User.query.filter_by(name=username).first()
    avatar = user.avatar
    return render_template('frontend/show.html', active='show', avatar=avatar, username=username)


@frontend.route('/show', methods=['GET', 'POST'])
@login_required
def show():
    avatar = session.get('avatar','')
    return render_template('frontend/show.html', active='show', avatar=avatar)

@frontend.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.show'))
    monitors = ['rescuetime', 'fitbit', 'github', 'nike', 'argus', 'bong', 'ledongli', 'moves', 'uber', 'withings']
    return render_template('index.html', monitors=monitors)

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.show'))
    next=request.args.get('next', None)
    redirect_uri = current_app.config.get('CALLBACK_URL') % 'github'
    oauth_url = 'https://github.com/login/oauth/authorize?redirect_uri=%s?next=%s&client_id=e925ef871d26e063315b' % (redirect_uri, next)
    return redirect(oauth_url)


@frontend.route('/<monitor_name>/callback', methods=['GET', 'POST'])
def callback(monitor_name):
    CALLBACK_URL = current_app.config.get('CALLBACK_URL')
    if monitor_name == 'github':
        code = request.args.get('code', None)
        next=request.args.get('next', None)
        params = {
                'client_id': current_app.config.get('GITHUB_KEY'),
                'redirect_uri': CALLBACK_URL % 'github',
                'client_secret': current_app.config.get('GITHUB_SECRET'),
                'code': code
            }
        url = 'https://github.com/login/oauth/access_token'
        req = requests.post(url=url, headers={'Accept': 'application/json'}, params=params)
        if req.status_code != 200:
            return redirect(url_for('frontend.login'))
        resp_json = json.loads(req.content)
        # get user token
        token = resp_json['access_token']
        req_url = 'https://api.github.com/user?access_token=%s' % token
        r = requests.get(req_url)
        user_json = json.loads(r.content)
        username = user_json['login']
        avatar_url = user_json['avatar_url']
        email = user_json['email'] if user_json['email'] else ''
        if not User.query.filter_by(name=username).first():
            print('no user:%s' % username)
            user = User(name=username, email=email, avatar=avatar_url)
            db.session.add(user)
            db.session.commit()
        user_one = User.query.filter_by(name=username).first()
        user_token = Tokens.query.filter_by(monitor_id=5, user_id=user_one.id, datatype='coding').first()
        if not user_token:
            user_token = Tokens(monitor_id=5, user_id=user_one.id, datatype='coding', token=token, name='github')
            db.session.add(user_token)
            db.session.commit()
            # 初始化爬取 github commit数据
            github_task_func.delay(token, username)
            print('github task start....')
        login_user(user_one)
        session['avatar'] = user_one.avatar
        # if login_user(user_one):
        #     flash("Logged in", 'success')
        return redirect(next or url_for('frontend.show'))
    elif monitor_name == 'fitbit':
        if not current_user.is_authenticated:
            return redirect(url_for('frontend.login'))
        code = request.args.get('code', None)
        params = {
                'client_id': current_app.config.get('FITBIT_KEY'),
                'redirect_uri': CALLBACK_URL % 'fitbit',
                'grant_type': 'authorization_code',
                'code': code
            }
        base_str = 'Basic %s' % base64.b64encode('%s:%s' % (current_app.config.get('FITBIT_KEY'), current_app.config.get('FITBIT_SECRET')))
        headers = {
            'Authorization': base_str,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = 'https://api.fitbit.com/oauth2/token'
        req = requests.post(url=url, headers=headers, params=params)
        resp_json = json.loads(req.content)
        print(resp_json)
        token = resp_json['access_token']
        refresh_token = resp_json['refresh_token']
        print(refresh_token)
        user_token = Tokens.query.filter_by(monitor_id=3, user_id=current_user.id, datatype='health').first()
        if user_token:
            user_token.token = token
            user_token.refresh_token = refresh_token
            db.session.commit()
            flash(u'fitbit权限更新成功', 'success')
        else:
            user_token = Tokens(monitor_id=3, user_id=current_user.id, datatype='health', token=token, refresh_token=refresh_token, name='fitbit')
            db.session.add(user_token)
            db.session.commit()
            # 初始化爬取 fitbit 健康数据
            fitbit_task_func(token, current_user.name)
            print(u'开始爬取fitbit数据')
            flash(u'fitbit权限认证成功', 'success')
        return redirect(url_for('monitor.list'))
    else:
        flash(u'未有此项目权限', 'success')
        return redirect(url_for('monitor.list'))



@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('avatar', None)
    # flash('Logged out', 'success')
    return redirect(url_for('frontend.index'))

@frontend.route('/about')
def about():
    return render_template('frontend/about.html', active='about')

