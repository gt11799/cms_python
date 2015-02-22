# coding:utf-8

import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
import urllib2
import json
import time

from utility.utils import getMongoDBConn

with open("code.txt") as f:
    codes = f.readlines()

VIP_ADDRESS_API = "http://n.myopen.vip.com/address/address?areaid=%s"

conn = getMongoDBConn()
db = conn.shop


def getdata(code,code_can_zero=False):
    if code == '0' and code_can_zero == False:
        return
    url = VIP_ADDRESS_API % code
    try:
        res = urllib2.urlopen(url)
        jsondata = json.load(res)
        jsondata["_id"] = code
        db.address.save(jsondata)
        print "%s get" % code
        lists = jsondata["list"]
        if not lists:
            return
        for c in lists:
            getdata(c["id"])
    except:
        time.sleep(10)
        print "get error"
        getdata(code)


# getdata('0',True)

code = []
xx = """
104103
104104
104105
104106
105100
105101
105102
105103
105104
106101
106102
106103
106104
106105
"""
xx = xx.strip()
xx = xx.split()
code.extend(xx)
for c in code:
    getdata(c)