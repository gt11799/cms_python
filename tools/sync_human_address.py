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
    addressId = r["address_id"]
    addressInfo = getAddressInfo(addressId)
    human_address = getHumanAddress(addressInfo)
    phone = addressInfo["phone"]
    receiver_name = addressInfo["receiver_name"]
    order_no = r["order_no"]
    print order_no

    sql = " update orders set human_address='%s',phone='%s',receiver_name='%s' where order_no='%s'"%(human_address,phone,receiver_name,order_no)
    print sql

    db.execNonQuery(sql)

