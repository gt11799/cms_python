# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess,getMongoDBConn


conn = getMongoDBConn()
mongodb = conn.shop


db = DBAccess()
db.dbName = "billing_record_db"
sql = "select product_id,id,order_no from order_goods"
orders = db.execQueryAssoc(sql)
for t in orders:
    goods_id = t["product_id"]
    print goods_id
    try:
        original_goods_id = mongodb.activity_goods.find_one({"_id":goods_id})["goods_id"]
        print original_goods_id
    except Exception as e:
        print str(e)
        continue
    sql = "update order_goods set original_goods_id=%s where id=%s"%(original_goods_id,t['id'])
    db.execNonQuery(sql)