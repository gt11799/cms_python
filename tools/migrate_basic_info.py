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
sql = "select * from xh_user where last_login>'2014-04-23 0:0:0'"
result = db.execQueryAssoc(sql)
userCount = {}
for item in result:
    lastLoginTime = item['last_login']
    key = lastLoginTime.strftime("%Y-%m-%d")
    if key in userCount:
        userCount[key] = userCount[key] + 1
    else:
        userCount[key] = 1
userCount = sorted(userCount.iteritems(),key = lambda d:d[0])
for item in userCount:
    print str(item[0]) + "," + str(item[1]) + ";"

sql = "select * from orders where create_time>'2014-04-23 0:0:0'"
result = db.execQueryAssoc(sql)
orderCount = {}
dailyPay = {}

orderUserCount = {}
userHadPurchased = {}
def checkIfUserPurchased(uid):
    if uid in userHadPurchased:
        return True
    else:
        userHadPurchased[uid] = "1"
        return False

for item in result:
    createTime = item["create_time"]
    finalPay = item["total_pay"]
    uid = str(item["uid"])
    key = createTime.strftime("%Y-%m-%d")
    if key in orderCount:
        orderCount[key] = orderCount[key] + 1
    else:
        orderCount[key] = 1

    if key in dailyPay:
        dailyPay[key] = dailyPay[key] + float(finalPay)
    else:
        dailyPay[key] = finalPay

    if not checkIfUserPurchased(uid):
        if key in orderUserCount:
            orderUserCount[key] = orderUserCount[key] + 1
        else:
            orderUserCount[key] = 1


orderCount = sorted(orderCount.iteritems(),key = lambda d:d[0])
dailyPay = sorted(dailyPay.iteritems(),key = lambda d:d[0])
orderUserCount = sorted(orderUserCount.iteritems(), key = lambda d:d[0])
print ""
for item in orderCount:
    print str(item[0]) + "," + str(item[1]) + ";"
print ""
for item in dailyPay:
    print str(item[0]) + "," + str(item[1]) + ";"


for item in orderUserCount:
    print str(item[0]) + "," + str(item[1]) + ";"

sql = "select * from order_goods where create_time>'2014-04-23 0:0:0'"
result = db.execQueryAssoc(sql)


##########################
#品牌销量统计
##########################
brandCount = {}
brandPrice = {}
totalPrice = 0
for item in result:
    brandName = item['brand_name']  
    price = item['price'] * item["count"] * item['cargo_fee_rate']
    totalPrice = totalPrice + price
    if brandName in brandPrice:
        brandPrice[brandName] = brandPrice[brandName] + price
    else:
        brandPrice[brandName] = price
  
    if brandName in brandCount:
        brandCount[brandName] = brandCount[brandName] + 1
    else:
        brandCount[brandName] = 1

brandCount = sorted(brandCount.iteritems(),key = lambda d:d[1],reverse = True)
sumRatio = 0.0
for item in brandCount:
    sumRatio = sumRatio + int(brandPrice[item[0]]*10000/totalPrice)/100.0
    print str(item[0]) + "," + str(item[1]) + ","+str(brandPrice[item[0]]) + "," + str(int(brandPrice[item[0]]*10000/totalPrice)/100.0)
print sumRatio




####################
#1. A=如果商品表里，用户买过0.01元或10元的商品，同时还买过其他其他商品  的数量
#2. B=如果商品表里，用户买过0.01元或10元的商品 的数量
#3. A/B
####################

sql = "select * from order_goods"
db = DBAccess()
db.dbName = "billing_record_db"
result = db.execQueryAssoc(sql)
fuliUser = {}
nonFuliUser = {}
for item in result:
    price = item["price"]
    uid = str(item["uid"])
    if price < 15:
        fuliUser[uid] = 1
    else:
        nonFuliUser[uid] = 1

B = len(fuliUser)
intersectUser = {}
for uid in fuliUser:
    if uid in nonFuliUser:
        intersectUser[uid] = 1

A = len(intersectUser)

####################
#1. C=如果订单表里，用户买过0.01元或10元的订单，同时还买过其他其他订单  的数量
#2. D=如果订单表里，用户买过0.01元或10元的订单 的数量
#3. C/D


#基于订单的福利比率逻辑
####################
sql = "select * from orders"
db = DBAccess()
db.dbName = "billing_record_db"
result = db.execQueryAssoc(sql)
fuliUser = {}

for item in result:
    price = item["total_price"]
    uid = str(item["uid"])
    if price<15:
        fuliUser[uid] = 1
    else:
        nonFuliUser[uid] = 1

D = len(fuliUser)
intersectUser = {}
for uid in fuliUser:
    if uid in nonFuliUser:
        intersectUser[uid] = 1

C = len(intersectUser)

print "A: " + str(A) + " B:" + str(B) + " A/B:" + str(float(A)/float(B))

print "C: " + str(C) + " D:" + str(D) + " C/D:" + str(float(C)/float(D))





##########################
###6.20截止目前新人下的正常订单数
######################
sql = "select * from orders where create_time >'2014-06-23 0:0:0'"
db = DBAccess()
db.dbName = "billing_record_db"
result = db.execQueryAssoc(sql)

totalPrice = 0.0
for item in result:
    totalPrice = totalPrice + item['total_price'] + item['cargo_fee']

print totalPrice












