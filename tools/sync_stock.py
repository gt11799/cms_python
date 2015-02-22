# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import getMongoDBConn

conn  = getMongoDBConn()
db = conn.shop


def syncStock():

    return
    activityGoodsObjs = db.activity_goods.find()
    for obj in activityGoodsObjs:
        size = obj["size"]
        real_stock = 0
        for s in size:
            if s["real_stock"] < 0:
                s["real_stock"] = 0
            
            s["stock"] = s["real_stock"]

            real_stock += s["real_stock"]

        obj["real_stock"] = real_stock
        obj["stock"] = real_stock

        db.activity_goods.save(obj)


