#!/usr/bin/env python
# -*- coding: utf-8 -*-

#coding:utf-8
import os
import sys
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from check_bill.models import getResultFromMySQL

def getStockSumFromDetails(stock_details=[]):
    '''

    :param stock_details: 商品的stock_detail记录
    :return:
    '''
    stock_sum = 0
    size_arr = []

    for sd in stock_details:
        size = sd['size']
        locations = sd['locations']
        stock = sum([i['num'] for i in locations])

        s_a = filter(lambda a: a['mark'] == size, size_arr)
        if s_a:
            s_a[0]['stock'] += stock
        else:
            size_arr.append({'mark': size, 'stock':stock})
        stock_sum += stock

    return stock_sum, size_arr


def goodsStockSumFromId(goods_id=0, stock_detail=[]):
    '''
    :param goods_id: 商品id号
    :param stock_detail: 商品相关的staock_detail记录
    :return:
    '''
    if goods_id:
        conn = getMongoDBConn()
        db = conn.shop
        stock_detail = stock_detail or list(db.stock_detail.find({'goods_id': goods_id}))

        if stock_detail:
            #goods_stock = db.goods_stock_sum.find_one({'_id': goods_id})
            #if not goods_stock:
            #    db.goods_stock_sum.insert({'_id': goods_id})

            stock_sum, size_arr = getStockSumFromDetails(stock_detail)
            set_dic = {'stock': stock_sum, 'size': size_arr}
            db.goods_stock_sum.update({'_id': goods_id}, {'$set':set_dic}, True)


def getAllProductNeedStock():

    query_dict = {"product_status__in": ("picking", "purchase")}
    fields = ['count', 'product_size','original_goods_id']
    result = getResultFromMySQL("billing_record_db", "order_goods",page="nopage", query_dict=query_dict,fields=fields)
    need_stock = {}
    for r in result:
        if r["original_goods_id"] not in need_stock:
            need_stock[r['original_goods_id']] = {}

        need_stock[r['original_goods_id']][r['product_size']] = need_stock[r['original_goods_id']].get(r['product_size'],0) + r["count"]

    query_dict = {"order_status": "pending"}
    fields = ["product_ids", "counts", "sizes"]
    result = getResultFromMySQL("billing_record_db", "orders", query_dict=query_dict,fields=fields, page="nopage")
    db = getMongoDBConn().shop
    for r in result:
        product_ids = [ int(i) for i in r["product_ids"].split('_') if i]
        counts = [ int(i) for i in r["counts"].split('_') if i]
        sizes = [ i for i in r["sizes"].split('_') if i]

        for i in range(len(product_ids)):
            try:
                product_id = product_ids[i]
                count = counts[i]
                size = sizes[i]
            except IndexError:
                print product_id
                continue
            try:
                original_goods_id = db.activity_goods.find_one({"_id":product_id},{"goods_id":1})['goods_id']
            except:
                continue


            if original_goods_id not in need_stock:
                need_stock[original_goods_id] = {}

            need_stock[original_goods_id][size] = need_stock[original_goods_id].get(size,0) + count

    return need_stock



def getProductNeedStock(product_id):
    query_dict = {"original_goods_id": product_id, "product_status__in": ("picking", "purchase")}
    fields = ['count', 'product_size']
    result = getResultFromMySQL("billing_record_db", "order_goods",page="nopage", query_dict=query_dict,fields=fields)
    need_stock = {}
    for r in result:
        need_stock[r['product_size']] = need_stock.get(r['product_size'], 0) + r['count']

    # orders in pending
    # first the event
    db = getMongoDBConn().shop
    activity_id  = [ obj['activity_id']  for obj in
                     db.activity_goods.find({"goods_id":product_id},{"_id":1,"activity_id":1})]
    now_time = getNowUTCtime()
    activity_id = [ obj["_id"] for obj in
                    db.activity.find({"_id":{"$in":activity_id},"create_time":{"$lt":now_time},"end_time":{"$gt":now_time},"status":3},{"_id":1})]
    for event_id in activity_id:
        query_dict = {"order_status": "pending","event_ids__regexp":str(event_id)}
        fields = ["event_ids", "product_ids", "counts", "sizes"]
        result = getResultFromMySQL("billing_record_db", "orders", query_dict=query_dict,fields=fields, page="nopage")
        for r in result:
            event_ids = [ int(i) for i in r["event_ids"].split('_') if i]
            product_ids = [ int(i) for i in r["product_ids"].split('_') if i]
            counts = [ int(i) for i in r["counts"].split('_') if i]
            sizes = [ i for i in r["sizes"].split('_') if i]

            for i in range(len(event_ids)):
                if event_ids[i] != event_id:
                    continue
                _id = product_ids[i]

                if not db.activity_goods.find_one({"_id":_id, "goods_id":product_id}):
                    continue

                size = sizes[i]

                need_stock[size] = need_stock.get(size,0) + counts[i]

    return need_stock

def setProductStock(product_id,need_stock):

    need_stock = {}
    query_dict = {"goods_id":product_id}
    fields = ["goods_id", "size", "free_stock"]
    result = getResultFromMySQL("xiaoher_stock_db", "storage_goods_stock", query_dict=query_dict, page="nopage",fields=fields)
    stock = 0
    size = []
    for r in result:
        # print r['product_id']
        if r["goods_id"] == 2153:
            for key,values in need_stock.items():
                print key,values
        s_stock = r["free_stock"] - need_stock.get(r["size"],0)
        s_mark = r["size"]
        if s_stock < 0:
            s_stock = 0

        size.append({"stock": s_stock, "mark": s_mark})
        stock += s_stock


    set_dic = {'stock': stock, 'size': size,'update_time': datetime.datetime.now()}
    db = getMongoDBConn().shop
    db.goods_stock_sum.update({'_id': product_id}, {'$set': set_dic}, True)


def updateGoodsStockFromNewStock(mode="all"):

    # 从new_stock表读取库存更新,不考虑采购的影响

    # all_need_stock = getAllProductNeedStock()
    all_need_stock = {}

    print "mode is %s"%mode

    if mode == 'all':
        fields = ["goods_id"]
        result = getResultFromMySQL("xiaoher_stock_db", "storage_goods_stock",
                                query_dict={}, fields=fields, group_by='group by goods_id', page="nopage")

        for item in result:
            product_id = item["goods_id"]
            setProductStock(product_id,all_need_stock.get(product_id,{}))
    else:
        for product_id,need_stock in all_need_stock.items():
            setProductStock(product_id,need_stock)


    # 十分钟更新,保证库存及时更新
    r = getRedisObj()
    key = "goods_stock_update"
    r.set(key, 1)
    r.expire(key, 60*10)

def goodsStockSumInstockTime():
    ''' 将入库时间[采购] instock_time， 加入 mongo goods_stock_sum '''
    mysqldb = DBAccess()
    mysqldb.dbName = "billing_record_db"
    sql = ''' select Max(update_time) as instock_time, product_id as goods_id from stock_detail where count > 0 group by product_id '''
    result = mysqldb.execQueryAssoc(sql)

    db = getMongoDBConn().shop

    for r in result:
        db.goods_stock_sum.update({'_id': r['goods_id']}, {'$set':{'instock_time': r['instock_time']}})



def goodsStockSumOnlineTime():
    db = getMongoDBConn().shop
    ##由于库存中间表的数据先存在，可以使用goods_stock_sum中的_id来反查活动结束时间
    goods_stock_sum = db.goods_stock_sum.find({},{"_id":1,"online_time":1})
    for gss in goods_stock_sum:
        #获取该商品所在的所有活动ID
        ids = db.activity_goods.find({"goods_id":gss['_id']},{"activity_id":1})
        activity_id_list = []
        for x in ids:
            activity_id_list.append(x["activity_id"])
        ##根据活动ID获取最后下线时间
        activity_obj = list(db.activity.find({"_id":{"$in":activity_id_list}},{"end_time":1}).sort("end_time",-1).limit(1))

        if activity_obj:

            try:
                end_time = activity_obj[0]["end_time"]
            except:
                end_time = ''
            try:
                online_time = gss["online_time"]
            except:
                online_time = '1979-01-01 00:00:00'
            if end_time and (end_time>online_time):
                 
                db.goods_stock_sum.update({'_id': gss['_id']}, {'$set':{'online_time': end_time}})


    #未上过线的： 不考虑


def goodsStockClearStock(goods_stock_sum_ids=[]):
    db = getMongoDBConn().shop
    if not goods_stock_sum_ids:
        good_stocks = list(db.stock_detail.find({'goods_id': {'$exists': True}}, {"goods_id": 1}))
        goods_ids = [i['goods_id'] for i in good_stocks]
        goods_ids = list(set(goods_ids))
        goods_stock_sum_ids = [i['_id'] for i in db.goods_stock_sum.find({'_id': {'$nin': goods_ids}}, {"_id": 1})]

    for i in goods_stock_sum_ids:
        db.goods_stock_sum.update({'_id': i}, {'$set': {'stock': 0, 'size': []}})


def goodsStockSumInit():
    db = getMongoDBConn().shop
    good_stocks = list(db.stock_detail.find({'goods_id': {'$exists': True}}))

    goods_ids = [i['goods_id'] for i in good_stocks]
    goods_ids = list(set(goods_ids))

    for goods_id in goods_ids:
        goodsStockSumFromId(goods_id, stock_detail=filter(lambda g: g['goods_id'] == goods_id, good_stocks))

    goods_stock_sum_ids = [i['_id'] for i in db.goods_stock_sum.find({'_id': {'$nin': goods_ids}}, {"_id": 1})]
    goodsStockClearStock(goods_stock_sum_ids)


def goodsStockAll():
    '''
    将stock_detail记录， 归入 goods_stock_sum
    跑批脚本， 每小时跑一次，大概耗时20s
    collection: goods_stock_sum
    attr:
        _id: 产品id
        stock： 产品存货
        size： 尺码信息、对应库存
        instock_time： 最新入库时间
        online_time:  最新上线时间

    :return:
    '''
    print getNowUTCtime()
    goodsStockSumInit()

    goodsStockSumInstockTime()
    print getNowUTCtime()

    goodsStockSumOnlineTime()
    print getNowUTCtime()

    goodsStockSumPriceName()

    goodsStockSumPurchaseTime()


def goodsStockSumPriceName():
    #price
    db = getMongoDBConn().shop
    for gs in db.goods_stock_sum.find():
        goods = db.goods.find_one({'_id': gs['_id']})
        if goods:
            dic = {
                'price': goods.get('price', 0),
                'name': goods.get('name', '')
            }
            db.goods_stock_sum.update({'_id': gs['_id']}, {'$set': dic})
        else:
            continue
    print 'goodsStockSumPriceName Done'


def goodsStockSumPurchaseTime():
    sqldb = DBAccess()
    sqldb.dbName = "billing_record_db"

    sql = '''select Max(purchase_time) as purchase_time from new_purchase_list where brand_id = %s'''
    brand_time = {}
    #purchase_time
    db = getMongoDBConn().shop
    for gs in db.goods_stock_sum.find():
        goods = db.goods.find_one({'_id': gs['_id']})

        if goods:
            brand_id = goods.get('brand_id', 0)
            if brand_id:
                if brand_id in brand_time:
                    purchase_time = brand_time.get(brand_id)
                else:
                    purchase_time = sqldb.execQueryAssoc(sql%brand_id)
                    purchase_time = purchase_time[0]["purchase_time"] if purchase_time else ''
                    brand_time[brand_id] = purchase_time

                db.goods_stock_sum.update({'_id': gs['_id']}, {'$set': {'purchase_time': str(purchase_time)}})
            else:
                continue

        else:
            continue
    print 'goodsStockSumPurchaseTime Done'


def getGoodsStock(goods_id):
    '''
    :param goods_id: 获取goods对应的 stock 信息
    :return:
    '''
    db = getMongoDBConn().shop
    return db.goods_stock_sum.find_one({'_id': goods_id})



'''
   activity_goods_order_datas
   脚本初次运行时间点开始
        在线商品购买信息：
        _id 对应 activity_goods._id
        count 对应 购买总数
'''
def activityGoodsOrderDatas(t='m'):
    sqldb = DBAccess()
    sqldb.dbName = "billing_record_db"
    sql = '''select sum(count) as count_sum, product_id from order_goods where product_id in (%s) group by product_id'''

    from shop.models import getAvailableActivityGoodsIdsByCategory
    available_ags_ids = getAvailableActivityGoodsIdsByCategory(category='all')

    sql_per_num = len(available_ags_ids) / 100 + 1

    db = getMongoDBConn().shop

    def update_(r):
        ag_id = int(r['product_id'])
        count = int(r['count_sum'])
        print ag_id, type(ag_id)
        dic = {
            '_id': ag_id,
            'count': count
        }

        db.activity_goods_order_datas.update({'_id': ag_id}, {'$set': dic}, True)

    def sql_100_per_time():
        # test 100/sql
        for i in range(sql_per_num):
            ids = available_ags_ids[i*100: (i+1)*100]
            ids_s = ','.join([str(s) for s in ids])
            result = sqldb.execQueryAssoc(sql%ids_s)
            for r in result:
                update_(r)

    def sql_1_per_time():
        # test 1/sql
        sql = '''select sum(count) as count_sum, product_id from order_goods where product_id=%s group by product_id'''
        for agid in available_ags_ids:
            result = sqldb.execQueryAssoc(sql%agid)
            if result:
                update_(result[0])

    start = datetime.datetime.now()
    if t == 's':
        sql_1_per_time()

    else:
        sql_100_per_time()
    end = datetime.datetime.now()

    print 'last.........', str(end-start)

if __name__ == "__main__":

    goodsStockSumOnlineTime()