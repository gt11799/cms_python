#coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getNowUTCtime,getRedisObj
from utility.utils import getMongoDBConn
import datetime

def userOrdersAna():
    start_date = datetime.date(2014, 04, 01)
    keys = []
    while start_date < datetime.date.today():
        k = start_date.strftime("%Y-%m")
        keys.append(k)
        start_date += datetime.timedelta(days=31)

    header = "月份,新增用户,总订单,平均订单数"
    for i in range(1, 21):
        header += ",下单%s次" % i

    header += ",下单%s次+" % i

    print header
    for key in keys:
        result = userOrderAnaMonth(key, keys)
        row = "%s,%s,%s,%s" % (key, result['users'], result['orders'], result['ava_orders'])

        for i in range(1,21):
            row += ",%s" % result[str(i)]

        row += ",%s" % result['21']
        print row



def userOrderAnaMonth(month,keys):
    db = getMongoDBConn().shop
    objs = db.user_orders_analysis.find({"first_order_date": month})
    result = {"users": 0, "orders": 0, "ava_orders": 0}
    for i in range(1, 22):
        result[str(i)] = 0

    for obj in objs:
        result["users"] += 1
        s = 0
        for key in keys:
            s += obj.get(key, 0)
        result['orders'] += s

        if s>= 21:
            s = 21

        result[str(s)] += 1

    if result["users"] == 0:
        result["ava_orders"] = 0
    else:
        result["ava_orders"] = round(result["orders"] / float(result["users"]), 2)
    return result



userOrdersAna()
