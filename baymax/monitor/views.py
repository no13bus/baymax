# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, redirect, url_for, session, current_app
from flask_login import login_required, current_user
import urllib
from ..extensions import db
from ..libs.fitbit import Fitbit
from .models import Tokens, Monitor
from .task import rescuetime_task_func
from .forms import RescuetimeForm

monitor = Blueprint('monitor', __name__, url_prefix='/monitor')

@monitor.route('/', methods=['GET', 'POST'])
@login_required
def list():
    res = {'rescuetime':None, 'fitbit':None}
    avatar = session.get('avatar', None)
    user_tokens = Tokens.query.filter_by(user_id=current_user.id).all()
    for item in user_tokens:
        if item.name == 'rescuetime':
            res['rescuetime'] = True
        if item.name == 'fitbit':
            res['fitbit'] = True
    monitors = Monitor.query.filter(Monitor.name!='github').all()
    return render_template('monitor/list.html', res=res, active='monitor', avatar=avatar, monitors=monitors)


@monitor.route('/<monitor_name>', methods=['GET', 'POST'])
@login_required
def detail(monitor_name):
    redirect_uri = current_app.config.get('CALLBACK_URL') % 'github'
    if monitor_name == 'rescuetime':
        form = RescuetimeForm()
        if form.validate_on_submit():
            print(form.key.data)
            user_id = current_user.id
            web_tooken = Tokens.query.filter_by(monitor_id=2, user_id=user_id, datatype='webtimer').first()
            if web_tooken:
                web_tooken.token = form.key.data
                web_tooken.name = 'rescuetime'
                db.session.commit()
                flash(u'recuetime重新权限认证成功', 'success')
            else:
                token = Tokens(monitor_id=2, user_id=user_id, token=str(form.key.data), datatype='webtimer', name='rescuetime')
                db.session.add(token)
                db.session.commit()
                # 初始化爬取 rescuetime的数据
                rescuetime_task_func.delay(str(form.key.data), current_user.name)
                print(u'rescuetime data')
                flash(u'recuetime权限认证成功', 'success')
            return redirect(url_for('monitor.list'))
        return render_template('monitor/detail.html', form=form, active='monitor')
    elif monitor_name == 'fitbit':
        authorize_url = Fitbit.get_auth_url()
        return redirect(authorize_url)
    else:
        flash(u'对不起，目前还未支持该检测项目或者您未将其点亮(赋予权限)', 'warning')
        return redirect(url_for('monitor.list'))
        # return render_template('monitor/detail.html', form=None, active='monitor')