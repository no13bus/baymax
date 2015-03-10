#coding: utf-8
from mechanize import Browser

class Argus(object):
    def __init__(self):
        pass

# headers={
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
# 'Cache-Control':'max-age=0',
# 'Connection':'keep-alive',
# 'Content-Type':'application/x-www-form-urlencoded',
# 'Host':'www.azumio.com',
# 'Origin':'http://www.azumio.com',
# 'Referer':'http://www.azumio.com/login',
# 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'
# }

LOGIN_URL = 'http://www.azumio.com/login'
email = 'no13bus@gmail.com'
password = '111111'
check_url = 'https://api.azumio.com/api2/checkins'
br = Browser()                # Create a browser
br.open(LOGIN_URL)            # Open the login page
br.select_form(nr = 0)       # Find the login form
br['email'] = email     # Set the form values
br['password'] = password
resp = br.submit()

r = br.open(check_url)
myjson = r.read()
