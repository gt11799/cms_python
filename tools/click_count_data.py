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

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime,getRedisObj

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
    count = 20
    apiCollection = []
    i  = 0 
    for r in apiPath:
        api = r[0]
        if api.find("admin") != -1:
            continue

        apiCollection.append(api)
        i =  i + 1
        if i >= count:
            break
    return apiCollection


def getAllSources():
    re = getRedisObj()
    if re.exists("all_click_sources"):
        sources = re.smembers("all_click_sources")
        return sources
    else:
        conn =getMongoDBConn()
        db = conn.shop
        result = db.apiclick.find()
        source = {}
        for r in result:
            if r["source"] in source:
                source[r["source"]] = source[r["source"]] + 1
            else:
                source[r["source"]] = 1
        source = sorted(source.iteritems(),key = lambda d:d[1],reverse = True) 
        count = 200
        sourceCollection = []
        i  = 0 
        for r in source:
            s = r[0]
            sourceCollection.append(s)
            re.sadd("all_click_sources",s)
            i =  i + 1
            if i >= count:
                break
        re.expire("all_click_sources",3600 * 12 * 7)
        return sourceCollection

sources = getAllSources()


def getAllUser(min_time=None,max_time=None,links = None,source = None):
    # query = " where create_time >= '2014-04-20 00:00:00' "
    conn = getMongoDBConn()
    db = conn.shop
    if links is None:
        result = db.apiclick.find({"date":{"$gte":str(min_time),"$lte" : str(max_time)},"source":source})
    else:
        result = db.apiclick.find({"date":{"$gte":str(min_time),"$lte" : str(max_time)},"api_path":links})
    uids = []
    for r in result:
        uids.append(r['uid'])
    return uids

def analyzeCustomerBySource(uid,source):
    uid = int(uid)
    conn = getMongoDBConn()
    db = conn.shop
    result = db.apiclick.find({"uid":uid,"source":source}).sort([("date",1)])
    if result.count() == 0:
        return
    timeObj = time.strptime(result[0]["date"],TIME_FORMAT)
    first_click_time = time.strftime("%Y-%m-%d",timeObj)
    if db.user_apiclick_1.find_one({"_id":uid,"source":source}):
        pass
    else:
        db.user_apiclick_1.save({"_id":uid,"source":source,"first_click_time":first_click_time})

    dateOrders = {}
    for r in result:
        if not r["date"]:
            continue
        timeObj = time.strptime(r['date'],TIME_FORMAT)
        d = time.strftime("%Y-%m-%d",timeObj)
        c = dateOrders.get(d,0)
        c = c + 1
        dateOrders[d] = c
    db.user_apiclick_1.update({"_id":uid,"source":source},{"$set" : dateOrders})


def analyzeCustomerEx(uid,s):
    analyzeCustomerBySource(uid,s)

def outputToFiles(fileName,str):
    f = open(fileName,"a+")
    f.write(str)
    f.write("\r\n")
    f.close()


def analyzeCustomer(uid,links):
    uid = int(uid)
    conn = getMongoDBConn()
    db = conn.shop
    result = db.apiclick.find({"uid":uid,"api_path":links}).sort([("date",1)])
    timeObj = time.strptime(result[0]["date"],TIME_FORMAT)
    first_click_time = time.strftime("%Y-%m-%d",timeObj)
    if db.user_apiclick.find_one({"_id":uid,"api_path":links}):
        pass
    else:
        db.user_apiclick.save({"_id":uid,"api_path":links,"first_click_time":first_click_time})

    dateOrders = {}
    for r in result:
        if not r["date"]:
            continue
        timeObj = time.strptime(r['date'],TIME_FORMAT)
        d = time.strftime("%Y-%m-%d",timeObj)
        c = dateOrders.get(d,0)
        c = c + 1
        dateOrders[d] = c
    db.user_apiclick.update({"_id":uid,"api_path":links},{"$set" : dateOrders})

from shop_admin.models import getAllApis
def dailyClickCountData():
    d = datetime.date.today() - datetime.timedelta(days = 1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    apis = getAllApis()
    for api in apis:
        result = getAllUser(min_time,max_time,api)
        for r in result:
            analyzeCustomer(r,api)
    pass

def dailyClickCountDataEx():
    d = datetime.date.today() - datetime.timedelta(days = 1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    sources = getAllSources()
    for s in sources:
        result = getAllUser(min_time,max_time,links = None,source = s)
        for r in result:
            analyzeCustomerEx(r,s)
    pass

def countSpecificDateEx(theDate,s):
    d = theDate - datetime.timedelta(days = 1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    result = getAllUser(min_time,max_time,links = None,source = s)
    outputStr = "total customer of " + str(theDate) + " is " + str(len(result))
    print "total customer of " + str(theDate) + " is " + str(len(result))
    outputToFiles("output",outputStr)
    count = 0 
    for r in result:
        count = count + 1
        analyzeCustomerEx(r,s)
        if count % 100 == 0:
            outputStr = "finished users " + str(count)
            print outputStr
            outputToFiles("output",outputStr)

    pass


def countSpecificDate(links,theDate):
    d = theDate - datetime.timedelta(days = 1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    result = getAllUser(min_time,max_time,links)
    print "total customer of " + str(theDate) + " is " + str(len(result))
    count = 0 
    for r in result:
        count = count + 1
        analyzeCustomer(r,links)
        if count % 100 == 0:
            print "finished users " + str(count)
    pass

def dayAnalysisEx(sources,first_click_time):
    conn = getMongoDBConn()
    db = conn.shop
    returnResult = {}
    returnResult["first_click_time"] = first_click_time
    if sources == "":
        result = db.user_apiclick_1.find({"first_click_time":first_click_time})
    else:
        if len(sources) == 1:
            result = db.user_apiclick_1.find({"source":sources[0],"first_click_time":first_click_time})
        elif len(sources) == 0:
            result = db.user_apiclick_1.find({"first_click_time":first_click_time})
        else:
            orConditions = []
            for item in sources:
                orConditions.append({"source" : item})
            result = db.user_apiclick_1.find({"$or":orConditions,"first_click_time":first_click_time})
    returnResult["users"] = result.count()
    first_click_time_user = result.count()

    analysisResult = {}
    for r in result:
        for key,value in r.items():
            if str(key).startswith("201"):
                if key not in analysisResult:
                    analysisResult[key] = {
                        "users":0,
                        "clicks":0,
                    }
                analysisResult[key]["users"] += 1
                analysisResult[key]["clicks"] += value
                analysisResult[key]['rate'] = str(round(analysisResult[key]["users"]/float(first_click_time_user),4)*100 ) + "%"
            else:
                pass
    returnResult.update(analysisResult)
    print returnResult
    return returnResult

def dayAnalysis(links,first_click_time):
    conn = getMongoDBConn()
    db = conn.shop
    returnResult = {}
    returnResult["first_click_time"] = first_click_time
    if links == "":
        result = db.user_apiclick.find({"first_click_time":first_click_time})
    else:
        result = db.user_apiclick.find({"api_path":links,"first_click_time":first_click_time})
    returnResult["users"] = result.count()
    first_click_time_user = result.count()

    analysisResult = {}
    for r in result:
        for key,value in r.items():
            if str(key).startswith("201"):
                if key not in analysisResult:
                    analysisResult[key] = {
                        "users":0,
                        "clicks":0,
                    }
                analysisResult[key]["users"] += 1
                analysisResult[key]["clicks"] += value
                analysisResult[key]['rate'] = round(analysisResult[key]["users"]/float(first_click_time_user),2)
            else:
                pass
    returnResult.update(analysisResult)
    print returnResult
    return returnResult

 
if __name__ == "__main__":
    '''
    apis = getAllApis()
    initialDate = datetime.date(2014,9,24)
    for api in apis:
        print "begin process " + api
        for i in range(0,10):
            d = initialDate + datetime.timedelta(days = i)
            print d
            countSpecificDateEx(api,d)
    '''
    initialDate = datetime.date(2014,9,24)
    for s in sources:
        outputToFiles("output","begin process source:" + s)
        for i in range(0,10):
            d = initialDate + datetime.timedelta(days = i)
            countSpecificDateEx(d,s)

    # result = getAllApiPath()
    # for r in result:
    #     print r
    #     dailyCountData(r)





