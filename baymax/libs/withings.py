# -*- coding: utf-8 -*-
#
"""
Python library for the Withings API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Withings Body metrics Services API
<http://www.withings.com/en/api/wbsapiv2>
Uses Oauth 1.0 to authentify. You need to obtain a consumer key
and consumer secret from Withings by creating an application
here: <https://oauth.withings.com/partner/add>
Usage:
auth = WithingsAuth(CONSUMER_KEY, CONSUMER_SECRET)
authorize_url = auth.get_authorize_url()
print "Go to %s allow the app and copy your oauth_verifier" % authorize_url
oauth_verifier = raw_input('Please enter your oauth_verifier: ')
creds = auth.get_credentials(oauth_verifier)
client = WithingsApi(creds)
measures = client.get_measures(limit=1)
print "Your last measured weight: %skg" % measures[0].weight
"""

__title__ = 'withings'
__version__ = '0.1'
__author__ = 'Maxime Bouroumeau-Fuseau'
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Maxime Bouroumeau-Fuseau'

# __all__ = ['WithingsCredentials', 'WithingsAuth', 'WithingsApi',
#            'WithingsMeasures', 'WithingsMeasureGroup']

import requests
from requests_oauthlib import OAuth1, OAuth1Session
import json
import datetime


class WithingsCredentials(object):
    def __init__(self, access_token=None, access_token_secret=None,
                 consumer_key=None, consumer_secret=None, user_id=None):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_id = user_id


class WithingsAuth(object):
    URL = 'https://oauth.withings.com/account'

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = None
        self.oauth_secret = None

    # 得到url
    def get_authorize_url(self):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret)

        tokens = oauth.fetch_request_token('%s/request_token' % self.URL)
        print tokens
        self.oauth_token = tokens['oauth_token']
        self.oauth_secret = tokens['oauth_token_secret']

        return oauth.authorization_url('%s/authorize' % self.URL)

    def get_credentials(self, oauth_verifier):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.oauth_token,
                              resource_owner_secret=self.oauth_secret,
                              verifier=oauth_verifier)
        tokens = oauth.fetch_access_token('%s/access_token' % self.URL)
        print tokens
        # 这个返回的其实就是个dict
        # return WithingsCredentials(access_token=tokens['oauth_token'],
        #                            access_token_secret=tokens['oauth_token_secret'],
        #                            consumer_key=self.consumer_key,
        #                            consumer_secret=self.consumer_secret,
        #                            user_id=tokens['userid'])
        return dict(access_token=tokens['oauth_token'],
                   access_token_secret=tokens['oauth_token_secret'],
                   consumer_key=self.consumer_key,
                   consumer_secret=self.consumer_secret,
                   user_id=tokens['userid'])


class WithingsApi(object):
    URL = 'http://wbsapi.withings.net'

    def __init__(self, **kwargs):
        # self.credentials = kwargs
        self.oauth = OAuth1(unicode(kwargs['consumer_key']),
                            unicode(kwargs['consumer_secret']),
                            unicode(kwargs['access_token']),
                            unicode(kwargs['access_token_secret']),
                            signature_type='query')
        self.client = requests.Session()
        self.client.auth = self.oauth
        self.client.params.update({'userid': kwargs['user_id']})

    def request(self, service, action, params=None, method='GET'):
        if params is None:
            params = {}
        params['action'] = action
        r = self.client.request(method, '%s/%s' % (self.URL, service), params=params)
        response = json.loads(r.content)
        print response
        if response['status'] != 0:
            raise Exception("Error code %s" % response['status'])
        return response.get('body', None)

    # 好多参数是可选的 这个要注意 这个也是为什么选择**kwargs的原因
    # get_body_measures(startdate=1222819200, enddate=1223190167)
    def get_body_measures(self, kwargs):
        res_body = self.request('measure', 'getmeas', kwargs)
        return res_body

    # https://wbsapi.withings.net/v2/measure?action=getactivity&userid=29&startdateymd=2013-10-04&enddateymd=2013-10-08
    # get_activity_measures(userid=29, startdateymd='2013-10-04', enddateymd='2013-10-08')
    def get_activity_measures(self):
        params = {'action':'getactivity', 'userid':6828098, 'date':'2015-04-21'}
        r = self.client.request('GET', 'http://wbsapi.withings.net/v2/measure', params=params)
        # r = self.request('v2/measure', 'getactivity', kwargs)
        return r

    # https://wbsapi.withings.net/v2/measure?action=getintradayactivity&userid=29&startdate=1368138600&enddate=1368142469
    # get_intraday_activity(userid=29, startdate=1368138600, enddate=1368142469)
    def get_intraday_activity(self, kwargs):
        r = self.request('v2/measure', 'getintradayactivity', kwargs)
        return r

    # https://wbsapi.withings.net/v2/sleep?action=get&userid=29&startdate=1387234800&enddate=1387258800
    # get_sleep(userid=29, startdate=1387234800, enddate=1387258800)
    def get_sleep(self, kwargs):
        r = self.request('v2/sleep', 'get', kwargs)
        return r

    # https://wbsapi.withings.net/v2/sleep?action=getsummary&startdateymd=2014-06-20&enddate=2014-10-25
    # get_sleep_summary(startdateymd='2014-06-20', enddate='2014-10-25')
    def get_sleep_summary(self, kwargs):
        r = self.request('v2/sleep', 'getsummary', kwargs)
        return r

    def subscribe(self, callback_url, comment, appli=1):
        params = {'callbackurl': callback_url,
                  'comment': comment,
                  'appli': appli}
        self.request('notify', 'subscribe', params)

    def unsubscribe(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        self.request('notify', 'revoke', params)

    def is_subscribed(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        try:
            self.request('notify', 'get', params)
            return True
        except:
            return False

    def list_subscriptions(self, appli=1):
        r = self.request('notify', 'list', {'appli': appli})
        return r['profiles']


class WithingsMeasureGroup(object):
    MEASURE_TYPES = (('weight', 1), ('height', 4), ('fat_free_mass', 5),
                     ('fat_ratio', 6), ('fat_mass_weight', 8),
                     ('diastolic_blood_pressure', 9), ('systolic_blood_pressure', 10),
                     ('heart_pulse', 11))

    def __init__(self, data):
        self.data = data
        self.grpid = data['grpid']
        self.attrib = data['attrib']
        self.category = data['category']
        self.date = datetime.datetime.fromtimestamp(data['date'])
        self.measures = data['measures']
        for n, t in self.MEASURE_TYPES:
            self.__setattr__(n, self.get_measure(t))

    def is_ambiguous(self):
        return self.attrib == 1 or self.attrib == 4

    def is_measure(self):
        return self.category == 1

    def is_target(self):
        return self.category == 2

    def get_measure(self, measure_type):
        for m in self.measures:
            if m['type'] == measure_type:
                return m['value'] * pow(10, m['unit'])
        return None

if __name__ == '__main__':
    auth = WithingsAuth('', '')
    authorize_url = auth.get_authorize_url()

    oauth_verifier = raw_input('Please enter your oauth_verifier: ')
    creds = auth.get_credentials('XS9syb8rp95Jg9prm4jB')
    # 开始请求
    creds_dcit = {'access_token': u'',
                 'access_token_secret': u'',
                 'consumer_key': '',
                 'consumer_secret': '',
                 'user_id': u''}
    # creds_dcit 非常重要
    client = WithingsApi(**creds_dcit)
    body_measures = client.get_body_measures({'startdate':1429275337, 'enddate':1429707337})
    ### 不对 取得的body是空的
    activity_measures = client.get_activity_measures()
    intraday_activity = client.get_intraday_activity({'startdate': 1429275337, 'enddate':1429707337})
    sleep = client.get_sleep({'startdate':1429275337, 'enddate':1429707337})
