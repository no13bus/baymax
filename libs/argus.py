#coding: utf-8
from mechanize import Browser
import json
import datetime


API_URL = 'https://www.azumio.com/'
class Argus(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.br = Browser()
        self._login()

    def _login(self):
        login_url = '%s%s' % (API_URL, 'login')
        self.br.open(login_url)
        self.br.select_form(nr = 0)
        self.br['email'] = self.email
        self.br['password'] = self.password
        resp = self.br.submit()
        return resp

    def getdata(self):
        pass

    def checkins(self):
        check_url = '%s%s' % (API_URL, 'api2/checkins?type=drink')
        r = self.br.open(check_url)
        return json.loads(r.read())

if __name__ == '__main__':
    ag = Argus('no13bus@gmail.com', 'jiazhang')
    j = ag.checkins()
    print [datetime.datetime.fromtimestamp(i['timestamp']/1000) for i in j['checkins']]


# http://developer.azumio.com/azumio-api
# why requests can not post form data request??? it's not work
# webhook is fun. flask. request.data