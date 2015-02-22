# coding:utf-8
import os
import sys
print "hello,window"
import datetime
import time
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
# from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime,errorLog
from shop_admin.models import addToblackUser,getUserByUid, get_skip_list
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ERRORLOG = errorLog()

def isOnlyCancelledOrder(uid):
    sql = "select order_status from orders where uid=%s" %(uid,)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    for item in result:
        if item["order_status"] != "user_cancelled":
            return False
    return True


from sms.models import sendMessage

def automacticallyCheckUser():
    sql = "select uid from cash_coupon where activity_id=-2  group by uid having count(uid)  > 5;"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    for item in result:
        uid = item["uid"]
        if uid == 0:
            continue
        sql = "select uid from xh_user where referrer_uid=%s" % (str(uid),)
        uidResult = db.execQueryAssoc(sql)
        count = 0
        cancelledCount = 0
        for subItem in uidResult:
            count = count + 1
            ruid = subItem["uid"]
            if isOnlyCancelledOrder(ruid):
                cancelledCount = cancelledCount + 1
        user = getUserByUid(uid)[0]
        #print " 姓名：" + str(user["username"]) + "  电话:" +  str(user["phone"]) + " 该用户所有分享获得优惠券:" + str(count) + " 他的朋友中 取消订单的数量：" + str(cancelledCount)
        # skipList = ["18318823189","18617050051","18617091441","15915430757","15989315768","13692171956"]
        skipList = get_skip_list()
        if float(cancelledCount) / float (count) >= 0.3:
            porm = user['phone'] if user['phone'] else user['email']
            # if user["phone"] is not None and user["phone"] not in skipList:
            if int(uid) not in skipList:
                addToblackUser(porm)
                cancelUnDeliveringUserOrder(uid)
                if user['phone']:
                    sendMessage(user['phone'],"您的账号存在异常，已冻结，请及时联系我们客服,热线电话：400-888-6700")



def cancelUnDeliveringUserOrder(uid):
    sql = "select product_status,id,payment_method from order_goods where uid=%s" %(str(uid),)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    for item in result:
        status = item["product_status"]
        if status in ["packed","packing","picking","purchase"] and item['payment_method'] == "0":
            print item["id"]
            cancelOrderGoods(item["id"])

    sql = "select order_status,order_no,payment_method from orders where uid=%s" % (uid,)
    result = db.execQueryAssoc(sql)
    for item in result:
        if item['order_status'] == "pending" and item['payment_method'] == '0':
            print item["order_no"]
            cancelOrder(item["order_no"])
    pass

def cancelOrderGoods(orderGoodsId):
    if not orderGoodsId:
        return
    sql = "update order_goods set product_status='admin_cancelled',package_id=0 where id=%s" % (str(orderGoodsId),)
    db = DBAccess()
    db.dbName= "billing_record_db"
    db.execNonQuery(sql)

def cancelOrder(orderNo):
    sql = "update orders set order_status='admin_cancelled' where order_no=%s" % (str(orderNo),)
    db = DBAccess()
    db.dbName= "billing_record_db"
    db.execNonQuery(sql)




if __name__ == "__main__":
    automacticallyCheckUser()





