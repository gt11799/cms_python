#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from io import BytesIO
import csv
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime

def getOrderGoods():
	sql = "select a.*,b.province,b.city,b.district,b.street,b.detailed,b.phone,b.receiver_name from order_goods a,address b where a.address_id = b.address_id and left(a.create_time,10) >= '2014-09-19' and left(a.create_time,10) <= '2014-09-30'"
	db= DBAccess()
	db.dbName="billing_record_db"
	order_goods = db.execQueryAssoc(sql)
        return order_goods

def getpurchaseinfo(purchase_time):
	sql = "select * from new_purchase_list where purchase_time = '%s' " %purchase_time
	db= DBAccess()
	db.dbName="billing_record_db"
	arrive_time = db.execQueryAssoc(sql)
	return arrive_time[0] if arrive_time else ''

if __name__ == '__main__':
    orders = getOrderGoods()
    for r in orders:
        r["purchase_info"] = getpurchaseinfo(r["purchase_time"])
    output = BytesIO()
    writer = csv.writer(output)
    headData = ["订单号","姓名","手机号","地址","品牌","货号","数量","下单时间","采购单号","采购时间","到货时间","支付时间","打包完毕时间","发货完毕时间","最后状态","最后更新时间"]
    writer.writerow(headData)
    for r in orders:
        writer.writerow([ r["order_no"],r["receiver_name"],r['phone'],r["province"]+r["city"]+r["district"]+r["street"]+r["detailed"],r["brand_name"],r["product_code"],r["count"],r["create_time"],r["purchase_info"]["id"] if r["purchase_info"] else '',r["purchase_time"],r["purchase_info"]["arrival_time"] if r["purchase_info"] else '','',r["pack_time"],r["deliver_time"],r["product_status"],r["update_time"],])
    csv = output.getvalue()
    with open("/tmp/purchase_time.csv","wb") as f:
    	f.write(csv)
