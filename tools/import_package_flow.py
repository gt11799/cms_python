# coding:utf-8
import os
import sys
print "hello,window"
import datetime
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from orders.models import getPackage

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime,NewSQLInsertBuilder

db = DBAccess()
db.dbName = "billing_record_db"
sql = "select * from order_goods where deliver_time >='2014-07-17 00:00:00' \
    and  deliver_time <='2014-09-05 00:00:00' and product_status not in ('admin_cancelled','user_cancelled')"
packageDict = {}
result = db.execQueryAssoc(sql)
for r in result:

    package_id = int(r["package_id"])
    if package_id == 0:
        continue

    if package_id in packageDict:
        continue
    else:
        packageDict[package_id] = ''

    package = getPackage(package_id)
    if not package:
        continue

    deliver_no = r["deliver_no"]
    deliver = r["deliver"]
    packed_by = r["packed_by"]
    deliver_time = r["deliver_time"]

    db.execNonQuery(sql)
    # print [ r["id"] for r in package['goods'] ]
    sqlDict = {
        "package_id":package_id,
        "deliver_no":deliver_no,
        "deliver":deliver,
        "packed_by":packed_by,
        "deliver_time":deliver_time,
        "package_status":"send",
        "should_paid":package["real_should_paid"],
        "order_goods_id":"_".join([ str(r["id"]) for r in package['goods'] ]),
    }
    try:
        sql = NewSQLInsertBuilder(sqlDict,"package_flow",True)
        db.execNonQuery(sql)
    except:
        print sql
        pass
