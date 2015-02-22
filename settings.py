#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
from tornado.options import define,options

from unchange_settings import *


################ UPYUN #########################

IMAGE_BUCKET = "youyihui"
USERNAME = "pluray"
PASSWORD = "4r3e2w1q"

################ QINIU ##########################
QINIU_IMAGE_BUCKET = "you1huitest"
AK = "7THwH1rj3HicB45sl0oqqmmLUk2_b2CG6popljmn"
SK = "E1CdQ8JCed3N4eseYugAJxjZYQILe0CLWTamgUb6"



##############MYSQL############################
DB_HOST = '192.168.1.150'
#DB_HOST = '127.0.0.1'
DB_PWD = ''
#DB_PWD = ''

# CLIENT
CLIENT = "wap" # "web"

NODE_NAME = '' #节点名称


QUERY_MONGODB_HOST = "192.168.1.150"
QUERY_MONGODB_PASSWD = ""
QUERY_MONGODB_PORT = 29017
QUERY_MONGODB_USERNAME = ""
QUERY_MONGODB_USERPASSWD = ""

QUERY_DB_HOST = "192.168.1.150"


settings = {
    "static_path": os.path.join(SITE_ROOT, 'static'),
    "template_path": os.path.join(SITE_ROOT, 'templates'),
    "cookie_secret": "0y7uIjECSxmnnm0QmkCyh5Zpna0/sElYp6H7BxVLn1U=",
    "login_url": "/login",
    "xsrf_cookies": False,
    "debug": True,
}
domain=None

MAIL_WARN = False
#myself
'''
REDIS_HOST = '127.0.0.1'
REDIS_PASSWD = ""

DB_HOST = '127.0.0.1'
DB_PWD = 'chrdw'


QUERY_MONGODB_HOST = "127.0.0.1"
QUERY_MONGODB_PASSWD = ""
QUERY_MONGODB_PORT = 29017
QUERY_MONGODB_USERNAME = ""
QUERY_MONGODB_USERPASSWD = ""

QUERY_DB_HOST = "127.0.0.1"
'''