#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getRedisObj, getMongoDBConn,getNowUTCtime, DBAccess, countTime
import datetime

@countTime
def getOrdersData(startTime, endTime):
    sql = "select uid, order_no, order_status, phone, human_address, receiver_name, create_time, prices, counts, \
              cargo_fee, paid_by_coupon, paid_by_wallet, paid_by_hercoin, total_pay, reserved_2 \
              from orders where create_time >= '%s' and create_time <= '%s' order by create_time desc" % (startTime, endTime)
    print sql
    db = DBAccess()
    db.dbName = "billing_record_db"
    orderResult = db.execQueryAssoc(sql) 
    print "orderResult count : %s" % len(orderResult)
    return orderResult

@countTime
def getChatMsgs(userUID, kefuUID, startTime, endTime):
    condition = {"from": {"$in": kefuUID}, "to":{"$in": userUID}, "create_time": {"$gte": startTime, "$lte": endTime }}
    db = getMongoDBConn().shop
    print condition
    _chatMsgs = db.chat_msgs.find(condition).sort("create_time", -1)
    chatMsgs = [r for r in _chatMsgs]
    print "chatMsgs count : %s" % len(chatMsgs)
    return chatMsgs

@countTime
def getKefuUID():
    # 获取客服UID
    db = getMongoDBConn().shop
    condition = {} 
    column = {'_id' : 1}
    kefuUidsResult = db.kefu.find(condition, column)
    kefuUids = []
    for r in kefuUidsResult:
        uid = int(r['_id'])
        kefuUids.append(uid)
    return kefuUids

@countTime
def kefuPerformance(day = -1):
    day = int(day)
    delta = datetime.timedelta(days = day)
    now = datetime.datetime.now()
    lastDayTime = now + delta
    startTime = lastDayTime.strftime('%Y-%m-%d 00:00:00')
    endTime = lastDayTime.strftime('%Y-%m-%d 23:59:59')

    # 查询昨天的订单
    orderResult = getOrdersData(startTime = startTime, endTime = endTime)

    # 筛选出下单用户的UID
    uids = []
    from register.models import getXHUserInfo
    from coupon.models import queryOrderCoupon
    for r in orderResult:
        uid = r['uid']
        if uid not in uids:
            uids.append(uid)

    kefuUids = getKefuUID()

    # 根据下单用户的UID和客服UID获取7天前到现在的聊天记录
    delta = datetime.timedelta(days = -7)
    startTime = (lastDayTime + delta).strftime('%Y-%m-%d 00:00:00')
    chatMsgs = getChatMsgs(userUID = uids, kefuUID = kefuUids, startTime = startTime , endTime = endTime)

    db = getMongoDBConn().shop
    print "find result"
    # 记录总数
    count = 0
    # 筛选记录
    for order in orderResult:
        uid = order['uid']
        for chat in chatMsgs:
            if chat.get('to') == uid:
                time = str(chat.get('create_time'))
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                order['kefu_uid'] = chat['from']
                order['contact_time'] = time
                order['kefu_name'] = chat.get('from_name')
                # 获取用户其他信息
                res = getXHUserInfo(uid = uid)
                if res:
                    order['account'] = res['phone'] or res['email']
                # 获取优惠劵类型
                orderNo = order['order_no']
                coupon = queryOrderCoupon(orderNo)
                if coupon is None:
                    order['coupon_type'] = ""
                else:
                    order['coupon_type'] = coupon["source"]
                if not order['reserved_2']:
                    order['reserved_2'] = ''
                # 更新中间表
                order['_id'] = order['order_no']
                db.user_kefu_orders.save(order)
                count += 1
                break

    print "result count %s" % count
    print "finish"

@countTime
def kefuPerformanceEffective(day = -1):
    day = int(day)
    delta = datetime.timedelta(days = day)
    now = datetime.datetime.now()
    lastDayTime = now + delta
    startTime = lastDayTime.strftime('%Y-%m-%d 00:00:00')
    endTime = lastDayTime.strftime('%Y-%m-%d 23:59:59')

    # 查询昨天的订单
    orderResult = getOrdersData(startTime = startTime, endTime = endTime)
    print orderResult

    # 筛选出下单用户的UID
    uids = []
    from register.models import getXHUserInfo
    from coupon.models import queryOrderCoupon
    for r in orderResult:
        uid = r['uid']
        if uid not in uids:
            uids.append(uid)

    kefuUids = getKefuUID()

    db = getMongoDBConn().shop
    print "find result"
    # 记录总数
    count = 0
    # 筛选记录
    for order in orderResult:
        if order['order_status'] not in ["unconfirmed","user_cancelled","timeout_cancelled"]:
            uid = order['uid']
            # 根据下单用户的UID和客服UID获取下单前一小时的聊天记录
            create_time = order['create_time']
            delta = datetime.timedelta(hours = -1)
            (lastDayTime + delta).strftime('%Y-%m-%d 00:00:00')
            chatMsgs = getChatMsgs(userUID = [uid], kefuUID = kefuUids, startTime = (create_time+delta).strftime('%Y-%m-%d %H:%M:%S'), endTime = create_time.strftime('%Y-%m-%d %H:%M:%S'))
            kefu_uid_list =[]
            kefu_name_list =[]
            for chat in chatMsgs:
                if chat.get('to') == uid:
                    if chat['from'] not in kefu_uid_list:
                        kefu_uid_list.append(chat.get('from'))
                        time = str(chat.get('create_time'))
                        time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                        order['kefu_uid']=chat.get('from')
                        order['contact_time'] = time
                        order['kefu_name']=chat.get('from_name')
                        # 获取用户其他信息
                        res = getXHUserInfo(uid = uid)
                        if res:
                            order['account'] = res['phone'] or res['email']
                        # 获取优惠劵类型
                        orderNo = order['order_no']
                        coupon = queryOrderCoupon(orderNo)
                        if coupon is None:
                            order['coupon_type'] = ""
                        else:
                            order['coupon_type'] = coupon["source"]
                        if not order['reserved_2']:
                            order['reserved_2'] = ''
                        # 更新中间表
                        order['_id'] = order['order_no']
                        db.user_kefu_orders_effective.save(order)
                        count += 1

    print "result count %s" % count
    print "finish"


if __name__ == '__main__':
    #kefuPerformance(day = -1)
    kefuPerformanceEffective(day = -1)
