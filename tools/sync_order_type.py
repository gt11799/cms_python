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
sql = "select * from orders"
orders = db.execQueryAssoc(sql)

for r in orders:
    order_no = r["order_no"]
    order_type = r["order_type"]
    sql = "update order_goods set reserved_1='%s' where order_no='%s'"%(order_type,order_no)
    db.execNonQuery(sql)