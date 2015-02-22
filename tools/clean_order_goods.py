# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import *

from shop_admin.models import genPackageId

db = DBAccess()

db.dbName = "billing_record_db"

deliverNoDict = {} # deliber package_id

sql = " select * from order_goods "

result = db.execQueryAssoc(sql)

for r in result:

    if not r["deliver_no"]:
        continue

    if r["deliver_no"] in deliverNoDict:
        continue

    package_id = genPackageId()

    sql = "update order_goods set package_id=%s where deliver_no='%s'"%(package_id,r["deliver_no"])

    db.execQuery(sql)
    
    deliverNoDict[r["deliver_no"]] = ""