#coding: utf-8
import json
import requests

# oauth2 需要跟rescuetime申请才可以。正在申请中，所以目前只是使用了他的token来操作数据。
# https://www.rescuetime.com/apidoc
# Full key: B63QS4V5Rydzx7rlvIcLuCFeAxruuA5g039Kh7Zh
# key code: kEqF
# https://www.rescuetime.com/anapi/data?key=B63EqFoPaEX2L8WmevO16ky0b64nk0JFLG1YvaHb&perspective=interval&restrict_kind=productivity&interval=hour&restrict_begin=2014-11-01&restrict_end=2014-11-11&format=json

# https://www.rescuetime.com/anapi/daily_summary_feed?key=B63QS4V5Rydzx7rlvIcLuCFeAxruuA5g039Kh7Zh
#  http://t.cn/RAYHUhU