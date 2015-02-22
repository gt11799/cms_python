# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from utility.utils import DBAccess

db = DBAccess()
db.dbName = "billing_record_db"

def normalOrderExists(uid):
    sql = "select * from orders where uid=%s and total_price>1" % (uid,)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    if result:
        return True
    else:
        return False

##########################
###6.20截止目前新人下的正常订单数
######################
sql = "select * from orders where create_time >'2014-04-23 0:0:0'"
db = DBAccess()
db.dbName = "billing_record_db"
result = db.execQueryAssoc(sql)

totalPrice = 0.0
dateUidDict = {}
for item in result:
    totalPrice = item['total_price']
    uid = item['uid']
    dateStr = item["create_time"].strftime("%Y-%m-%d")
    if totalPrice < 1:
        if dateStr in dateUidDict:
            dateUidDict[dateStr][str(uid)] = 1
        else:
            temp = {}
            temp[str(uid)] = 1
            dateUidDict[dateStr] = temp

dateUidDict = sorted(dateUidDict.iteritems(),key = lambda d:d[0])

secDict = {}
    uidSet = item[1]for item in dateUidDict:

    secDict[item[0]] = 0
    for uid in uidSet:
        if normalOrderExists(uid):
            secDict[item[0]]  = secDict[item[0]] + 1

    print item[0] + "  " + str(len(uidSet)) + "  " + str(secDict[item[0]])













