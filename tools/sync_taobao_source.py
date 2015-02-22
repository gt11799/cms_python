# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import getMongoDBConn
from shop_admin.models import getTaobaoSource
def test():

    conn = getMongoDBConn()
    db = conn.shop

    goods = db.activity.find_one({"_id":2973})["goods_id"]
    for g in goods:
        goods_id = db.activity_goods.find_one({"_id":g},{"goods_id":1}).get("goods_id",0)
        print(goods_id)
if __name__ == "__main__":
    test()
    print("完成")
