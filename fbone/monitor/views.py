# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime

from flask import Blueprint, render_template, current_app, request, flash, abort, redirect, url_for
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..user import User
from ..utils import allowed_file, make_dir
from .models import Monitor, Tokens
from .forms import RescuetimeForm
from ..libs import FitbitAuth, FitbitApi

monitor = Blueprint('monitor', __name__, url_prefix='/monitor')

@monitor.route('/', methods=['GET', 'POST'])
@login_required
def list():
    monitors = Monitor.query.all()
    return render_template('monitor/list.html', active='monitor_list', monitors=monitors)

# B63QS4V5Rydzx7rlvIcLuCFeAxruuA5g039Kh7Zh
@monitor.route('/<monitor_name>', methods=['GET', 'POST'])
@login_required
def detail(monitor_name):
    if monitor_name == 'rescuetime':
        form = RescuetimeForm()
        if form.validate_on_submit():
            print form.key.data
            mytooken = Tokens.query.filter_by(monitor_id=2, user_id=2, datatype='webtimer').first()
            if mytooken:
                mytooken.token = form.key.data
            else:
                token = Tokens(monitor_id=2, user_id=2, token=str(form.key.data), datatype='webtimer')
                db.session.add(token)
            db.session.commit()
            return 'form data'
        return render_template('monitor/detail.html', form=form)
    elif monitor_name == 'fitbit':
        # auth = FitbitAuth('0ad642de85bc4e30a5c1e0aca8ec8355', '018285a1459844c082e9e0711328bd66')
        # authorize_url = auth.get_authorize_url()
        authorize_url = 'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=229NZW&redirect_uri=http%3A%2F%2F106.186.117.185%3A5555%2Ffitbit%2Fcallback&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight'

        print authorize_url
        return redirect(authorize_url)
    else:
        return render_template('monitor/detail.html', form=None)
