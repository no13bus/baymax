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


class FitbitAuth(object):
    URL = 'https://api.fitbit.com'

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = None
        self.oauth_secret = None

    # 得到url
    def get_authorize_url(self):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret)

        tokens = oauth.fetch_request_token('%s/oauth/request_token' % self.URL)
        print tokens
        self.oauth_token = tokens['oauth_token']
        self.oauth_secret = tokens['oauth_token_secret']

        return oauth.authorization_url('%s/oauth/authorize' % self.URL)

    def get_credentials(self, oauth_verifier):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.oauth_token,
                              resource_owner_secret=self.oauth_secret,
                              verifier=oauth_verifier)
        tokens = oauth.fetch_access_token('%s/oauth/access_token' % self.URL)
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
                   user_id=tokens['encoded_user_id'])


class FitbitApi(object):
    URL = 'https://api.fitbit.com'
    # US = 'en_US'
    # METRIC = 'en_UK'
    API_VERSION = 1

    def __init__(self, **kwargs):
        # self.credentials = kwargs
        self.oauth = OAuth1(unicode(kwargs['consumer_key']),
                            unicode(kwargs['consumer_secret']),
                            unicode(kwargs['access_token']),
                            unicode(kwargs['access_token_secret']),
                            signature_type='auth_header')
        self.client = requests.Session()
        # 给requests实例 添加oauth认证
        self.client.auth = self.oauth
        # self.client.params.update({'userid': kwargs['user_id']})
        self.user_id = kwargs['user_id'] if kwargs.get('user_id', None) else '-'
        # system 如果不是 en_US 和 en_UK 那么就是采用公制的常规单位
        self.system = kwargs['system'] if kwargs.get('system', None) else None

    def request(self, service, params=None, method='GET'):
        if params is None:
            params = {}
        headers = {'Accept-Language': self.system}
        r = self.client.request(method, '%s/%s/%s' % (self.URL, self.API_VERSION, service), params=params, headers=headers)
        response = json.loads(r.content)
        # if response['status'] != 0:
        #     raise Exception("Error code %s" % response['status'])
        return response

    # 好多参数是可选的 这个要注意 这个也是为什么选择**kwargs的原因
    # get_user_profile(user_id=3333)  or get_user_profile()
    def get_user_profile(self, **kwargs):
        user_id = kwargs.get('user_id', None)
        if not user_id:
            user_id = '-'
        service = "user/%s/profile.json" % user_id
        res_body = self.request(service)
        return res_body

    # /1/user/228TQ4/sleep/date/2010-02-25.json
    def get_sleep(self, **kwargs):
        user_id = kwargs.get('user_id', None)
        date_string = kwargs['date']
        if not user_id:
            user_id = '-'
        service = "user/%s/sleep/date/%s.json" % (user_id, date_string)
        res_body = self.request(service)
        return res_body



if __name__ == '__main__':
    auth = FitbitAuth('0ad642de85bc4e30a5c1e0aca8ec8355', '018285a1459844c082e9e0711328bd66')
    authorize_url = auth.get_authorize_url()
    # http://baymax.ninja/callback?oauth_token=f2136e8a65fabe844adc16e8fc451bb0&oauth_verifier=95ee6317d3abc29ca8c01f7507d3cee4
    oauth_verifier = raw_input('Please enter your oauth_verifier: ')
    creds = auth.get_credentials('95ee6317d3abc29ca8c01f7507d3cee4')
    # 开始请求
    #    {'access_token': u'368dc98e41bea23c702b2fdea471ecc1',
    # 'access_token_secret': u'a26d868de479cdb3a6e3943f68968299',
    # 'consumer_key': '0ad642de85bc4e30a5c1e0aca8ec8355',
    # 'consumer_secret': '018285a1459844c082e9e0711328bd66',
    # 'user_id': u'3BNRKD'}
    creds_dcit = {'access_token': u'368dc98e41bea23c702b2fdea471ecc1',
                 'access_token_secret': u'a26d868de479cdb3a6e3943f68968299',
                 'consumer_key': '0ad642de85bc4e30a5c1e0aca8ec8355',
                 'consumer_secret': '018285a1459844c082e9e0711328bd66',
                 'user_id': u'3BNRKD'}
    # creds_dcit 非常重要
    client = FitbitApi(**creds_dcit)
    body_measures = client.get_user_profile()
    ### 不对 取得的body是空的

