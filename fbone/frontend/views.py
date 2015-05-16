# -*- coding: utf-8 -*-

from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify)
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..user import User, UserDetail
from ..monitor import Monitor, Tokens
from ..extensions import db, mail, login_manager, oid, celery
from .forms import SignupForm, LoginForm, RecoverPasswordForm, ReauthForm, ChangePasswordForm, OpenIDForm, CreateProfileForm
import requests
import json
import base64

frontend = Blueprint('frontend', __name__)


@celery.task
def add_num(a,b):
    print a+b
    return a+b



@frontend.route('/login/openid', methods=['GET', 'POST'])
@oid.loginhandler
def login_openid():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = OpenIDForm()
    if form.validate_on_submit():
        openid = form.openid.data
        current_app.logger.debug('login with openid(%s)...' % openid)
        return oid.try_login(openid, ask_for=['email', 'fullname', 'nickname'])
    return render_template('frontend/login_openid.html', form=form, error=oid.fetch_error())


@oid.after_login
def create_or_login(resp):
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user and login_user(user):
        flash('Logged in', 'success')
        return redirect(oid.get_next_url() or url_for('user.index'))
    return redirect(url_for('frontend.create_profile', next=oid.get_next_url(),
            name=resp.fullname or resp.nickname, email=resp.email,
            openid=resp.identity_url))


@frontend.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = CreateProfileForm(name=request.args.get('name'),
            email=request.args.get('email'),
            openid=request.args.get('openid'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        if login_user(user):
            return redirect(url_for('user.index'))

    return render_template('frontend/create_profile.html', form=form)


@frontend.route('/')
def index():
    current_app.logger.debug('debug')

    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    page = int(request.args.get('page', 1))
    pagination = User.query.paginate(page=page, per_page=10)
    return render_template('index.html', pagination=pagination)


@frontend.route('/search')
def search():
    keywords = request.args.get('keywords', '').strip()
    pagination = None
    if keywords:
        page = int(request.args.get('page', 1))
        pagination = User.search(keywords).paginate(page, 1)
    else:
        flash(_('Please input keyword(s)'), 'error')
    return render_template('frontend/search.html', pagination=pagination, keywords=keywords)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):
                flash(_("Logged in"), 'success')
            return redirect(form.next.data or url_for('user.index'))
        else:
            flash(_('Sorry, invalid login'), 'error')

    return render_template('frontend/login.html', form=form)

@frontend.route('/<monitor_name>/callback', methods=['GET', 'POST'])
def callback(monitor_name):
    if monitor_name == 'github':
        code = request.args.get('code', None)
        print code
        params = {
                'client_id': 'e925ef871d26e063315b',
                'redirect_uri': 'http://106.186.117.185:5555/github/callback',
                'client_secret': 'aff83393a739a9d84c72b723c566c0e6366f887f',
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

        if not db.session.query(User).filter_by(name=username).all():
            print 'no user'
            user = User(name=username, email=email, avatar=avatar_url)
            db.session.add(user)
            db.session.commit()

        user_one = db.session.query(User).filter_by(name=username).first()

        mytooken = Tokens.query.filter_by(monitor_id=5, user_id=2, datatype='coding').first()
        if not mytooken:
            token = Tokens(monitor_id=5, user_id=2, datatype='coding', token=token)
            db.session.add(token)
            db.session.commit()
        if login_user(user_one):
            flash("Logged in", 'success')

        add_num.delay(2,3)

        return redirect(url_for('user.index'))
    elif monitor_name == 'fitbit':
        code = request.args.get('code', None)
        print code
        params = {
                'client_id': '229NZW',
                'redirect_uri': 'http://106.186.117.185:5555/fitbit/callback',
                'grant_type': 'authorization_code',
                'code': code
            }
        base_str = 'Basic %s' % base64.b64encode('229NZW:018285a1459844c082e9e0711328bd66')
        headers = {
            'Authorization': base_str,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = 'https://api.fitbit.com/oauth2/token'
        req = requests.post(url=url, headers=headers, params=params)
        resp_json = json.loads(req.content)

        token = resp_json['access_token']
        mytooken = Tokens.query.filter_by(monitor_id=3, user_id=2, datatype='health').first()
        if mytooken:
            mytooken.token = token
        else:
            mytooken = Tokens(monitor_id=3, user_id=2, datatype='health', token=token)
            db.session.add(mytooken)
        db.session.commit()

        refresh_token = resp_json['refresh_token']
        profile_url = 'https://api.fitbit.com/1/user/-/profile.json'
        actvity_url = 'https://api.fitbit.com/1/user/-/activities/date/2015-04-21.json'
        food_url = 'https://api.fitbit.com/1/user/-/foods/log/date/2015-04-22.json'
        body_url = 'https://api.fitbit.com/1/user/-/body/date/2015-04-22.json'
        actvity_stat_url = 'https://api.fitbit.com/1/user/-/activities.json'
        auth_str = 'Bearer %s' % token
        print '********'
        print auth_str
        print len(auth_str)
        print '********'
        headers_json = {'Authorization':auth_str}
        # r = requests.get(profile_url, headers=headers_json)
        # r = requests.get(actvity_url, headers=headers_json)
        # r = requests.get(food_url, headers=headers_json)
        # r = requests.get(body_url, headers=headers_json)
        r = requests.get(actvity_stat_url, headers=headers_json)

        user_json = json.loads(r.content)

        # print user_json

        add_num.delay(3,2)

        return jsonify(user_json)
    else:
        return 'other'



@frontend.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    form = ReauthForm(next=request.args.get('next'))

    if request.method == 'POST':
        user, authenticated = User.authenticate(current_user.name,
                                    form.password.data)
        if user and authenticated:
            confirm_login()
            current_app.logger.debug('reauth: %s' % session['_fresh'])
            flash(_('Reauthenticated.'), 'success')
            return redirect('/change_password')

        flash(_('Password is wrong.'), 'error')
    return render_template('frontend/reauth.html', form=form)


@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('frontend.index'))


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))

    form = SignupForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        user.user_detail = UserDetail()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        if login_user(user):
            return redirect(form.next.data or url_for('user.index'))

    return render_template('frontend/signup.html', form=form)


@frontend.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = None
    if current_user.is_authenticated():
        if not login_fresh():
            return login_manager.needs_refresh()
        user = current_user
    elif 'activation_key' in request.values and 'email' in request.values:
        activation_key = request.values['activation_key']
        email = request.values['email']
        user = User.query.filter_by(activation_key=activation_key) \
                         .filter_by(email=email).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():
        user.password = form.password.data
        user.activation_key = None
        db.session.add(user)
        db.session.commit()

        flash(_("Your password has been changed, please log in again"),
              "success")
        return redirect(url_for("frontend.login"))

    return render_template("frontend/change_password.html", form=form)


@frontend.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Please see your email for instructions on '
                  'how to access your account', 'success')

            user.activation_key = str(uuid4())
            db.session.add(user)
            db.session.commit()

            url = url_for('frontend.change_password', email=user.email, activation_key=user.activation_key, _external=True)
            html = render_template('macros/_reset_password.html', project=current_app.config['PROJECT'], username=user.name, url=url)
            message = Message(subject='Reset your password in ' + current_app.config['PROJECT'], html=html, recipients=[user.email])
            mail.send(message)

            return render_template('frontend/reset_password.html', form=form)
        else:
            flash(_('Sorry, no user found for that email address'), 'error')

    return render_template('frontend/reset_password.html', form=form)


@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")
