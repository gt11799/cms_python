# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getMongoDBConn


def initGoodsStock(brand_id):
    
    conn = getMongoDBConn()
    db = conn.shop

    goods = db.goods.find({"brand_id":brand_id})

    for g in goods:
        g["stock"] = 0
        g["real_stock"] = 0
        g["init_stock"] = 0

        for s in g["size"]:
            s["stock"] = 0
            s["real_stock"] = 0
            s["init_stock"] = 0

        # print g
        db.goods.save(g)



if __name__ == "__main__":
    import sys
    brand_id = int(sys.argv[1])
    initGoodsStock(brand_id)