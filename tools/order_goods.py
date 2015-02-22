
# coding:utf-8
import os
import sys
import json

print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import DBAccess,NewSQLInsertBuilder,getMongoDBConn


sql = "select * from orders where order_status='confirmed' and create_time>'2014-08-00 00:00:00'"
db = DBAccess()
db.dbName  = "billing_record_db"

result = db.execQueryAssoc(sql)

for r in result:
    order_no=r['order_no']
    sql = "select * from order_goods where order_no='%s'"%order_no
    if db.execQueryAssoc(sql):
        continue
    else:
        print order_no,r["product_names"],r["event_ids"],r["product_ids"],r['brand_ids']
        db.execQueryAssoc("update orders set order_status='pending' where order_no='%s'"%order_no)
'''
sql = "select order_no,brand_ids,product_ids,product_images,event_ids from orders  where event_ids  regexp '1267' and create_time >'2014-08-05 00:00:00'"

db = DBAccess()

db.dbName  = "billing_record_db"

result = db.execQueryAssoc(sql)


todoGoods = {}
conn = getMongoDBConn()
mongodb = conn.shop


def getAllimage():
    image = {}
    goodsObj = mongodb.goods.find({},{"image":1})
    for obj in goodsObj:
        for i in obj["image"]:
            image[str(i)] = obj["_id"]

    return image

def copyGoods(goods_id,product_id):
    goodsObj = mongodb.goods.find_one({"_id":goods_id})
    if not goodsObj:
        print goods_id,product_id
        return
    goodsObj["_id"] = product_id
    goodsObj["activity_id"] = 1267
    goodsObj["goods_id"] = goods_id
    goodsObj["activity_name"] = "新手区2"
    mongodb.activity_goods.save(goodsObj)

for r in result:
    brand_ids = [ int(i) for i in r['brand_ids'].split('_') if i ]
    event_ids = [ int(i) for i in r['event_ids'].split('_') if i ]
    product_ids = [ int(i) for i in r['product_ids'].split('_') if i ]
    product_images = json.loads(r['product_images'])
    for i in range(0,len(brand_ids)):
        if event_ids[i] == 1267:
            product_id = product_ids[i]
            t = mongodb.activity_goods.find_one({"_id":product_id})
            if t and "goods_id" in t:
                continue
            else:
                todoGoods[product_id] = product_images[str(product_id)] 


image = getAllimage()

for key in todoGoods:
    product_id = key
    print product_id,
    url = todoGoods[key]
    goods_id = image.get(str(url))
    print goods_id
    copyGoods(goods_id,product_id)

'''
