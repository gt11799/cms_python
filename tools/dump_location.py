#coding: utf-8

import os
import sys
import datetime
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from check_bill.models import getResultFromMySQL, transMysqlExec,getUpdateSql
from stock_log.barcode_models import BARCODE_LOG
from utility.utils import NewSQLInsertBuilder, getMongoDBConn, getNowUTCtime ,DBAccess


def split_file(filename):

    mongodb = getMongoDBConn().shop
    db = DBAccess()
    db.dbName = "xiaoher_stock_db"
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        _t = line.split(',')
        try:
            product_id = int(_t[0])
        except:
            print "%s,cangwei" % line
            continue

        goods = mongodb.activity_goods.find_one({"_id": product_id}, {"goods_id": 1})
        if not goods:
            print "%s,not found the goods" % line
            continue

        goods_id = goods['goods_id']

        sql = "select a.stock_location_id,b.location_name from stock_location_barcode a, stock_log_db.storage_location b" \
              " where a.stock_location_id=b.id and a.stock_location_id>0 and a.goods_id=%s" % goods_id

        result = db.execQueryAssoc(sql)
        if not result:
            print "%s, not found the location_name" % line
            continue

        print "%s,%s" % (line, result[0]['location_name'].decode("utf-8").encode("gbk"))



if __name__ == "__main__":
    print split_file("1.csv")
