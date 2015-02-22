#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from io import BytesIO
import csv
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime

def getPurchase():
    sql = "select a.*,b.purchase_time from new_purchase a left join new_purchase_list b on a.purchase_list_id = a.id"
    db= DBAccess()
    db.dbName="billing_record_db"
    purchase_goods = db.execQueryAssoc(sql)
    return purchase_goods

def getPurchaseCanceledGoods():
    db= DBAccess()
    db.dbName="billing_record_db"
    purchase_goods = getPurchase()
    order_cancel = []
    for r in purchase_goods:
    	sql = "select count(*) as sum from order_goods where purchase_time = '%s' and product_id = %s and product_size = '%s' and product_status like 'cancel' " %(r["purchase_time"],r["product_id"],r["size"])

    	cancel_count = db.execQueryAssoc(sql)[0]["sum"]
        diff_count = cancel_count - r["stock_out"]
        if diff_count > 0:
            sql = "select a.*,b.province,b.city,b.district,b.street,b.detailed,b.phone,b.receiver_name from order_goods a,address b where a.address_id = b.address_id and purchase_time = '%s' and product_id = %s and size = '%s' and product_status like '%cancel%' limit 0,%s" %(r["purchase_time"],r["product_id"],r["size"],diff_count)
            result = db.execQueryAssoc(sql)
            order_cancel += result
    return order_cancel
if __name__ == '__main__':
    orders = getPurchaseCanceledGoods()
    output = BytesIO()
    writer = csv.writer(output)
    headData = ["订单号","姓名","手机号","地址","品牌","货号","数量","尺码","颜色","订单状态"]
    writer.writerow(headData)
    for r in orders:
        writer.writerow([ r["order_no"],r["receiver_name"],r['phone'],r["province"]+r["city"]+r["district"]+r["street"]+r["detailed"],r["brand_name"],r["product_code"],r["count"],r["product_size"],r["product_color"],r["product_status"],])
    csv = output.getvalue()
    with open("/tmp/purchase_cancel.csv","wb") as f:
    	f.write(csv)
