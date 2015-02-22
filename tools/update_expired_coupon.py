#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess, countTime
import datetime

@countTime
def update_expired_coupon():
    db = DBAccess()
    db.dbName = "backend_log_db"
    table="coupon_flow"
    sql = 'select * from %s where status= "未使用" and end_date<now()' % table
    results = list(db.execQueryAssoc(sql))
    for result in results:
    	if result["operator_id"]:
    		sql = "insert into coupon_flow(created_time,operator_id,receiver_id,type,start_date,end_date,discount_amount,\
				effective_amount, update_time, limit_order_price, status, coupon_id) values('%s',%s,%s,'%s','%s','%s',%s,\
				%s,'%s',%s,'%s',%s)" %(result["created_time"],result["operator_id"],result["receiver_id"],result["type"],
                result["start_date"],result["end_date"],result["discount_amount"],result["effective_amount"],
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),result["limit_order_price"],"已过期",result["coupon_id"])
        else:
			sql = "insert into coupon_flow(created_time,receiver_id,type,start_date,end_date,discount_amount,\
				effective_amount, update_time, limit_order_price, status, coupon_id) values('%s',%s,'%s','%s','%s',%s,\
				%s,'%s',%s,'%s',%s)" %(result["created_time"],result["receiver_id"],result["type"],result["start_date"],
				result["end_date"],result["discount_amount"],result["effective_amount"],
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),result["limit_order_price"],"已过期",result["coupon_id"])
        db.execNonQuery(sql)
    return

if __name__ == '__main__':
    update_expired_coupon()
