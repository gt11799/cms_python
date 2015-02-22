#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding: utf-8

import os
from tornado.options import define,options

from unchange_settings import *


################ QINIU ##########################
QINIU_IMAGE_BUCKET = "you1huitest"
AK = "7THwH1rj3HicB45sl0oqqmmLUk2_b2CG6popljmn"
SK = "E1CdQ8JCed3N4eseYugAJxjZYQILe0CLWTamgUb6"



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

DB_HOST = 'localhost'
DB_PWD = ''

REDIS_HOST = 'localhost'
REDIS_PASSWD = ""
REDIS_PORT = 6379

