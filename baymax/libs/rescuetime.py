#coding: utf-8
import json
import requests

API_URL = 'https://www.rescuetime.com/anapi'



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


