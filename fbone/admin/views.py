# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User
from ..monitor import Monitor
from .forms import UserForm


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')

@admin.route('/monitors')
@login_required
@admin_required
def monitors():
    monitors = Monitor.query.all()
    return render_template('admin/monitors.html', monitors=monitors, active='monitors')

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    # 这个地方完全是form和模型一起绑定的。注意下。obj就是个说明
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('User updated.', 'success')

    return render_template('admin/user.html', user=user, form=form)

@admin.route('/monitor/<int:monitor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def monitor(monitor_id):
    monitor = Monitor.query.filter_by(id=monitor_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('User updated.', 'success')

    return render_template('admin/user.html', user=user, form=form)
