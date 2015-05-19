# coding: utf-8
import requests
import json
import datetime
from itertools import groupby

API_URL = 'https://api.github.com'

class GitHub(object):
    def __init__(self, token, username):
        self.token = token
        self.username = username

    def get_datas(self):
        url = '%s/users/%s/events?page=1&per_page=100&access_token=%s' % (API_URL, self.username, self.token)
        r = requests.get(url)
        j = json.loads(r.content)
        def group_key(s):
            time_str = datetime.datetime.strptime(s['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
            return time_str
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        j = [i for i in j if i['type'] == 'PushEvent' and datetime.datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') < now]
        res = []
        for key,valuesiter in groupby(j, key=group_key):
            res.append((key, len(list(valuesiter))))
        return res
    # start_day: 2015-05-01 数据库内最新的时间
    def get_data(self, start_day):
        now_time_str = datetime.datetime.now().strftime('%Y-%m-%d')
        url = '%s/users/%s/events?page=1&per_page=100&access_token=%s' % (API_URL, self.username, self.token)
        r = requests.get(url)
        j = json.loads(r.content)
        def group_key(s):
            time_str = datetime.datetime.strptime(s['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
            return time_str
        j = [i for i in j if i['type'] == 'PushEvent' and i['created_at'].split('T')[0] < now_time_str]
        res = []
        for key,valuesiter in groupby(j, key=group_key):
            if start_day < key:
                res.append((key, len(list(valuesiter))))
            else:
                break
        return res

