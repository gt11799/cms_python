#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib2,urllib
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess,getMongoDBConn
from orders.models import getPackage
from shop_admin.models import pickExpressByPackageId
import random
def cathdeliver():
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select id,package_id,pack_time from order_goods where product_status='waitdeliver' and deliver='HT'"
    result = db.execQueryAssoc(sql)
    # package_queue = []
    package_ids = []
    order_goods_ids = []
    for p in result:
    	package_ids.append(str(p["package_id"]))
    package_ids = list(set(package_ids))
    if package_ids:
        for package_id in package_ids:
            deliver_mark = pickExpressByPackageId(package_id)
            if not deliver_mark:
                deliver_mark = "YT"
                try:
                    db2 = DBAccess()
                    db2.dbName = "express_records"
                    sql = "insert into parse_failed (package_id)values ('{}')".format(package_id)
                    db2.execNonQuery(sql)
                except:
                    pass
                        
            print 'updating pack_time...(waitdelivery...)'
            sql = "update order_goods set deliver = '%s' where package_id = %s " % (deliver_mark,package_id)
            db.execNonQuery(sql)

if __name__ == '__main__':
	cathdeliver()
