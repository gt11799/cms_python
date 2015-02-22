#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
import sys
import tornado
from tornado import gen
import tornado.httpclient
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from sms.models import sendMessageNoAsync

from utility.utils import DBAccess,getMongoDBConn

import datetime

#@gen.coroutine
def send_wish_notification():
   
    """
    Send message to user who subscribe wish, which is in the future
    """
    
    wishlist_table = getMongoDBConn().shop.wishlist 
    delta = datetime.timedelta(seconds=30)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fake_current_time = (datetime.datetime.now()-delta).strftime("%Y-%m-%d %H:%M:%S")
    all_future_wishlist = wishlist_table.find({"upline_time": {"$gt": fake_current_time}})
    wishlist_ids =[]
    for e in all_future_wishlist:
        #返回跟现在时间同小时的所有心愿单活动
        if e['upline_time'][:13] == current_time[:13]:
            wishlist_ids.append(str(e['_id']))
    print wishlist_ids
    
    return_list = []
    if len(wishlist_ids)>0:
        db = DBAccess()
        db.dbName = "billing_record_db"
        condition = ",".join(wishlist_ids)
        sql = "select * from user_wish_list where wish_list_id in (%s)" % condition
        print sql
        fit_user = list(db.execQueryAssoc(sql))
        print "fit_user"
        print fit_user
        if len(fit_user)> 0: 
            fit_user_ids_str = []
            for i in fit_user:
                fit_user_ids_str.append(str(i['uid']))
            condition = ",".join(fit_user_ids_str)
            sql = "select * from xh_user where uid in (%s)" % condition
            print sql
            user_infos = list(db.execQueryAssoc(sql))
            for user_info in user_infos:
                print "user_info"
                print user_info
                '''
                print user_info.get('phone')
                print user_info.get('phone_verify')
                print user_info.get('allow_push',0)
                print user_info.get('is_push', 0)
                print user_info.get('phone_verify') == 1 and user_info.get('allow_push',0) ==1 and user_info.get('is_push', 0) == 0
                '''
                user_wishlist_info =[]
                for i in fit_user:
                    if i['uid'] == user_info.get('uid', 0):
                        user_wishlist_info.append(i)
                print "user_wishlist_info"
                print user_wishlist_info
                for i in user_wishlist_info:
                    if user_info.get('phone_verify', 0) == 1 and user_info.get('allow_push',0) ==1 and i.get('is_pushed',0) == 0:
                        print "True", user_info.get('phone')
                        wishlist_table = getMongoDBConn().shop.wishlist
                        wishlist = list(wishlist_table.find({"_id": i['wish_list_id']}))[0]
                        return_list.append({"phone":user_info.get('phone'),"wishlist_name":wishlist["wishlist_name"]
                            ,"upline_time":wishlist['upline_time'],"uid":i.get('uid', '')})
    print "return_list:",return_list
    for i in return_list:
        '''
        if int(i["upline_time"][11:13])<6:
            time = "凌晨" + i["upline_time"][11:]
        if int(i["upline_time"][11:13])<11:
            time = "上午" + i["upline_time"][11:]
        elif int(i["upline_time"][11:13])<13:
            time = "中午" + i["upline_time"][11:]
        elif int(i["upline_time"][11:13])<18:
            time = "下午" + str(int(i["upline_time"][11:13])-12)+i["upline_time"][13:]
        else:
            time = "晚上" + str(int(i["upline_time"][11:13])-12)+i["upline_time"][13:]
        '''
        msg = "亲爱的会员，您加入心愿单的%s活动已经开始，赶紧上线抢购吧！" %(i["wishlist_name"])
        msg += "【小荷特卖】"
        print msg
        try:
            sendMessageNoAsync(i["phone"],msg)
        except Exception,e:
            print "sendMessageNoAsync:",e
            continue
        db = DBAccess()
        db.dbName = "billing_record_db"
        sql = "update user_wish_list set is_pushed = 1 where uid = %s" % i["uid"]
        db.execNonQuery(sql)

    #return return_list



if __name__ == '__main__':
    send_wish_notification()