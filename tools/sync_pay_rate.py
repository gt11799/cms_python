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
    paid_by_wallet = r["paid_by_wallet"]
    total_price = r['total_price']
    cargo_fee = r["cargo_fee"]
    try:
        pay_rate = r["total_pay"] / r["total_price"]
    except:
        continue

    wallet_rate = float( paid_by_wallet) / (total_price + cargo_fee)

    cargo_fee_rate = float(cargo_fee) / total_price

    sql = "update order_goods set pay_rate=%s,wallet_rate=%s,cargo_fee_rate=%s \
    where order_no='%s'"%(pay_rate,wallet_rate,cargo_fee_rate,order_no,)

    print order_no,pay_rate,wallet_rate

    db.execNonQuery(sql)
