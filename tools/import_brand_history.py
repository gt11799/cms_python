##coding:utf-8

#导入品牌最近一次上线历史

import os
import sys
import urllib2,urllib
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime


def importOnlineHistory(history=True):

    db = getMongoDBConn().shop
    if history:
        status = [3,-3]
    else:
        status = [3]
    activitys = db.activity.find({"status":{"$in":status}})
    brand_dict = {}
    nowTime = getNowUTCtime()
    for obj in activitys:
        try:
            if obj["start_time"] > nowTime:
                continue
                
        except KeyError:
            continue

        if obj["brand_id"] not in brand_dict:
            brand_dict[obj["brand_id"]] = obj["start_time"]

        else:
            start_time = brand_dict[obj['brand_id']]
            if obj["start_time"] > start_time:
                brand_dict[obj['brand_id']] = obj["start_time"]

    print brand_dict
    for key,values in brand_dict.items():
        if  key and values:
            db.brand_online_history.save({"_id":key,"start_time":values})

if __name__ == '__main__':
    importHistory()



