# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess

#from shop_admin.models import NewSQLInsertBuilder,offlineDataCount

import datetime


def dataCount(date):
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid,order_no,prices from orders \
        where create_time >='%s 00:00:00' and create_time <='%s 23:59:59'"%(str(date),str(date))

    result = db.execQueryAssoc(sql)
    final_result = {"date":date}
    final_result['order_num'] = 0
    final_result['user_num'] = 0
    final_result['old_user_num'] = 0
    user_dict = {}
    final_result["goods_num"] = 0
    final_result['price_0'] = 0
    final_result['price_99'] = 0
    final_result['price_199'] = 0
    final_result['price_299'] = 0
    final_result['price_499'] = 0
    final_result['price_999'] = 0
    final_result['price_200'] = 0
    final_result['price_300'] = 0
    final_result['price_300_gt'] = 0

    for item in result:
        uid = item["uid"]
        if uid not in user_dict:
            user_dict[uid] = ''
            final_result["user_num"] += 1
            if checkOldUser(date,uid):
                final_result["old_user_num"] += 1
        else:
            pass
        final_result["order_num"] += 1
        prices = [ float(i) for i in item["prices"].split('_') if i ]
        final_result["goods_num"] += len(prices)

        for p in prices:

            final_result[getPriceKey(p)] += 1

    print final_result
    return final_result


def getPriceKey(p):
    if p <= 0.01:
        return "price_0"

    elif p<= 9.9:
        return "price_99"

    elif p<= 19.9:
        return "price_199"

    elif p<= 29.9:
        return "price_299"

    elif p<= 49.9:
        return "price_499"

    elif p<= 99.9:
        return "price_999"

    elif p<= 200:
        return "price_200"

    elif p<= 300:
        return "price_300"

    else:
        return "price_300_gt"

def checkOldUser(date,uid):
    sql = "select count(*) from orders where uid=%s and create_time <'%s 00:00:00'"%(uid,str(date))
    db = DBAccess()
    db.dbName = "billing_record_db"
    return db.execQuery(sql)[0][0]


def main():

    date = datetime.date.today()
    count = 0
    result = []
    while count<=5:
        d = date + datetime.timedelta(days=-count)
        result.append(dataCount(str(d)))
        count+=1

    print "日期 总单数  商品数 下单人数 老用户数 被购买的商品数量分布（0-0）（0-9.9） （9.9 - 19.9） （19.9 - 29.9) （29.9 - 49.9）（49.9-99.9）（99.9-200）（200-300）（300-）"
    for item in result:
        print "{date}  |{order_num}   |{goods_num}   |{user_num}   |{old_user_num}  |{price_0}  |{price_99}  |{price_199} |{price_499} |{price_999} |{price_200} \
        |{price_300} | {price_300_gt}".format(**item)


if __name__ == '__main__':
    main()