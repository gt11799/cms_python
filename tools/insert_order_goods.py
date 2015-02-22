#coding:utf-8
import os
import sys
import json

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *

def getOrders(order_no):
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select * from orders where order_no='%s'"%order_no
    result = db.execQueryAssoc(sql)
    return result

def insertOrdersGoods(orders,product_status_same_as_orders=False,status_explain=None,cuser=''):
    '''将订单商品插入订单商品表'''

    conn = getMongoDBConn()
    mongodb = conn.shop

    db = DBAccess()
    db.dbName = "billing_record_db"

    nowTime = getNowUTCtime()

    fileds = ["product_id","product_name","product_code","count","brand_name",
              "brand_id","product_color","event_id","address_id","uid","cargo_fee",
              "product_size","product_image","price","original_price","refund_rate",
              "order_id","order_no","create_time","payment_method","wallet_rate","pay_rate",
              "cargo_fee_rate",'reserved_1','original_goods_id','hercoin_rate']

    if product_status_same_as_orders:
        fileds.append("product_status")

    # if status_explain:
    fileds.append("status_explain")
    fileds.append("deliver_time_preference")

    db = DBAccess()
    if cuser == "superadmin":
        db.dbName = "billing_record_db_v1"
    else:
        db.dbName = "billing_record_db"

    goodsDict = {}

    # create_time = getNowUTCtime()

    if status_explain:
        order_explain  = status_explain
    else:
        order_explain = None

    for order in orders:
        product_ids = [int(i) for i in order["product_ids"].split("_") if i]
        product_names = [i for i in order["product_names"].split("_") if i]
        prices = [ float(i) for i in order["prices"].split("_") if i]
        event_ids  = [int(i) for i in order["event_ids"].split("_") if i]
        market_prices = [int(i)
                         for i in order["original_prices"].split("_") if i]
        brand_ids = [int(float(i)) for i in order["brand_ids"].split("_") if i]
        counts = [int(i) for i in order["counts"].split("_") if i]
        sizes = [i for i in order["sizes"].split("_") if i]
        # event_ids  =
        total_price = order["total_price"]
        cargo_fee = order["cargo_fee"]
        paid_by_coupon = order["paid_by_coupon"]
        total_pay = order["total_pay"]
        create_time = order["create_time"]

        address_id = order["address_id"]

        uid = order["uid"]

        payment_method = order["payment_method"]

        product_images = json.loads(order["product_images"])

        product_status = order["order_status"]

        status_explain = order_explain or order["reserved_2"] or ""

        reserved_1 = order["order_type"]
        deliver_time_preference = order["deliver_time_preference"]

        # print status_explain,"*"*29

        order_id = order["order_id"]
        order_no = order["order_no"]
        cargo_fee  = order["cargo_fee"]
        paid_by_wallet = order["paid_by_wallet"]
        paid_by_hercoin = order["paid_by_hercoin"]

        if total_price:


            refund_rate = float( total_price - paid_by_coupon - paid_by_hercoin) / total_price
            if refund_rate < 0:
                refund_rate = 0
            # wallet_rate = float( paid_by_wallet - cargo_fee )/ total_price 
            
            # wallet_rate = float( paid_by_wallet) / (total_price )
            # if wallet_rate > 1:
            #     wallet_rate = 1

            pay_rate = float(total_pay) / total_price

            cargo_fee_rate = float(cargo_fee) / total_price

        # if pay_rate < 0:
        #     pay_rate = 0
        else:
            refund_rate = pay_rate = cargo_fee_rate = 0

        try:
            wallet_rate = float( paid_by_wallet) / (total_price + cargo_fee)
        except:
            wallet_rate = 0
        try:
            hercoin_rate = float( paid_by_hercoin) / total_price
        except:
            hercoin_rate = 0
        

        for i in range(len(product_ids)):
            try:
                product_id = product_ids[i]
                if product_id not in goodsDict:
                    if product_id >=  MIN_ACTIVITY_GOODS_ID:
                        goodsObj = mongodb.activity_goods.find_one({"_id": product_id}, {"brand_name": 1, "code": 1, "color": 1,"goods_id":1})
                    else:
                        goodsObj = mongodb.goods.find_one({"_id": product_id}, {"brand_name": 1, "code": 1, "color": 1})
                    goodsDict[product_id] = goodsObj
                else:
                    goodsObj = goodsDict[product_id]


                original_goods_id = goodsObj["goods_id"] if product_id >= MIN_ACTIVITY_GOODS_ID else product_id
                product_name = product_names[i]
                product_size = sizes[i]
                brand_name = goodsObj["brand_name"]
                brand_id = brand_ids[i]
                product_code = goodsObj["code"]
                product_color = goodsObj["color"]
                count = counts[i]
                price = prices[i]
                event_id = event_ids[i]
                original_price = market_prices[i]
                product_image = product_images[str(product_id)]
                deliver_time_preference = deliver_time_preference

                sql = "insert into order_goods("

                for i in fileds:
                    sql += i
                    sql += ','
                sql = sql[:-1] + ") values("

                for i in fileds:
                    value = locals()[i]
                    if isinstance(value,int) or isinstance(value,float):
                        sql += "%s"%value
                    else:
                        sql += "'%s'"%value

                    sql += ","

                sql = sql[:-1] + ")"
                # sql += " WHERE NOT EXISTS (select order_no from order_goods where \
                #     order_no='%s' and product_id=%s) limit 1"%(order_no,product_id)
                print sql
                try:
                    db.execNonQuery(sql)
                except:
                    pass
            except Exception as e:
                print str(e)
                sql = "update orders set order_status='pending' where order_no='%s'"%order_no
                db.execNonQuery(sql)
                break


if __name__ == "__main__":
    import sys
    order_no = sys.argv[1]
    result = getOrders(order_no)
    insertOrdersGoods(result)
