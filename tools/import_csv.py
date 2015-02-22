# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess
from shop_admin.models import getDeliveringGoodsCsv
from address.models import getAddressInfo,getHumanAddress


sql = "select * from order_goods   where  deliver_time >='2014-09-01 00:00:00' and \
    deliver_time <='2014-09-10 00:00:00' and deliver='YT'"

db = DBAccess()
db.dbName = "billing_record_db"

result = db.execQueryAssoc(sql)

addressDict = {}

for r in result:
    order_no = r['order_no']
    if order_no not in addressDict:
        sql = "select order_no,human_address,receiver_name,phone from orders where order_no='%s'"%order_no

        _order = db.execQueryAssoc(sql)[0]

        if not  _order['human_address']:
            addressId = r["address_id"]
            addressInfo = getAddressInfo(addressId)
            address = getHumanAddress(addressInfo)
            receiver_name = addressInfo["receiver_name"]
            phone = addressInfo["phone"]
        else:
            address = _order['human_address']
            receiver_name = _order["receiver_name"]
            phone = _order["phone"]

        address = address.replace("我不清楚",'')

        addressDict[order_no] = {"address":address,"receiver_name":receiver_name,"phone":phone}
    else:
        address = addressDict[order_no]['address']
        receiver_name = addressDict[order_no]['receiver_name']
        phone = addressDict[order_no]['phone']

    r["address"] = address
    r["receiver_name"] = receiver_name
    r["phone"] = phone

csv = getDeliveringGoodsCsv(result)

with open("csv.csv","wb") as f:
    f.write(csv)



