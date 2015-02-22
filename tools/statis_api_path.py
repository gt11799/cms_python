# coding:utf-8
import os
import sys
print "hello,window"
import datetime
import time
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
# from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def getAllApiPath():
    conn =getMongoDBConn()
    db = conn.shop
    result = db.apiclick.find()
    apiPath = {}
    for r in result:
        if r["api_path"] in apiPath:
            apiPath[r["api_path"]] = apiPath[r["api_path"]] + 1
        else:
            apiPath[r["api_path"]] = 1
    apiPath = sorted(apiPath.iteritems(),key = lambda d:d[1],reverse = True) 
    for r in apiPath:
        print r
    pass

if __name__ == "__main__":
    getAllApiPath()




