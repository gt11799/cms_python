# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from orders.models import insertOrdersGoods

from utility.utils import DBAccess

db = DBAccess()
db.dbName = "billing_record_db"
sql = "select * from orders where order_status in ('confirmed','picking','picked','packing','packed','delivering','finished')"

orders = db.execQueryAssoc(sql)

insertOrdersGoods(orders,True)