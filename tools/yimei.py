#coding:utf-8
# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from utility.utils import DBAccess


from requests import request
import urllib
import urllib2

params = {"cdkey":"6SDK-EMY-6688-KEZSM","password":'660687'}
# params = {"cdkey":"6SDK-EMY-6688-KDSPR","password":'246131'}

def register():
    global params
    r = request("post","http://sdk4report.eucp.b2m.cn:8080/sdkproxy/regist.action",params=params)
    print r.text


def sendMsg(phone,content):
    global params
    local_params = params.copy()
    phone = ",".join(phone)
    local_params.update({"phone":phone,"message":content})
    r = request("post","http://sdk4report.eucp.b2m.cn:8080/sdkproxy/sendsms.action",params=local_params)
    print r.text

def getYiMeiBalance():
    postParas = params
    body = urllib.urlencode(postParas)
    try:
        import re
        req = urllib2.Request("http://sdk4report.eucp.b2m.cn:8080/sdkproxy/querybalance.action",body)
        res = urllib2.urlopen(req)
        Str = res.read()
        t = re.search("<message>([0-9,.,-].*?)</message>",Str)
        return int(float(t.group(1))*10)
    except Exception as e:
        print str(e)


def pushYueYueJia():
    db = DBAccess()
    db.dbName = "appsupport"
    sql = "select phone from apps_phone_list where app_type not like '%Menstruation%';"
    result = db.execQueryAssoc(sql)
    content = "【网利宝】尊敬的会员，月月佳福利100元理财享30元话费,3倍余额宝,平安保险全额承保,网利宝注册邀请码:axn7tq，回复TD退订"
    phone = []
    count = 0
    for item in result:
        phone.append(item['phone'])

        if len(phone) == 2000:
            # sendMsg(phone, content)
            print "send message done,%s,%s"%(phone[0],phone[-1])
            phone = []
            count += 2000

            if count >= 50000:
                return


def main():
    # register()
    # sendMsg(['18603036769','13243895577'],"【网利宝】尊敬的会员，月月佳福利100元理财享30元话费,3倍余额宝,平安保险全额承保,网利宝注册邀请码:axn7tq，回复TD退订")
    # print getYiMeiBalance()
    pushYueYueJia()

if __name__ == '__main__':
    main()
