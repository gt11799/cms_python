#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding:utf-8

import os

# from tornado.options import define, options
import re

SITE_ROOT = os.path.dirname(__file__)

settings = {
    "static_path": os.path.join(SITE_ROOT, 'static'),
    "template_path": os.path.join(SITE_ROOT, 'templates'),
    "cookie_secret": "0y7uIjECSxmnnm0QmkCyh5Zpna0/sElYp6H7BxVLn1U=",
    "login_url": "/login",
    "xsrf_cookies": False,
    "debug": False,
    "compiled_template_cache":True,
}

ADMINS = ["backenddev@xiaoher.com"]
# ADMINS = ["haifang@xiaoher.com"]
MAIL_WARN = True
#MAIL_WARN = False

SALT_SECRET = "0y7uIjECSxmnnm0QmkCyh5Zpna0/sElYp6H7BxVLn1U="

# session expire 3 months
# define("expire", default=90 * 24 * 60 * 60, help="session expire", type=int)

# PHONE UA
PHONE_UA_LIST = ["iPad", "iPhone", "Android", "MIDP", "Opera Mobi",
            "Opera Mini", "BlackBerry", "HP iPAQ", "IEMobile",
            "MSIEMobile", "Windows Phone", "HTC", "LG",
            "MOT", "Nokia", "Symbian", "Fennec",
            "Maemo", "Tear", "Midori", "armv",
            "Windows CE", "WindowsCE", "Smartphone", "240x320",
            "176x220", "320x320", "160x160", "webOS",
            "Palm", "Sagem", "Samsung", "SGH","SonyEricsson", "MMP", "UCWEB"]

PHONE_UA = "|".join(PHONE_UA_LIST)
PHONE_UA_RE = re.compile(PHONE_UA,re.I)

# QINIU
QINIU_IMAGE_BUCKET = "you1hui"
AK = "7THwH1rj3HicB45sl0oqqmmLUk2_b2CG6popljmn"
SK = "E1CdQ8JCed3N4eseYugAJxjZYQILe0CLWTamgUb6"

# HOST
HOST = "http://m.xiaoher.com"

PC_HOST = "http://www.xiaoher.com"
# CLIENT
CLIENT = "wap"

# LOCAL REDIS SERVER
# xiaoher1
# REDIS_HOST = '10.168.20.1'
# xiaoher6
REDIS_HOST = '10.168.181.196'
REDIS_PASSWD = "wangwenwenmaster"
REDIS_PORT = 6379

## ALIYUN OSS

ALIYUN_OSS_BUCKET = "you1hui"
ALIYUN_OSS_HOST = "http://%s.oss-cn-hangzhou.aliyuncs.com/"%ALIYUN_OSS_BUCKET

# IMAGE DOMAIN
# IMAGE_DOMAIN = "qiniudn.com"
IMAGE_DOMAIN = "qbox.me"
# IMAGE_DOMAIN = "aliyuncs.com"

# LOCAL MONGO SERVER
# xiaoher1
# MONGODB_HOST = "10.168.20.1"
# xiaoher6
MONGODB_HOST = "10.168.181.196"
MONGODB_PASSWD = ""
MONGODB_PORT = 29017
MONGODB_USERNAME = ""
MONGODB_USERPASSWD = ""

# ERP mongo
#xiaoher6
# QUERY_MONGODB_HOST = "10.168.181.196"
#xiaoher5
QUERY_MONGODB_HOST = "10.168.185.228"
QUERY_MONGODB_PASSWD = ""
QUERY_MONGODB_PORT = 29017
QUERY_MONGODB_USERNAME = ""
QUERY_MONGODB_USERPASSWD = ""


# UPYUN
IMAGE_BUCKET = "youyihui"
USERNAME = "pluray"
PASSWORD = "4r3e2w1q"

FARE_MONEY = 10
# ADD_FARE_FEE_NUM = 5
# FIVE_MORE_FARE_MONEY = 15
FARE_MONEY_LEVEL = 150
#FARE_MONEY_LEVEL = 0
FARE_PRODUCT_NUM_LEVEL = 2

XIAOHER4_DB_HOST = "10.168.178.192"

# MYSQL
DB_PWD = ""
#xiaoher2
# DB_HOST = "10.171.242.34"
#xiaoher6
DB_HOST = "10.168.181.196"
DB_USER = "root"
DB_PORT = 3306
#xioaher5
QUERY_DB_HOST = "10.168.185.228"


def getClient():
    return CLIENT

def setClient(client):
    global CLIENT
    CLIENT = client

def getMessageChannel():
    from sms.models import getMC
    mc = getMC()
    return mc
    return MessageChannel

def setMessageChannel(mc=None):
    if not mc:
        from sms.models import getMC
        mc = getMC()
    else:
        from sms.models import setMC
        setMC(mc)
    global MessageChannel
    MessageChannel = mc
    return mc

FARE_DIFF = 0
def getOrderFareFee(count, payment_method=0, big_num=0):
    '''
    pay_method=0 货到付款 pay_method=1 在线支付
    '''
    if int(big_num):
        #大件运费25元起，上不封顶
        return 25 + 25 * (big_num - 1) + 2 * (count - big_num)
    else:
        FARE_MONEY = 10 if int(payment_method) else 10 + FARE_DIFF
        if count >1:
            FARE_MONEY += (count-1)*2.0
        return FARE_MONEY if FARE_MONEY <= 30 else 30

def getOrderFareFeeOldVersion(count, payment_method, big_num=0):
    '''
    老版本app邮费计算
    '''
    if int(big_num):
        #大件运费25元起，上不封顶
        return 25 + 25 * (big_num - 1) + 2 * (count - big_num)
    else:
        FARE_MONEY = 10
        if count == 0:
            return 0
        elif count >1:
            FARE_MONEY += (count-1)*2.0
        return FARE_MONEY if FARE_MONEY <= 30 else 30



MIN_VIRTUAL_USER_ID = 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10

WAP_COOKIE_EXPIRE_DAYS = 180

WEB_COOKIE_EXPIRE_DAYS = 1

INIT_PASSWORD = "d41d8cd98f00b204e9800998ecf8427e"

MIN_GOODS_ID = 10 * 10 * 10 * 10 * 10

MIN_ACTIVITY_GOODS_ID = MIN_GOODS_ID * 10 * 10

MIN_BRAND_ID = 10 * 10 * 10 * 10

MIN_ACTIVITY_ID = 10 * 10 * 10

MIN_PACKAGE_ID = 100000

domain = ".xiaoher.com"

WEB_HOST = "http://www.xiaoher.com"

WAP_HOST = "http://m.xiaoher.com"

FRESH_MAN_ACTIVITY_ID  = 1165
#FRESH_MAN_ACTIVITY_ID  = 1140
SIGN_CLOTH_ACTIVITY_ID = 0

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 8

VERSION = 2015021319

#活动分类
# CATEGORY = [
#             {"id":1,"name":"潮流女装","q":"women"},
#             {"id":2,"name":"精品女包","q":"bags"},
#             {"id":3,"name":"时尚童装","q":"kids"},
#             {"id":4,"name":"儿童乐园","q":"toys"},
#             ]
CATEGORY = [
            {"id":1,"name":"女士区","q":"ladys"},
            {"id":2,"name":"儿童区","q":"children"},
            ]



#ORDER_CAN_CANCEL = ["applying","unpay","pending","paid","confirmed","picking","purchase","picked","picked","packing","part_packing","packed","part_packed","delivering","part_delivering"]
#ORDER_CAN_CANCEL = ("pending","paid","confirmed","picking","picked","packing","packed","part_picked","part_packed",)
ORDER_GOODS_CAN_CANCEL = ("confirmed","purchase","picking","picked","packing", 'packed','waitdeliver','delivering',)

NEW_ACTIVITY = False

PERMISSON_ON = False
#PV/UV查询URL
# PV_UV_QUERY_URL = 'http://127.0.0.1:8999/page_source_count_api'
PV_UV_QUERY_URL = 'http://10.161.162.197:9021/page_source_count_api'

#该cookies用于进行首页调度
INDEX_TYPE_COOKIES = 'index_template2'
