#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding:utf-8

import os

import re

SITE_ROOT = os.path.dirname(__file__)

settings = {
    "static_path": os.path.join(SITE_ROOT, 'static'),
    "template_path": os.path.join(SITE_ROOT, 'templates'),
    "cookie_secret": "xxxxxxxxx",
    "login_url": "/login",
    "xsrf_cookies": False,
    "debug": False,
    "compiled_template_cache":True,
}


CLIENT = "web"


def getClient():
    return CLIENT

def setClient(client):
    global CLIENT
    CLIENT = client



WEB_COOKIE_EXPIRE_DAYS = 1

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 8

VERSION = 2015021319

QINIU_IMAGE_BUCKET = ""
AK = ""
SK = ""

domain=None

DB_HOST = 'localhost'
DB_PWD = ''

REDIS_HOST = 'localhost'
REDIS_PASSWD = ""
REDIS_PORT = 6379