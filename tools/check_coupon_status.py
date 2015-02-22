# coding:utf-8
import os
import sys
print "hello,window" 
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from utility.utils import DBAccess
from coupon.models import deliverCashCoupon

def checkIfUserHadPurchaseRegular(uid):
	print "checking " + uid
	sql = "select * from orders where uid=%s" %(uid,)
	db = DBAccess()
	db.dbName = "billing_record_db"
	result = db.execQueryAssoc(sql)
	for item in result:
		print uid + "   "  + str(item["total_pay"])
		if item["total_pay"] >= 11:
			return True
	return False

db = DBAccess()
db.dbName = "billing_record_db"
sql = "select * from cash_coupon where activity_id=-2 and created_time>'2014-05-28 0:0:0'"
result = db.execQueryAssoc(sql)
uidCoupon = {}
for item in result:
	uid = str(item['uid'])
	if uid in uidCoupon:
		uidCoupon[uid] = uidCoupon[uid] + 1
	else:
		uidCoupon[uid] = 1

#key 是分享人的uid， value是分享有的有效下单数量
effectiveUser = {}
for item in uidCoupon:
	sql = "select uid from xh_user where referrer_uid='%s'" % (item,)
	result = db.execQueryAssoc(sql)
	effectiveUser[item] = 0
	for subItem in result:
		uid = str(subItem['uid'])
		if checkIfUserHadPurchaseRegular(uid):
			if item in effectiveUser:
				effectiveUser[item] = effectiveUser[item] + 1
			else:
				effectiveUser[item] = 1



for item in uidCoupon:
	print "%s, coupon:%s effectiveUser:%s" % (item,uidCoupon[item], effectiveUser[item])
	if uidCoupon[item] > effectiveUser[item]:
		print "handle %s" % (item,)
		depreCount = uidCoupon[item] - effectiveUser[item]
		sql = "select * from cash_coupon where activity_id=-2 and uid=%s order by created_time desc" % (item,)
		result = db.execQueryAssoc(sql)
		for i in range(0,depreCount):
			item = result[i]
			if item["coupon_status"] == "blocked":
				continue
			sql = "update cash_coupon set coupon_status='deprecated' where id=%s" % (str(item['id']),)
			#db.execNonQuery(sql)

			#deliverCashCoupon(item,datetime.datetime.now(),20,
			#	limitedOrderPrice = 50,availIntevalDay = 180,source='分享给好友',activityId = -3,ignoreUnique = True,couponType = 4)
			pass




	

