#coding:utf8
__author__ = 'David'

import os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

import motor
import pymongo
import redis
import copy
import urllib2,urllib
import json


class _const():
    def __init__(self):
        self.REDIS_HOST = "10.161.162.197"      #在erp.xiaoher.com:9999 上测的时候用着
        # self.REDIS_HOST = "115.29.174.80"
        # self.REDIS_HOST = "127.0.0.1"         #本地测的时候指到我的ip 192.168.1.61
        #self.REDIS_HOST = "192.168.1.61"
        self.REDIS_PASSWD = ""
        self.REDIS_PORT = 6379

        # self.DATAAPI_URL = "http://127.0.0.1:8999/dataapi" #本地测的时候指到我的ip 192.168.1.61
        self.DATAAPI_URL = "http://10.161.162.197:9021/dataapi"
        # self.DATAAPI_URL = "http://115.29.174.80:9021/dataapi"
        self.DATATYPEAPI_URL="http://10.161.162.197:9021/datatypeapi"
        # self.DATATYPEAPI_URL="http://115.29.174.80:9021/datatypeapi"
        # self.DATATYPEAPI_URL="http://127.0.0.1:8999/datatypeapi"
        # self.DATAAPI_URL = "http://10.161.162.197:9021/exposureapi"
        # self.DATAAPI_URL = "http://115.29.174.80:9021/exposureapi"
        # self.DATAAPI_URL = "http://127.0.0.1:8999/exposureapi"

C = _const()


class UBSclient():
    def __init__(self):
        self.redisConn = self._getUBSRedis()

    def _getUBSRedis(self,rdb=0):
        key = "REDIS_POOL_UBS_%s"%rdb
        pool = globals().get(key)
        if not pool:
            pool = redis.ConnectionPool(
                host= C.REDIS_HOST, password=C.REDIS_PASSWD, port=C.REDIS_PORT, db=rdb)
            globals()[key] = pool

        # print id(pool)
        r = redis.Redis(connection_pool=pool)
        return r

    def queryGoodsClickAndShow(self,activityGoodsIDs):
        # return [clickRecords,][showRecords,]
        pipeline = self.redisConn.pipeline()
        for i in activityGoodsIDs:
            pipeline.get("good_click_{}".format(i))

        clickRecords = pipeline.execute()

        for i in activityGoodsIDs:
            pipeline.get("good_show_{}".format(i))

        showRecords = pipeline.execute()
        return clickRecords,showRecords

    def queryActivityClickAndShow(self,activityIds):
        # return [clickRecords,][showRecords,]
        pipeline = self.redisConn.pipeline()
        for i in activityIds:
            pipeline.get("activity_click_{}".format(i))

        clickRecords = pipeline.execute()

        for i in activityIds:
            pipeline.get("activity_show_{}".format(i))

        showRecords = pipeline.execute()
        return clickRecords,showRecords

    def queryTopXActivityByClick(self, topX = 20, offset=0, descending=True):
        # return [{activity_id:,click:,show:,},]
        keys = self.redisConn.keys("activity_click_[1-9]*?")
        if offset > len(keys):
            return []
        rets = self.redisConn.mget(*keys)
        needSort = []
        assert len(keys) == len(rets)
        for i in xrange(len(keys)):
            value = int(rets[i]) if rets[i] else 0
            needSort.append((keys[i],value))

        needSort.sort(key=lambda x:x[1],reverse=descending)
        sortedRet = needSort
        topKeys = [ret[0] for ret in sortedRet]
        if offset > len(topKeys):
            return []

        if offset + topX > len(topKeys):
            endPos = len(topKeys) - 1
        else:
            endPos = offset + topX

        rangeKeys = sortedRet[offset:endPos]

        searchKey = [data[0] for data in rangeKeys]

        pipeline = self.redisConn.pipeline()
        for key in searchKey:
            activity_id = key.split("_")[-1]
            # searchIds.append(id)
            query = "activity_show_{}".format(activity_id)
            print "+",
            pipeline.get(query)
        print ""
        shows = pipeline.execute()
        assert len(shows) == len(searchKey)

        # gen finally result here
        ret = []

        for i in xrange(len(rangeKeys)):
            d = {}
            d['activityId'] = rangeKeys[i][0].split("_")[-1]
            d['click'] = int(rangeKeys[i][1]) if rangeKeys[i][1] else 0
            d['show'] = int(shows[i]) if shows[i] else 0
            ret.append(d)
        return ret, len(keys)

    def queryTopXActivityByExposure(self, topX = 20, offset=0, descending=True):
        # return [{activity_id:,click:,show:,},]
        keys = self.redisConn.keys("activity_show_[1-9]*?")
        if offset > len(keys):
            return []
        rets = self.redisConn.mget(*keys)
        needSort = []
        assert len(keys) == len(rets)
        for i in xrange(len(keys)):
            value = int(rets[i]) if rets[i] else 0
            needSort.append((keys[i],value))

        needSort.sort(key=lambda x:x[1],reverse=descending)
        sortedRet = needSort
        topKeys = [ret[0] for ret in sortedRet]
        if offset > len(topKeys):
            return []

        if offset + topX > len(topKeys):
            endPos = len(topKeys) - 1
        else:
            endPos = offset + topX

        rangeKeys = sortedRet[offset:endPos]
        searchKey = [data[0] for data in rangeKeys]

        pipeline = self.redisConn.pipeline()
        searchIds = []
        for key in searchKey:
            activity_id = key.split("_")[-1]
            # searchIds.append(id)
            query = "activity_click_{}".format(activity_id)
            print "+",
            pipeline.get(query)
        print ""

        click = pipeline.execute()
        assert len(click) == len(searchKey)

        # gen finally result here
        ret = []

        for i in xrange(len(rangeKeys)):
            d = {}
            d['activityId'] = rangeKeys[i][0].split("_")[-1]
            d['show'] = int(rangeKeys[i][1]) if rangeKeys[i][1] else 0
            d['click'] = int(click[i]) if click[i] else 0
            ret.append(d)
        return ret, len(keys)


    def _queryGoodsClickAndShowByTime(self,start,end,activityId=[],goodsId=[]):

        activityId = [str(r) for r in activityId]
        goodsId = [str(r) for r in goodsId]

        rawArgs = {
            "start":start,
            "end":end,
            "activityIds":activityId,
            "goodsIds":goodsId
        }
        raw = json.dumps(rawArgs)
        arg = {
            "token" : "xia1o2h3er",
            "raw" : raw
        }
        postData = urllib.urlencode(arg)
        req = urllib2.Request(C.DATAAPI_URL, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        print "sending request...{}".format(C.DATAAPI_URL)
        resp = urllib2.urlopen(req)
        print "Done"
        return resp.read()

    def _queryUsersRegister(self):
        arg = {
            "token" : "xia1o2h3er",
            "datatype" : "1"
        }
        postData = urllib.urlencode(arg)
        req = urllib2.Request(C.DATATYPEAPI_URL, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req)
        ret=resp.read()
        if ret:
            users=json.loads(ret)
            return users
        else:
            return None

    def _queryUsersClicks(self,vuidstrs):
        arg = {
            "token" : "xia1o2h3er",
            "datatype" : "2",
            "vuid" : json.dumps(vuidstrs)
        }
        postData = urllib.urlencode(arg)
        req = urllib2.Request(C.DATATYPEAPI_URL, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req)
        ret=resp.read()
        if ret:
            clicks=json.loads(ret)
            return clicks
        else:
            return None

    def _queryUsersNum(self,regtime,source):
        arg = {
            "token" : "xia1o2h3er",
            "datatype" : "3",
            "regtime":regtime,
            "source" : source
        }
        postData = urllib.urlencode(arg)
        req = urllib2.Request(C.DATATYPEAPI_URL, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req)
        ret=resp.read()
        if ret:
            usersnum=json.loads(ret)
            return usersnum
        else:
            return None

    def _queryUsers(self):
        arg = {
            "token" : "xia1o2h3er",
            "datatype" : "4"
        }
        postData = urllib.urlencode(arg)
        req = urllib2.Request(C.DATATYPEAPI_URL, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req)
        ret=resp.read()
        if ret:
            users=json.loads(ret)
            return users
        else:
            return None



    def queryActivityClickAndShowByTime(self,activityId,start,end):
        ret = self._queryGoodsClickAndShowByTime(start,end,activityId)
        if ret:
            (click,show) = json.loads(ret)
            return click,show
        else:
            return None

    def queryGoodsClickAndShowByTime(self,goodsIds,start,end):
        ret = self._queryGoodsClickAndShowByTime(start,end,goodsId=goodsIds)
        if ret:

            (click,show) = json.loads(ret)
            return click,show

        else:
            return None



def unitTest():


    activities = ["5200",]
    ubsclient=UBSclient()
    print ubsclient.queryActivityClickAndShowByTime(activities,"2015-02-05 14:30:10","2015-02-05 14:40:10")




    # print ubsclient.queryTopXActivityByExposure()
    # print "-orz-"*40
    # ret = ubsclient.queryTopXActivityByClick(topX=3,offset=2)
    # print len(ret)
    # for  r in ret[0] :
    #     print r
    # ret = ubsclient.queryTopXActivityByExposure(topX=2)
    # print len(ret)
    # for  r in ret[0] :
    #     print r

if __name__ == "__main__":
    unitTest()
    pass


