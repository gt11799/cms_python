# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
try:
    from settings import HOST
except:
    HOST = "http://127.0.0.1"
import urllib2

API_URL = "%s/cart/admin/recycle" % HOST

res = urllib2.urlopen(API_URL)

assert res.read() == "ok"
