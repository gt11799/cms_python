# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess

db = DBAccess()
db.dbName = "billing_record_db"
sql = "select order_no,order_status from orders"
orders = db.execQueryAssoc(sql)

for r in orders:
    order_no = r["order_no"]
    if r["order_status"] in ("user_cancelled","timeout_cancelled","unpay","pending","unconfirmed"):
        continue
    sql = "select count(*) from order_goods where order_no='%s'"%order_no
    if(db.execQuery(sql)[0][0]) == 0:
        print order_no

