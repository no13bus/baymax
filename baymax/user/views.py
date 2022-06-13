# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort
from flask import current_app as APP
from flask_login import login_required, current_user
from .models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/')
@login_required
def index():
    if not current_user.is_authenticated:
        abort(403)
    return render_template('user/index.html', user=current_user)
