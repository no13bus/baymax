# coding: utf-8
import requests
import json
import urllib
import datetime

API_URL = 'https://api.fitbit.com'
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://baymax.ninja/fitbit/callback'
OAUTH_URL = 'https://www.fitbit.com'


# profile_url = 'https://api.fitbit.com/1/user/-/profile.json'
# actvity_url = 'https://api.fitbit.com/1/user/-/activities/date/2015-04-21.json'
# food_url = 'https://api.fitbit.com/1/user/-/foods/log/date/2015-04-22.json'
# body_url = 'https://api.fitbit.com/1/user/-/body/date/2015-04-22.json'
# actvity_stat_url = 'https://api.fitbit.com/1/user/-/activities.json'

class Fitbit(object):
    def __init__(self, token):
        self.token = token

    def _get_json(self, url):
        auth_str = 'Bearer %s' % self.token
        headers_json = {'Authorization':auth_str}
        r = requests.get(url, headers=headers_json)
        j = json.loads(r.content)
        return j

    @classmethod
    def get_auth_url(cls):
        params = urllib.urlencode({
            'response_type':'code',
            'client_id': CLIENT_ID,
            'redirect_uri':REDIRECT_URI,
            'scope': 'activity nutrition heartrate location profile settings sleep social weight'
        })
        authorize_url = '%s/oauth2/authorize?%s' % (OAUTH_URL, params)
        authorize_url = authorize_url.replace('+', '%20')
        return authorize_url

    def get_calories_water_data(self, last_day=None):
        res = {}
        if not last_day:
            last_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%F')
        food_url = '%s/1/user/-/foods/log/date/%s.json' % (API_URL, last_day)
        j = self._get_json(food_url)
        res['calories_in'] = j['summary']['calories']
        res['water'] = j['summary']['water']
        res['date'] = last_day
        return res

    def get_weight_data(self, last_day=None):
        res = {}
        if not last_day:
            last_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%F')
        actvity_url = '%s/1/user/-/body/date/%s.json' % (API_URL, last_day)
        j = self._get_json(actvity_url)
        if res['weight']:
            res['weight'] = j['body']['weight']
        return res

    def get_steps_data(self, last_day=None):
        res = {}
        if not last_day:
            last_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%F')
        actvity_url = '%s/1/user/-/activities/date/%s.json' % (API_URL, last_day)
        j = self._get_json(actvity_url)
        res['steps'] = j['summary']['steps']
        res['calories_out'] = j['summary']['caloriesOut']
        res['distance'] = j['summary']['distances'][0]['distance']
        res['date'] = last_day
        return res

    #############
    def get_steps_datas(self):
        res = []
        for i in range(1, 8):
            day_now = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%F')
            res.append(self.get_steps_data(day_now))
        return res

    def get_weight_datas(self, last_day=None):
        res = []
        for i in range(1, 8):
            day_now = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%F')
            data = self.get_weight_data(day_now)
            if data:
                res.append(self.get_weight_data(day_now))
        return res

    # recent 5 days data
    def get_calories_water_datas(self):
        res = []
        for i in range(1, 8):
            day_now = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%F')
            res.append(self.get_calories_water_data(day_now))
        return res

    @classmethod
    def get_refresh_token(cls, token, refresh_token):
        url = '%s/oauth2/token' % API_URL
        auth_str = 'Bearer %s' % token
        headers_json = {'Authorization':auth_str, 'Content-Type':'application/x-www-form-urlencoded'}
        data = {
            'grant_type':'refresh_token',
            'refresh_token':refresh_token,
            'client_secret':CLIENT_SECRET,
            'client_id':CLIENT_ID
        }
        r = requests.post(url, data=data, headers=headers_json)
        j = json.loads(r.content)
        user_token = j['access_token']
        user_refresh_token = j['refresh_token']
        return (user_token, user_refresh_token)
