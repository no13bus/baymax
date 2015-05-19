# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask.ext.login import current_user, login_required
from ..user import User
from ..monitor import MonitorValue


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/<monitor_type>', methods=['GET'])
@login_required
def calories_out(monitor_type):
    res = []
    user_id = current_user.id
    mv = MonitorValue.query.filter_by(user_id=user_id, datatype=monitor_type).order_by('recode_date desc').limit(7).all()
    if not mv:
        return jsonify(result=[])
    for one_mv in mv[::-1]:
        res.append([one_mv.recode_date.strftime('%Y-%m-%d'), one_mv.value])
    return jsonify(result=res)

@api.route('/user/<username>/<monitor_type>', methods=['GET'])
def api_data(username, monitor_type):
    res = []
    user = User.query.filter_by(name=username).first()
    user_id = user.id
    mv = MonitorValue.query.filter_by(user_id=user_id, datatype=monitor_type).order_by('recode_date desc').limit(7).all()
    if not mv:
        return jsonify(result=[])
    for one_mv in mv[::-1]:
        res.append([one_mv.recode_date.strftime('%Y-%m-%d'), one_mv.value])
    return jsonify(result=res)

