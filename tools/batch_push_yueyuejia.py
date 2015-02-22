# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from utility.utils import DBAccess
from register.models import encryPassword

import urllib
import urllib2
def sendMessage(phone,content):
    username = 'xhfz'
    content += "【小荷】"
    password = encryPassword(username+encryPassword('pluray2014'))
    postParas = {'username':username,'password':password,'mobile':phone,'content':content}
    body = urllib.urlencode(postParas)
    req = urllib2.Request("http://211.154.154.151/smsSend.do",body)
    res = urllib2.urlopen(req)
    Str = res.read()
    
    print phone
    print Str

db = DBAccess()
db.dbName = "appsupport"
sql = "select phone from apps_phone_list where app_type not like '%Menstruation%';"

result = db.execQueryAssoc(sql)

i = 0
forSendStr = "" 
for item in result:
    phone = item["phone"]
    i = i +1
    content = "0元, 10元, 20元，品牌服装秒杀活动。巧动用户独享活动。http://m.xiaoher.com 回复TD退订"
    
    if i % 4000 == 0 or i >= len(result):
        sendMessage(forSendStr,content)
        #print forSendStr
        forSendStr = ""
    forSendStr = forSendStr + phone + ","










