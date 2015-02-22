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


temp = '''
1. 103791      小班尼
2. 103790      多力
4. 103788      多力
5. 103787      多力
6. 103808      图丽娅
7. 103807      子牧棉麻
8. 103815      图丽娅
9. 103814      图丽娅
10.  103813      图丽娅
11.  103811      图丽娅
12.  103810      图丽娅
14.  103833      梦菲儿
15.  103832      梦菲儿
16.  103831      梦菲儿
17. 103830      梦菲儿
18. 103829      梦菲儿
19. 103828     梦菲儿
20. 103827     梦菲儿
21. 103862     小斑尼
22. 103861     小斑尼
23. 103860     小斑尼
24. 103859     小斑尼
25. 103858     小斑尼
26. 103856     小斑尼
27. 103853     小斑尼
28. 103849     小斑尼
29. 103848     小斑尼
30. 103846     小斑尼
31. 103845     小斑尼
32. 103791     小斑尼
'''
temp = temp.strip()
temp = temp.split()

length = len(temp)
DICT  = {}
i = 0
while  i < length-2:
    # print i
    key = int(temp[i+1])
    value = temp[i+2]
    if value == "小斑尼":
        value="小班尼"
    i += 3
    DICT[key]=value

print DICT



db = DBAccess()
db.dbName = "billing_record_db"
sql = "select * from order_goods where event_id=1140 and brand_id=10080"
orders = db.execQueryAssoc(sql)

for t in orders:
    order_goods_id = t["id"]
    brand_id = t["brand_id"]
    brand_name = t["brand_name"]
    product_name = t["product_name"]
    activity_goods_id = t["product_id"]

    ### by brand_name
    if "新手区" not in brand_name:
        b = mongodb.brands.find_one({"name":brand_name})
        if b:
            new_brand_name = b['name']
            new_brand_id = b["_id"]
            sql = "update order_goods set brand_id=%s,brand_name='%s' where id=%s"%(new_brand_id,new_brand_name,order_goods_id)
            db.execNonQuery(sql)
            continue

    ### by product_name

    g = mongodb.goods.find_one({"name":product_name})

    if g:
        new_brand_name = g['brand_name']
        new_brand_id = g["brand_id"]
        sql = "update order_goods set brand_id=%s,brand_name='%s' where id=%s"%(new_brand_id,new_brand_name,order_goods_id)
        db.execNonQuery(sql)
        continue


    g = mongodb.activity_goods.find_one({"_id":activity_goods_id})

    if not g:
        print order_goods_id
        continue

    goods_id = g["goods_id"]

    b_name = DICT.get(goods_id,'')

    if not b_name:
        continue

    
    b = mongodb.brands.find_one({"name":str(b_name)})
    if b:
        new_brand_name = b['name']
        new_brand_id = b["_id"]
        sql = "update order_goods set brand_id=%s,brand_name='%s' where id=%s"%(new_brand_id,new_brand_name,order_goods_id)
        db.execNonQuery(sql)
        continue

    print goods_id,b_name

    print order_goods_id















