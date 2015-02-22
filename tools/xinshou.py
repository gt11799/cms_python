# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
# from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess,getMongoDBConn

sql ="select *  from order_goods where brand_id=10080;"

db = DBAccess()

db.dbName =  "billing_record_db"

#result = db.execQueryAssoc(sql)

conn = getMongoDBConn()
mongodb = conn.shop

goods = mongodb.activity_goods.find({"activity_id":1267})

for g in goods:
    print g["brand_id"],g['brand_name']
    brand_name = mongodb.brands.find_one({"_id":g["brand_id"]})['name']
    print brand_name
    mongodb.activity_goods.update({"brand_id":g["brand_id"]},{"$set":{"brand_name":brand_name}})
    sql = "update order_goods set brand_name='%s' where brand_id=%s"%(brand_name,g['brand_id'])
    db.execNonQuery(sql)


'''
for o in result:
    sql = "select * from order_goods where order_id=%s"%(o['order_id'],)
    orders = db.execQueryAssoc(sql)
    for r in orders: 
        goods_id = r["product_id"]
        goodsObj = mongodb.activity_goods.find_one({"_id":goods_id})
        brand_id = goodsObj['brand_id']
        if brand_id == 10182:
            continue
        brand_name = goodsObj['brand_name']
        sql = "update order_goods set brand_id=%s,brand_name='%s' where id=%s"%(brand_id,brand_name,r['id']) 
        print sql
        db.execQuery(sql)
     


for r in result:
    brand_name = r["brand_name"]
    product_name= r["product_name"]
    if product_name.startswith("图丽娅"):
        brand_id = 10063
        brand_name = "图丽娅"
    elif product_name.startswith("天二"):
        brand_id = 10139
        brand_name = "天二"

    elif product_name.startswith("7号小兔"):
        brand_id = 10104
        brand_name = "7号小兔"

    else:
        print brand_name
        continue

    print brand_id,brand_name
    sql = "update order_goods set brand_id=%s,brand_name='%s' where order_id=%s"%(brand_id,brand_name,r["order_id"])

    db.execNonQuery(sql)
'''
