#! /usr/bin/env python
# -*- coding=utf8 -*-

import datetime
from io import BytesIO
import csv,os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from utility.mail import send_mail


def priceModify():
    '''
    修改价格，如果价格的尾数不是.9则去掉
    修改1月8号之后更新的活动
    '''
    print 1
    log_temp = ''
    db = getMongoDBConn().shop
    activities = db.activity.find({"verify_time":{"$gt":"2015-01-08 00:00:00"}},{"goods_id":1,"verify_time":1})
    for activity in activities:
        print activity['verify_time']
        log_temp += str(activity['_id']) + '   ' + str(activity['verify_time']) + '\n'
        for goods_id in activity["goods_id"]:
            goodsObj = db.activity_goods.find_one({"_id":int(goods_id)},{"price":1})
            if goodsObj['price'] % 1 < 0.8999:
                price = round(goodsObj['price'],0)
                db.activity_goods.update({"_id":int(goods_id)},{"$set":{"price":price}})
                goods_new = db.activity_goods.find_one({"_id":int(goods_id)},{"price":1})
                log_temp += str(goodsObj['_id']) + '    ' + str(goodsObj['price']) + '    ' + str(price) + '    ' + str(goods_new['price']) + '\n'
    return log_temp

if __name__ == "__main__":
    log_temp = priceModify()
    send_mail("price_modify_log", log_temp, ["gongting@xiaoher.com","wang@xiaoher.com"])
