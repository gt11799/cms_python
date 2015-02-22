##coding:utf-8
import os
import sys
import urllib2,urllib
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess,getMongoDBConn

def test():
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = 'select count(id) as total,brand_name,brand_id from order_goods where  event_id not in(1653,2068,2185) ' \
          'group by brand_id order by total desc limit 100'
    r = db.execQueryAssoc(sql)
    l = []
    for x in r:
        brand_id = x["brand_id"]
        conn = getMongoDBConn()
        mongodb = conn.shop
        cursor = mongodb.activity.find_one({'brand_id':brand_id})
        try:
            s = cursor["category"]
            l.append(x)
        except:
            pass
    print(l)

def test_kuaidi_call_back():
    import json

    j = '''{"status":"polling","billstatus":"got","message":"","lastResult":{
		"message":"ok",
		"state":"0",
		"status":"200",
		"condition":"F00",
		"ischeck":"0",
		"com":"yuantong",
		"nu":"V030344422",
		"data":[{
"context":"上海分拨中心/装件入车扫描 ",
"time":"2012-08-28 16:33:19",
"ftime":"2012-08-28 16:33:19"
},{
"context":"上海分拨中心/下车扫描 ",
"time":"2012-08-27 23:22:42",
"ftime":"2012-08-27 23:22:42"
}]}
}
    '''
    j = json.dumps(j)
    print(j)
    postData = urllib.urlencode(j)

    req = urllib2.Request("192.168.1.118:5000/kuaidicallback/?", postData)
    req.add_header('Content-Type', "application/x-www-form-urlencoded")
    r = urllib2.urlopen(req)
    print(r)

if __name__ == "__main__":
    test()