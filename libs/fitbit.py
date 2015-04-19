#coding: utf-8
import requests
import json

# https://wiki.fitbit.com/display/API/Fitbit+API
# 文档写的好棒 这些api都提供了订阅者模式 订阅者模式可以实时同步 并且不会有api使用极限的限制
# Client (Consumer) Key  0ad642de85bc4e30a5c1e0aca8ec8355
# Client (Consumer) Secret  018285a1459844c082e9e0711328bd66
# Temporary Credentials (Request Token) URL  https://api.fitbit.com/oauth/request_token
# Token Credentials (Access Token) URL  https://api.fitbit.com/oauth/access_token
# Authorize URL  https://www.fitbit.com/oauth/authorize