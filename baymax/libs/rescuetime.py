#coding: utf-8
import json
import requests

API_URL = 'https://www.rescuetime.com/anapi'
# oauth2 需要跟rescuetime申请才可以。正在申请中，所以目前只是使用了他的token来操作数据。
# https://www.rescuetime.com/apidoc
# Full key: B63QS4V5Rydzx7rlvIcLuCFeAxruuA5g039Kh7Zh
# key code: kEqF
# https://www.rescuetime.com/anapi/data?key=B63EqFoPaEX2L8WmevO16ky0b64nk0JFLG1YvaHb&perspective=interval&restrict_kind=productivity&interval=hour&restrict_begin=2014-11-01&restrict_end=2014-11-11&format=json

# https://www.rescuetime.com/anapi/daily_summary_feed?key=B63QS4V5Rydzx7rlvIcLuCFeAxruuA5g039Kh7Zh
#  http://t.cn/RAYHUhU


class RescueTime(object):
    def __init__(self, token):
        self.token = token

    def get_data(self):
        res = {}
        url = '%s/daily_summary_feed?key=%s' % (API_URL, self.token)
        r = requests.get(url)
        j_all = json.loads(r.content)
        j = j_all[0]
        res['communication_and_scheduling'] = j['communication_and_scheduling_hours']
        res['software_development'] = j['software_development_hours']
        res['news'] = j['news_hours']
        res['entertainment'] = j['entertainment_hours']
        res['date'] = j['date']
        return res

    def get_datas(self):
        res_list = []
        url = '%s/daily_summary_feed?key=%s' % (API_URL, self.token)
        r = requests.get(url)
        j_all = json.loads(r.content)
        for j in j_all:
            res = {}
            res['communication_and_scheduling'] = j['communication_and_scheduling_hours']
            res['software_development'] = j['software_development_hours']
            res['news'] = j['news_hours']
            res['entertainment'] = j['entertainment_hours']
            res['date'] = j['date']
            res_list.append(res)
        return res_list


