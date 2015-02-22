#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getRedisObj, getMongoDBConn,getNowUTCtime, DBAccess, countTime
from utility.UBSclient import *
import datetime
import urlparse


# ##########################################################################
# 删除活动流量中间表今天0点以前的数据
##
# @brief	deleteActivityFlowData 
#
# @return	无
# ##########################################################################
def deleteActivityFlowData():
    nowTime = getNowUTCtime()
    # 获取当天零点时间
    todayTime = '%s 00:00:00' % nowTime[:10]
    # 删除当天零点以前的数据
    condition = { 'range_end_time': { '$lte': todayTime } }
    mongo = getMongoDBConn().shop
    mongo.activity_flow_range.remove(condition)



# ##########################################################################
# 删除商品流量中间表今天0点以前的数据
##
# @brief	deleteActivityGoodsFlowData 
#
# @return	
# ##########################################################################
def deleteActivityGoodsFlowData():
    nowTime = getNowUTCtime()
    # 获取当天零点时间
    todayTime = '%s 00:00:00' % nowTime[:10]
    # 删除当天零点以前的数据
    condition = { 'range_end_time': { '$lte': todayTime } }
    mongo = getMongoDBConn().shop
    mongo.activity_goods_flow_range.remove(condition)





# ##########################################################################
# 根据活动ID和活动开始时间查询订单量和交易额，循环查询太慢，该方法已放弃
##
# @brief	getActivityOrderCountAndTotal 
#
# @param	activityId		活动ID
# @param	activityStartTime	活动开始时间
#
# @return	(订单量，交易额)
# ##########################################################################
def getActivityOrderCountAndTotal(activityId, activityStartTime):
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select sum(total_pay) as price from orders where order_status in ('pending', 'confirmed') and event_ids like '%%%s%%' and create_time > '%s'" % (activityId, activityStartTime)
    res = db.execQueryAssoc(sql)
    total = 0
    if res and res[0]['price'] != None:
        total = float("%.2f"  % res[0]['price'])

    sql = "select order_no from orders where order_status in ('pending', 'confirmed') and event_ids like '%%%s%%' and create_time > '%s' group by order_no" % (activityId, activityStartTime)
    res = db.execQueryAssoc(sql)
    orderCount = len(res)
    #orderNoList = [ r['order_no'] for r in res ]

    #print 'getOrderCountAndTotal orderCount total orderNoList'
    #print orderCount, total
    #print orderNoList

    return orderCount, total





# ##########################################################################
# 获取一段时间的订单量和交易额，循环查询速度慢，已放弃使用
##
# @brief	getRangeActivityOrderCountAndTotal 
#
# @param	activityId      活动ID
# @param	startTime       开始时间
# @param	endTime         结束时间
#
# @return	(订单量，交易额)
# ##########################################################################
def getRangeActivityOrderCountAndTotal(activityId, startTime, endTime):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select sum(total_pay) as price from orders where order_status in ('pending', 'confirmed') and event_ids like '%%%s%%' and create_time >= '%s' and create_time < '%s'" % (activityId, startTime, endTime)
    res = db.execQueryAssoc(sql)
    total = 0
    if res and res[0]['price'] != None:
        total = float("%.2f" % res[0]['price'])

    sql = "select order_no from orders where order_status in ('pending', 'confirmed') and event_ids like '%%%s%%' and create_time >= '%s' and create_time < '%s'" % (activityId, startTime, endTime)
    res = db.execQueryAssoc(sql)
    orderCount = len(res)
    return orderCount, total


def getGoodsPurchasePrice(goodsId, size):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select purchase_price from new_purchase where product_id = '%s' and size = '%s'" % (goodsId, size)







# ##########################################################################
# 获取时间段的订单，并找出商品对应的成交量，订单量，交易额
##
# @brief	getRangeActvityGoodsOrderCountAndTotalByTime 
#
# @param	startTime   开始时间
# @param	endTime     结束时间
#
# @return	商品list，每个元素是dict，key是商品ID，value是list记录信息
# ##########################################################################
def getRangeActvityGoodsOrderCountAndTotalByTime(startTime, endTime):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select create_time, event_ids, prices, counts, product_ids from orders where create_time > '%s' and create_time < '%s'" % (startTime, endTime)
    result = db.execQueryAssoc(sql)
    results = {}
    for r in result:
        eventIds = r['event_ids'][:-1].split('_')
        prices = r['prices'][:-1].split('_')
        counts = r['counts'][:-1].split('_')
        productIds = r['product_ids'][:-1].split('_')
        length = len(eventIds)
        index = 0
        while index < length:
            productId = productIds[index]
            if results.get(productId):
                tmp = results.get(productId)
                tmp[0] += int(counts[index]) * float(prices[index])
                tmp[1] += int(counts[index])
            else:
                price = float(prices[index]) * int(counts[index])
                count = int(counts[index])
                results[productId] = [price, count, 0]
            index += 1
        for pid in set(productIds):
            tmp = results.get(str(pid))
            if tmp:
                tmp[2] += 1

    return results






# ##########################################################################
# 找出商品对应的成交量，订单量，交易额
##
# @brief	getActvityGoodsOrderCountAndTotalByTime 
#
# @param	activityIdsAndStartTimeDict	活动list，包含活动ID和活动开始时间
# @param	minimumStartTime		所有活动中开始时间最早的时间
#
# @return	商品list，每个元素是dict，key是商品ID，value是list记录信息
# ##########################################################################
def getActvityGoodsOrderCountAndTotalByTime(activityIdsAndStartTimeDict, minimumStartTime, endTime):
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select order_status, create_time, event_ids, prices, counts, product_ids from orders where create_time >= '%s' and create_time < '%s'" \
                    % (minimumStartTime, endTime)
    result = db.execQueryAssoc(sql)
    results = {}
    # 有效订单状态(pending:等待审核,confirmed:审核通过,...)
    validOrderStatus = ("pending","paid","confirmed","picking","picked","packing","packed","delivering",
                  "part_picked","part_packed","part_finished","part_delivering","part_auto_sign",
                  )
    nowTime = datetime.datetime.now()
    todayTime = nowTime.strftime("%Y-%m-%d 00:00:00")
    rangeValidOrdersDict = {}
    for r in result:
        eventIds = r['event_ids'][:-1].split('_')
        prices = r['prices'][:-1].split('_')
        counts = r['counts'][:-1].split('_')
        productIds = r['product_ids'][:-1].split('_')
        length = len(eventIds)
        index = 0
        createTime = str(r['create_time'])
        orderStatus = str(r['order_status'])
        while index < length:
            activityId = str(eventIds[index])
            activityStartTime = activityIdsAndStartTimeDict.get(activityId, '')
            if createTime > activityStartTime:
                productId = productIds[index]
                if results.get(productId):
                    tmp = results.get(productId)
                    tmp[0] += int(counts[index]) * float(prices[index])
                    tmp[1] += int(counts[index])
                else:
                    price = float(prices[index]) * int(counts[index])
                    count = int(counts[index])
                    validOrderCount = 0
                    results[productId] = [price, count, 0, validOrderCount]
            index += 1
        for pid in set(productIds):
            tmp = results.get(str(pid))
            if tmp:
                tmp[2] += 1
                if orderStatus in validOrderStatus:
                    # 累计有效订单量
                    tmp[3] += 1
                    if createTime >= todayTime:
                        rangeTime = '%s0:00' % createTime[:15]
                        rangeID = '%s_%s' % (pid, rangeTime)
                        if rangeValidOrdersDict.get(rangeID):
                            rangeValidOrdersDict[rangeID] += 1
                        else:
                            validOrderCount = 1
                            rangeValidOrdersDict[rangeID] = validOrderCount

    return results, rangeValidOrdersDict






# ##########################################################################
# 找出活动对应的订单量，交易额
##
# @brief	getActivityOrderCountAndTotalByTime 
#
# @param	activityIdsAndStartTimeDict	活动list，包含活动ID和活动开始时间
# @param	minimumStartTime		所有活动开始时间最早的时间
#
# @return	活动list，每个元素是dict，key是活动ID，value是list记录信息
# ##########################################################################
def getActivityOrderCountAndTotalByTime(activityIdsAndStartTimeDict, minimumStartTime, endTime):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select order_status, create_time, event_ids, prices, counts, product_ids from orders where create_time >= '%s' and create_time < '%s'" \
	              % (minimumStartTime, endTime)
    result = db.execQueryAssoc(sql)
    results = {}
    # 有效订单状态(pending:等待审核,confirmed:审核通过,...)
    validOrderStatus = ("pending","paid","confirmed","picking","picked","packing","packed","delivering",
		          "part_picked","part_packed","part_finished","part_delivering","part_auto_sign",
		          )
    nowTime = datetime.datetime.now()
    todayTime = nowTime.strftime("%Y-%m-%d 00:00:00")
    rangeValidOrder = {}
    for r in result:
        eventIds = r['event_ids'][:-1].split('_')
        prices = r['prices'][:-1].split('_')
        counts = r['counts'][:-1].split('_')
        length = len(eventIds)
        index = 0
        createTime = str(r['create_time'])
        orderStatus = str(r['order_status'])
        while index < length:
            activityId = str(eventIds[index])
            activityStartTime = activityIdsAndStartTimeDict.get(activityId, '')
            if createTime > activityStartTime:
                if results.get(activityId):
                    tmp = results.get(activityId)
                    tmp[0] += int(counts[index]) * float(prices[index])
                else:
                    price = float(prices[index]) * int(counts[index])
                    count = 0
                    validOrderCount = 0
                    results[activityId] = [price, count, validOrderCount]
            index += 1

        for aid in set(eventIds):
            tmp = results.get(str(aid))
            if tmp:
                tmp[1] += 1
                if orderStatus in validOrderStatus:
                    tmp[2] += 1
                    # 今天内的有效订单
                    if createTime >= todayTime:
                        rangeTime = '%s0:00' % createTime[:15]
                        rangeID = '%s_%s' % (aid, rangeTime)
                        if rangeValidOrder.get(rangeID):
                            rangeValidOrder[rangeID] += 1
                        else:
                            validOrderCount = 1
                            rangeValidOrder[rangeID] = validOrderCount

    return results, rangeValidOrder






# ##########################################################################
# 找出对应时间段的活动对应的订单量，交易额
##
# @brief	getRangeActivityOrderCountAndTotalByTime 
#
# @param	startTime	开始时间
# @param	endTime	        结束时间
#
# @return	活动list，每个元素是dict，key是活动ID，value是list记录信息
# ##########################################################################
def getRangeActivityOrderCountAndTotalByTime(startTime, endTime):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select order_no, event_ids, prices, counts, product_ids from orders where create_time >= '%s' and create_time < '%s'" % (startTime, endTime)
    res = db.execQueryAssoc(sql)
    
    activityIds = []
    results = {}
    for r in res:
        eventIds = r['event_ids'][:-1].split('_')
        prices = r['prices'][:-1].split('_')
        counts = r['counts'][:-1].split('_')
        length = len(eventIds)
        index = 0
        while index < length:
            activityId = str(eventIds[index])
            if results.get(activityId):
                tmp = results.get(activityId)
                tmp[0] += int(counts[index]) * float(prices[index])
            else:
                price = float(prices[index]) * int(counts[index])
                count = 0
                results[activityId] = [price, count]
            index += 1
        for aid in set(eventIds):
            tmp = results.get(str(aid))
            if tmp:
                tmp[1] += 1

    return results





# ##########################################################################
# 计算在线时长，测试用
##
# @brief	getOnlineTime 
#
# @param	activityStartTime	活动开始时间
# @param	activityEndTime		活动结束时间
#
# @return	在线时长
# ##########################################################################
def getOnlineTime(activityStartTime, activityEndTime):
    # 计算在线总时长
    activityStartTime = r['start_time']
    activityEndTime = r['end_time']
    onlineTime = ''
    if activityStartTime and activityEndTime:
        activityStartTime = datetime.datetime.strptime(activityStartTime, '%Y-%m-%d %H:%M:%S')
        activityEndTime = datetime.datetime.strptime(activityEndTime, '%Y-%m-%d %H:%M:%S')
        nowTime = datetime.datetime.today()
        if activityEndTime > nowTime:
            delta = nowTime - activityStartTime
        else:
            delta = activityEndTime - activityStartTime
        onlineDay = delta.days
        onlineHour = delta.seconds / 3600
        if onlineDay >= 0 and onlineHour >= 0:
            onlineTime = str(onlineDay) + '天' + str(onlineHour) + '小时'
    #print 'getOnlineTime onlineTime'
    #print onlineTime
    #return onlineTime






# ##########################################################################
# 计算 点击量/曝光量，订单量/曝光量，订单量/点击量
##
# @brief	getConversion 
#
# @param	click	点击量
# @param	show	曝光量
# @param	count	订单量
#
# @return	(点击量/曝光量,订单量/曝光量,订单量/点击量)
# ##########################################################################
def getConversion(click, show, count):
    conversion = float(click) / float(show) if show else 0
    showConversion = float(count) / float(show) if show else 0
    clickConversion = float(count) / float(click) if click else 0
    #print 'getConversion conversion showConversion clickConversion'
    #print conversion, showConversion, clickConversion
    return conversion, showConversion, clickConversion






# ##########################################################################
# 获取所有在线活动商品ID，对应的活动开始时间和结束时间
##
# @brief	getAvailableActivityGoodsIds 
#
# @param	time	时间
#
# @return	(商品ID的list，活动时间list)
# ##########################################################################
def getAvailableActivityGoodsIds(time):
    mongo = getMongoDBConn().shop
    condition = { 'status': 3, 'start_time': {'$lt': time}, 'end_time': {'$gt': time}, 'goods_id': {'$ne': []} }
    column = { '_id': 1, 'goods_id': 1, 'start_time': 1, 'end_time': 1 }
    result = mongo.activity.find(condition, column).sort('start_time', -1)
    activityGoodsIds = []
    activityTime = []
    for r in result:
        activityGoodsIds += r.get('goods_id', [])
        tmp = {}
        tmp['activityId'] = r['_id']
        tmp['activityStartTime'] = r['start_time']
        tmp['activityEndTime'] = r['end_time']
        activityTime.append(tmp)

    return activityGoodsIds, activityTime







# ##########################################################################
# 测试用
##
# @brief	test 
#
# @param	activityGoodIds
#
# @return	
# ##########################################################################
def test(activityGoodIds):
    tmp = sorted(activityGoodIds, reverse = True)
    activityGoodIds = ','.join([str(r) for r in activityGoodIds])
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select product_id, original_goods_id, price, product_size, refund_time from order_goods where product_id in (%s) order by product_id desc" % activityGoodIds
    result = db.execQueryAssoc(sql)
    index = 0
    resLen = len(result)
    agoods = []
    for r in tmp:
        agdict = {}
        activityGoodId = r
        priceSum = 0
        goodCount = 0
        returnOfGoodCount = 0
        productSize = ''
        purchasePrice = ''
        goodId = ''
        while index < resLen and result and result[index]['product_id'] == activityGoodId:
            priceSum += result[index]['price']
            goodCount += 1
            productSize = result[index]['product_size']
            goodId = result[index]['original_goods_id']
            if result[index]['refund_time']:
                returnOfGoodCount += 1
            index += 1
        if productSize and goodId:
            sql = "select purchase_price from new_purchase where product_id = %s and size = '%s' limit 1" % (goodId, productSize)
            res = db.execQueryAssoc(sql)
            if res and res[0]['purchase_price'] != None:
                purchasePrice = res[0]['purchase_price']

        agdict['id'] = activityGoodId
        agdict['total'] = priceSum
        agdict['good_count'] = goodCount
        agdict['return_of_goods'] = returnOfGoodCount
        agdict['purchase_price'] = purchasePrice
        agoods.append(agdict)
        if activityGoodId == 10027319 or activityGoodId == 10027302:
            print agdict
    return agoods








# ##########################################################################
# 获取商品成交量，采购价，交易额，退货量，循环查询速度慢，放弃使用
##
# @brief	getActivityGoodCountAndTotal 
#
# @param	activityId	活动ID
# @param	activityGoodId	商品ID
#
# @return	(成交量，采购价，交易额，退货量)
# ##########################################################################
def getActivityGoodCountAndTotal(activityId, activityGoodId):
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select price, product_size from order_goods where event_id = %s and original_goods_id = %s" % (activityId, activityGoodId)
    result = db.execQueryAssoc(sql)
    # 成交量
    goodCount = len(result)
    # 根据尺码和商品ID获取采购价
    productSize = ''
    purchasePrice = ''
    if result and result[0]['product_size'] != None:
        productSize = result[0]['product_size']
    if productSize:
        sql = "select purchase_price from new_purchase where product_id = %s and size = '%s' limit 1" % (activityGoodId, productSize)
        res = db.execQueryAssoc(sql)
        if res and res[0]['purchase_price'] != None:
            purchasePrice = res[0]['purchase_price']
    # 交易额
    priceSum = 0
    for r in result:
        priceSum += r['price']
    # 退货量
    returnOfGood = 0
    sql = "select count(*) as return_of_goods from order_goods where refund_time != '0000-00-00 00:00:00' and event_id = %s and original_goods_id = %s" % (activityId, activityGoodId)
    res = db.execQueryAssoc(sql)
    if res and res[0]['return_of_goods'] != None:
        returnOfGood = res[0]['return_of_goods']

    return goodCount, purchasePrice, priceSum, returnOfGood







# ##########################################################################
# 获取商品流量和订单等数据，并插入中间表
##
# @brief	getAvailableActivityGoodData 
#
# @param	nowTime		当前时间
# @param	startTime       开始时间
# @param	endTime		结束时间
#
# @return	无
# ##########################################################################
@countTime
def getAvailableActivityGoodData(nowTime, startTime, endTime):
    #nowTime = getNowUTCtime()
    # 获取所有的活动商品ID和活动时间
    activityGoodsIds, activityTime = getAvailableActivityGoodsIds(time = nowTime)

    # 查询活动商品信息
    mongo = getMongoDBConn().shop
    condition = { '_id': { '$in': activityGoodsIds } }
    column = { '_id': 1, 'name': 1, 'activity_id': 1, 'brand_id': 1, 'brand_name': 1, 'goods_id': 1, 'goods_source': 1, 'goods_type': 1,
                       'image': 1, 'leimu_id': 1, 'market_price': 1, 'price': 1 }
    activityGoods = list(mongo.activity_goods.find(condition, column).sort('_id', -1))
    print len(activityGoods)

    for ag in activityGoods:
        activityId = ag['activity_id']
        for acTime in activityTime:
            if activityId == acTime['activityId']:
                ag['activity_start_time'] = acTime['activityStartTime']
                ag['activity_end_time'] = acTime['activityEndTime']
                break


    # 获取所有在线活动ID和开始时间
    activityIdsAndStartTimeDict = {}
    minimumStartTime = '2099-12-31 23:59:59'
    for r in activityGoods:
        activityId = str(r['activity_id'])
        activityStartTime = r['activity_start_time']
        activityIdsAndStartTimeDict[activityId] = str(activityStartTime)
        if activityStartTime < minimumStartTime:
            minimumStartTime = activityStartTime

    # 获取订单量和交易额
    orderGoodsDict, rangeValidOrdersDict = getActvityGoodsOrderCountAndTotalByTime(activityIdsAndStartTimeDict = activityIdsAndStartTimeDict, 
                                                                                                                                            minimumStartTime = minimumStartTime, endTime = endTime)

    # 获取点击量和曝光量
    activityGoodsIds = [ r['_id'] for r in activityGoods ]
    ubsclient = UBSclient()
    activityGoodsClicks, activityGoodsShows = ubsclient.queryGoodsClickAndShow(activityGoodsIDs = activityGoodsIds)

    # 获取时间段点击量和曝光量
    rangeActivityGoodsClicks, rangeActivityGoodsShows = ubsclient.queryGoodsClickAndShowByTime(goodsIds = activityGoodsIds, start = startTime, end = endTime)
    rangeIndex = 0

    # 获取时间段活动对应订单数和交易额
    rangeOrderGoodsDict = getRangeActvityGoodsOrderCountAndTotalByTime(startTime = startTime, endTime = endTime) 

    # 查出所有活动商品数据
    activityGoodIds = ','.join( [ str(r['_id']) for r in activityGoods ])
    db = DBAccess()
    db.dbName = 'billing_record_db'
    sql = "select order_no, create_time, product_id, original_goods_id, price, product_size, refund_time from order_goods where product_id in (%s) order by product_id desc" % activityGoodIds
    result = db.execQueryAssoc(sql)
    resIndex = 0
    resLen = len(result)
    index = 0
    for r in activityGoods:
        # 获取成交量,采购价,交易额,退货量
        activityGoodId = r['_id']
        goodId = r['goods_id']
        # 交易额
        priceSum = 0
        # 成交量
        goodCount = 0
        orderCount = 0
        validOrderCount = 0
        # 退货量
        returnOfGoodCount = 0
        productSize = ''
        # 采购价
        purchasePrice = ''

        if orderGoodsDict.get(str(activityGoodId)):
            t = orderGoodsDict.get(str(activityGoodId), [0, 0, 0])
            priceSum = t[0]
            goodCount = t[1]
            orderCount = t[2]
            validOrderCount = t[3]


        # 时间段
        rangePriceSum = 0
        rangeGoodCount = 0
        rangeOrderCount = 0
        rangeReturnOfGoodCount = 0

        if rangeOrderGoodsDict.get(str(activityGoodId)):
            t = rangeOrderGoodsDict.get(str(activityGoodId))
            rangePriceSum = t[0]
            rangeGoodCount = t[1]
            rangeOrderCount = t[2]



        # rangeOrderCount = set()

        # # 商品对应的活动开始时间
        # activityStartTime = r['activity_start_time']
        # orderCount = set()
        # orderCreateTime = str(result[resIndex]['create_time'])
        # while resIndex < resLen and result and result[resIndex]['product_id'] == activityGoodId and orderCreateTime > activityStartTime:
        #     priceSum += result[resIndex]['price']
        #     orderNo = result[resIndex]['order_no']
        #     orderCount.add(orderNo)
        #     goodCount += 1
        #     productSize = result[resIndex]['product_size']
        #     if result[resIndex]['refund_time']:
        #         returnOfGoodCount += 1
        #         if startTime <= orderCreateTime < endTime:
        #             rangeReturnOfGoodCount += 1

        #     if startTime <= orderCreateTime < endTime:
        #         rangePriceSum += result[resIndex]['price']
        #         rangeOrderCount.add(orderNo)
        #         rangeGoodCount += 1
        #     resIndex += 1

        if productSize and goodId:
            sql = "select purchase_price from new_purchase where product_id = %s and size = '%s' limit 1" % (goodId, productSize)
            res = db.execQueryAssoc(sql)
            if res and res[0]['purchase_price'] != None:
                purchasePrice = res[0]['purchase_price']
        
        #goodCount, purchasePrice, priceSum, returnOfGood = getActivityGoodCountAndTotal(activityId = activityId, activityGoodId = activityGoodId)
        # orderCount = len(orderCount)
        # rangeOrderCount = len(rangeOrderCount)
        r['good_count'] = goodCount
        r['order_count'] = orderCount
        r['valid_order_count'] = validOrderCount
        r['purchase_price'] = purchasePrice
        r['total'] = priceSum
        r['return_of_goods'] = returnOfGoodCount

        # 获取类目名称
        leimuId = r.get('leimu_id', 0)
        res = mongo.leimu.find_one({ '_id': leimuId })
        r['leimu_name'] = res['name'] if res else ''

        # 计算转化率
        show = activityGoodsShows[index] if activityGoodsShows[index] != None else 0
        click = activityGoodsClicks[index] if activityGoodsClicks[index] != None else 0
        r['show'] = int(show)
        r['click'] = int(click)
        index += 1
        conversion, showConversion, clickConversion = getConversion(click = click, show = show, count = orderCount)
        r['conversion'] = conversion
        r['show_conversion'] = showConversion
        r['click_conversion'] = clickConversion

        # 插入中间表
        mongo.activity_goods_flow.save(r)

        # if activityGoodId == 10114890:
        #     print r


        # 时间段数据
        tmp = r
        click = rangeActivityGoodsClicks[rangeIndex] if rangeActivityGoodsClicks[rangeIndex] != None else 0
        show = rangeActivityGoodsShows[rangeIndex] if rangeActivityGoodsShows[rangeIndex] != None else 0
        rangeIndex += 1
        tmp['click'] = int(click)
        tmp['show'] = int(show)
        tmp['activity_goods_id'] = activityGoodId
        tmp['_id'] = '%s_%s' % (activityGoodId, startTime)
        tmp['range_start_time'] = startTime
        tmp['range_end_time'] = endTime
        tmp['order_count'] = rangeOrderCount
        tmp['good_count'] = rangeGoodCount
        tmp['total'] = rangePriceSum
        tmp['return_of_goods'] = rangeReturnOfGoodCount
        conversion, showConversion, clickConversion = getConversion(click = click, show = show, count = rangeOrderCount)
        tmp['conversion'] = conversion
        tmp['show_conversion'] = showConversion
        tmp['click_conversion'] = clickConversion

        tmp['valid_order_count'] = 0
        tmp['valid_order_conversion'] = 0


         # 插入中间表
        mongo.activity_goods_flow_range.save(tmp)

        # if activityGoodId == 10114890:
        #     print tmp


    updateActivityGoodsTodayValidOrderCount(rangeValidOrdersDict = rangeValidOrdersDict)


    # 更新redis有效订单量排序
    updateActivityGoodsValidOrderSortToRedis(endTime = endTime)



def updateActivityGoodsTodayValidOrderCount(rangeValidOrdersDict):
    activityGoodsIds = [ key for key in rangeValidOrdersDict ]
    showDict = getActivityGoodsShowById(activityGoodsIds = activityGoodsIds)
    mongo = getMongoDBConn().shop
    for key in rangeValidOrdersDict:
        validOrderCount = rangeValidOrdersDict[key]
        condition = { '_id': key }
        # 更新有效订单量和有效订单量/曝光量
        show = showDict.get(key)
        validOrderConversion = float(validOrderCount) / show if show else 0
        setValue = { '$set': { 'valid_order_count': validOrderCount, 'valid_order_conversion': validOrderConversion } }
        mongo.activity_goods_flow_range.update(condition, setValue)




def getActivityGoodsShowById(activityGoodsIds):
    mongo = getMongoDBConn().shop
    condition = { '_id': { '$in': activityGoodsIds } }
    column = { '_id': 1, 'show': 1 }
    results = list(mongo.activity_goods_flow_range.find(condition, column))
    resultsDict = {}
    for r in results:
        resultsDict[str(r['_id'])] = int(r['show'])

    return resultsDict



def updateActivityTodayOrderCount(rangeValidOrdersDict):
    activityIds = [ key for key in rangeValidOrdersDict ]
    showDict = getActivityShowById(activityIds = activityIds)
    mongo = getMongoDBConn().shop
    for key in rangeValidOrdersDict:
        validOrderCount = rangeValidOrdersDict[key]
        condition = { '_id': key }
        # 更新有效订单量和有效订单量/曝光量
        show = showDict.get(key)
        validOrderConversion = float(validOrderCount) / show if show else 0
        setValue = { '$set': { 'valid_order_count': validOrderCount, 'valid_order_conversion': validOrderConversion } }
        mongo.activity_flow_range.update(condition, setValue)


def getActivityShowById(activityIds):
    mongo = getMongoDBConn().shop
    condition = { '_id': { '$in': activityIds } }
    column = { '_id': 1, 'show': 1 }
    results = list(mongo.activity_flow_range.find(condition, column))
    resultsDict = {}
    for r in results:
        resultsDict[str(r['_id'])] = int(r['show'])

    return resultsDict



# ##########################################################################
# 提取活动区间最高价格(如从68元~112元中提取出112)
##
# @brief    promotionToPrice 
#
# @param    promotion   包含价格的字符串
#
# @return   区间最高价   
# ##########################################################################
def promotionToPrice(promotion):
    import re
    promotion = str(promotion)
    r = re.findall(r'[\d,\.]{1,6}', promotion)
    price = 10000
    if r:
        price = float(r[-1])
    return price






def getRangeActivityGoodValidOrders(queryStartTime, queryEndTime):
    condition = { 'range_start_time': { '$gte': queryStartTime }, 'range_end_time': { '$lte': queryEndTime } }
    mongo = getMongoDBConn().shop
    result = list(mongo.activity_goods_flow_range.find(condition).sort('activity_goods_id', -1))

    # 合并数据
    index = 0
    resLen = len(result)
    queryResult = []
    while index < resLen:
        activityGoodId = int(result[index]['activity_goods_id'])
        validOrderCount = 0
        tmp = result[index]
        while index < resLen and result[index]['activity_goods_id'] == activityGoodId:
            validOrderCount += int(result[index].get('valid_order_count', 0))
            index += 1

        tmp['valid_order_count'] = validOrderCount
        tmp['_id'] = activityGoodId

        queryResult.append(tmp)

    queryResult.sort(key = lambda x : (-x['valid_order_count'], x['price']))

    return queryResult




def getRangeActivityValidOrders(queryStartTime, queryEndTime):
    condition = { 'range_start_time': { '$gte': queryStartTime }, 'range_end_time': { '$lte': queryEndTime } }
    mongo = getMongoDBConn().shop
    result = list(mongo.activity_flow_range.find(condition).sort('activity_id', -1))

    # 合并数据
    index = 0
    resLen = len(result)
    queryResult = []
    while index < resLen:
        activityId = int(result[index]['activity_id'])
        promotion = str(result[index]['promotion'])
        price = promotionToPrice(promotion = promotion)
        validOrderCount = 0
        tmp = result[index]
        while index < resLen and result[index]['activity_id'] == activityId:
            validOrderCount += int(result[index].get('valid_order_count', 0))
            index += 1

        tmp['_id'] = activityId
        tmp['price'] = price
        tmp['valid_order_count'] = validOrderCount

        queryResult.append(tmp)

    queryResult.sort(key = lambda x : (-x['valid_order_count'], x['price']))
    return queryResult




def updateActivityValidOrderSortToRedis(endTime):
    d = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    delta = datetime.timedelta(hours = -0.5)
    queryStartTime = (d + delta).strftime('%Y-%m-%d %H:%M:%S')
    queryEndTime = endTime
    results = getRangeActivityValidOrders(queryStartTime = queryStartTime, queryEndTime = queryEndTime)
    r = getRedisObj()
    redisKey = 'activity_valid_orders_ids'
    redisKeyBackup = 'activity_valid_orders_ids_back_up'

    activityIds = r.lrange(redisKey, 0, -1)
    r.delete(redisKeyBackup)
    if activityIds:
        r.rpush(redisKeyBackup, *activityIds)

    activityIds = [ str(x['_id']) for x in results ]
    if activityIds:
        r.delete(redisKey)
        r.rpush(redisKey, *activityIds)


def updateActivityGoodsValidOrderSortToRedis(endTime):
    d = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    delta = datetime.timedelta(hours = -0.5)
    queryStartTime = (d + delta).strftime('%Y-%m-%d %H:%M:%S')
    queryEndTime = endTime
    results = getRangeActivityGoodValidOrders(queryStartTime = queryStartTime, queryEndTime = queryEndTime)
    r = getRedisObj()
    redisKey = 'activity_goods_valid_orders_ids'
    redisKeyBackup = 'activity_goods_valid_orders_ids_back_up'

    activityGoodsIds = r.lrange(redisKey, 0, -1)
    r.delete(redisKeyBackup)
    if activityGoodsIds:
        r.rpush(redisKeyBackup, *activityGoodsIds)

    activityGoodsIds = [ str(x['_id']) for x in results ]
    if activityGoodsIds:
        r.delete(redisKey)
        r.rpush(redisKey, *activityGoodsIds)



# ##########################################################################
# 获取活动流量和订单等数据，并插入中间表
##
# @brief	getAvailableActivityIdsByTime 
#
# @param	time		当前时间
# @param	startTime	开始时间
# @param	endTime 	结束时间
#
# @return	无
# ##########################################################################
def getAvailableActivityIdsByTime(time, startTime, endTime):
    mongo = getMongoDBConn().shop
    condition = { 'status': 3, 'start_time': {'$lt': time}, 'end_time': {'$gt': time} }
    column = { '_id': 1, 'brand_name': 1, 'brand_id': 1, 'is_promotion': 1, 'category': 1, 'goods_id': 1, 'is_unit': 1,
                       'leimu_id': 1, 'start_time': 1, 'end_time': 1, 'banner': 1, 'name': 1, 'promotion': 1, 'desc': 1, 'status': 1 }
    result = mongo.activity.find(condition, column).sort('start_time', -1)
    result = list(result)

    # 获取所有在线活动ID和开始时间
    activityIdsAndStartTimeDict = {}
    minimumStartTime = '2099-12-31 23:59:59'
    for r in result:
        activityId = str(r['_id'])
        activityStartTime = r['start_time']
        activityIdsAndStartTimeDict[activityId] = str(activityStartTime)
        if activityStartTime < minimumStartTime:
            minimumStartTime = activityStartTime

    # 获取订单量和交易额
    ordersDict, rangeValidOrdersDict = getActivityOrderCountAndTotalByTime(activityIdsAndStartTimeDict = activityIdsAndStartTimeDict,
                                                                                                                        minimumStartTime = minimumStartTime, endTime = endTime)

    # 获取所有活动ID
    activityIDs = [ r['_id'] for r in result ]

    ubsclient = UBSclient()
    # 获取活动曝光量和点击量
    activityClicks, activityShows = ubsclient.queryActivityClickAndShow(activityIds = activityIDs)
    index = 0

    # 获取时间段活动曝光量和点击量
    rangeActivityClicks, rangeActivityShows = ubsclient.queryActivityClickAndShowByTime(activityId = activityIDs, start = startTime, end = endTime)
    rangeIndex = 0

    # 获取活动开始后对应订单数和交易额
    #ordersDict = getActivityOrderCountAndTotalByTime(activityStartTime = activityStartTime)

    # 获取时间段活动对应订单数和交易额
    rangeOrdersDict = getRangeActivityOrderCountAndTotalByTime(startTime = startTime, endTime = endTime) 

    for r in result:
        activityId = r['_id']
        # 获取订单量和交易额
        activityStartTime = r.get('start_time', '')
        #orderCount, total = getActivityOrderCountAndTotalByTime(activityId = activityId, activityStartTime = activityStartTime)
        orderCount = 0
        validOrderCount = 0
        total = 0
        if ordersDict.get(str(activityId)):
            t = ordersDict.get(str(activityId))
            total = t[0]
            orderCount = t[1]
            validOrderCount = t[2]
        r['order_count'] = orderCount
        r['valid_order_count'] = validOrderCount
        r['total'] = total
        # 计算转化率
        click = activityClicks[index] if activityClicks[index] != None else 0
        show = activityShows[index] if activityShows[index] != None else 0
        r['click'] = int(click)
        r['show'] = int(show)
        index += 1
        conversion, showConversion, clickConversion = getConversion(click = click, show = show, count = orderCount)
        r['conversion'] = conversion
        r['show_conversion'] = showConversion
        r['click_conversion'] = clickConversion
        r['valid_order_conversion'] = float(validOrderCount) / int(show) if show else 0
        # 获取图片和图片ID
        image = r.get('banner') if r else ''
        image = image[0] if image else ''
        r['image'] = image
        url = urlparse.urlparse(image)
        r['imageId'] = url.path

        # 插入中间表
        mongo.activity_flow.save(r)

        # if activityId == 4939:
        #     print r


        # 获取时间段数据
        tmp = r
        click = rangeActivityClicks[rangeIndex] if rangeActivityClicks != None else 0
        show = rangeActivityShows[rangeIndex] if rangeActivityShows != None else 0
        rangeIndex += 1
        tmp['click'] = int(click)
        tmp['show'] = int(show)
        tmp['activity_id'] = activityId
        tmp['_id'] = "%s_%s" % (activityId, startTime)
        tmp['range_start_time'] = startTime
        tmp['range_end_time'] = endTime
        #rangeOrderCount, rangeTotal = getRangeActivityOrderCountAndTotal(activityId = activityId, startTime = startTime, endTime = endTime)
        rangeOrderCount = 0
        rangeTotal = 0
        if rangeOrdersDict.get(str(activityId)):
            t = rangeOrdersDict.get(str(activityId), [0, 0])
            rangeTotal = t[0]
            rangeOrderCount = t[1]
        tmp['order_count'] = rangeOrderCount
        tmp['total'] = rangeTotal
        conversion, showConversion, clickConversion = getConversion(click = click, show = show, count = rangeOrderCount)
        tmp['conversion'] = conversion
        tmp['show_conversion'] = showConversion
        tmp['click_conversion'] = clickConversion

        tmp['valid_order_count'] = 0
        tmp['valid_order_conversion'] = 0

        # 插入中间表
        mongo.activity_flow_range.save(tmp)

        # if activityId == 4939:
        #     print tmp
        

    # 更新中间表有效订单量
    updateActivityTodayOrderCount(rangeValidOrdersDict = rangeValidOrdersDict)


    # 更新redis有效订单量排序
    updateActivityValidOrderSortToRedis(endTime = endTime)
    #print 'getAvailableActivityIdsByTime result:'
    #print result







# ##########################################################################
# 调用getAvailableActivityIdsByTime获取活动流量和订单等数据插入中间表
##
# @brief	getAvailableActivityData 
#
# @param	nowTime		当前时间
# @param	startTime	开始时间
# @param	endTime		结束时间
#
# @return	
# ##########################################################################
@countTime
def getAvailableActivityData(nowTime, startTime, endTime):
    getAvailableActivityIdsByTime(time = nowTime, startTime = startTime, endTime = endTime)









if __name__ == '__main__':
    nowTime = getNowUTCtime()
    # 上10分钟时间
    t = '%s0:00' % nowTime[:15]
    d = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    delta = datetime.timedelta(minutes = -10)
    startTime = (d + delta).strftime('%Y-%m-%d %H:%M:%S')
    endTime = d.strftime('%Y-%m-%d %H:%M:%S') 
    # 更新商品流量数据
    getAvailableActivityGoodData(nowTime = nowTime, startTime = startTime, endTime = endTime)
    # 更新活动流量数据
    getAvailableActivityData(nowTime = nowTime, startTime = startTime, endTime = endTime)
    #return
    #activityGoodIds = getAvailableActivityGoodsIds(time = getNowUTCtime())
    #print len(activityGoodIds)
    #test(activityGoodIds = activityGoodIds)
    #getAvailableActivityIdsData()
