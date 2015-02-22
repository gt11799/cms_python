#coding:utf-8
import os
import sys
import datetime

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess

import xlwt

class TopSalesGoodsFinder():
    def __init__(self, includeFreeGoods = False):
        self.freeGoods = includeFreeGoods

    def fetchData(self):
        sql = "select * from order_goods where status in ()"

sql = "select order_no,product_ids from orders where create_time>='2014-10-10 00:00:00' \
    and order_status not in ('pending','unconfirmed','timeout_cancelled')"

db = DBAccess()
db.dbName = "billing_record_db"

result = db.execQueryAssoc(sql)

for item in result:
    order_no = item["order_no"]
    product_ids = item["product_ids"]
    sql = "select count(*) from order_goods where order_no='%s'"%order_no
    t = db.execQuery(sql)[0][0]
    if t and t != len([ i for i in product_ids.split('_') if i]):
        print order_no