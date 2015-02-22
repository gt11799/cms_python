#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime,getRedisObj
from stock_log.barcode_models import BARCODE_LOG
# from stock_log.models import init_purchase
def getNeedFreeStock():
	db = DBAccess()
	db.dbName = "xiaoher_stock_db"
	sql = "select * from barcode_order_goods where status = 'blocked'"
	result = db.execQueryAssoc(sql)
	for r in result:
		order_goods = getOrderGoodsByOrderGoodsID(r["order_goods_id"])
		if order_goods:
			if order_goods[0]["product_status"] not in ["packing","packed","waitdeliver"]:
				BARCODE_LOG(order_goods_id=order_goods[0]["id"],order_no=order_goods[0]["order_no"],count=order_goods[0]["count"],goods_id=order_goods[0]["original_goods_id"],size=order_goods[0]["product_size"],source='user_cancelled_order',stock_location_id=0,operator='系统',barcode=0)
		else:
			pass
			

def getOrderGoodsByOrderGoodsID(order_goods_id):
	db = DBAccess()
	db.dbName = "billing_record_db"
	sql = "select * from order_goods where id = %s "%order_goods_id
	result = db.execQueryAssoc(sql)
	return result
		

if __name__ == '__main__':
	getNeedFreeStock()

