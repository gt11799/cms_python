# coding:utf-8
import os
import sys
print "hello,window"

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess

from shop_admin.models import NewSQLInsertBuilder

from shop_admin.models import updateStockNum


db = DBAccess()
db.dbName = "billing_record_db"

package_ids = '''
235282
235267
235323
235322
235321
235318
235316
235312
235307
235309
235310
235315
235302
235304
235301
235279
235296
235300
235305
235308
235306
235274
235327
235326
235328
235303
235298
235288
235289
235291
235290
235272
235324
235273
235294
235285
235293
235286
'''

package_ids = [ int(i) for i in package_ids.strip().split() if i ]

print package_ids


for p in package_ids:
    sql = "update package_queue set package_status='send' where package_id=%s"%p
    print db.execUpdate(sql)
    '''
    sql = "select original_goods_id as product_id,product_size,count from order_goods where package_id=%s"%p
    result = db.execQueryAssoc(sql)
    for r in result:
        product_id = r["product_id"]
        size = r["product_size"]
        count = r["count"]

        sql = "select * from stock_detail where product_id=%s and size='%s' and count=%s \
            and update_time>'2014-10-08 14:00:00'  and update_time <'2014-10-09 00:00:00'"%(product_id,size,-count)

        if db.execQueryAssoc(sql):
            continue

        else:
            print "need update stock",product_id,size,count
            # print "need update stock"
            try:
                updateStockNum(product_id,size,-count,0,'',source="out_stock",operator="script")
            except:
                continue
    '''
