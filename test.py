#coding: utf-8
import requests
import json


API_KEY = '982519480'
API_SECRET = '57875e1b5d0a61385b06a1ae76bfe398'
REDIRECT_URI = 'https://api.weibo.com/oauth2/default.html'

from weibo import Client
c = Client(API_KEY, API_SECRET, REDIRECT_URI)
c.authorize_url
# https://api.weibo.com/oauth2/default.html?code=d4912b9d15777d799be53273b3e3655a
# https://api.weibo.com/oauth2/default.html?code=3ae8ff636f7ca71ef2cda13ac5ca9a7e
auth_url = 'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A%2F%2Fapi.weibo.com%2Foauth2%2Fdefault.html&client_id=982519480'
r = requests.get(auth_url)
print r.url

# https://api.weibo.com/oauth2/default.html?code=e3ff24403bf4f1d570a00cffd0b39ac8
c.set_code('3ae8ff636f7ca71ef2cda13ac5ca9a7e')
d = c.get('statuses/user_timeline', uid=2586104751, count=50)

# d['statuses'][0]['user']['statuses_count']
for x in d['statuses']:
    print x['text']
    print x['created_at']



#### emotions analysis
from bosonnlp import BosonNLP
BOSON_KEY = 'DLg8aedI.2485.ay8NOHblggqH'
nlp = BosonNLP(BOSON_KEY)
nlp.sentiment(text)