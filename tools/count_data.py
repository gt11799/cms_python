# coding:utf-8
import os
import sys
print "hello,window"
import datetime
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
import  datetime

# from orders.models import insertOrdersGoods
# from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime

def getAllUser(min_time=None,max_time=None):
    # query = " where create_time >= '2014-04-20 00:00:00' "
    query = " where 1=1 "
    if min_time:
        query += " and create_time >='%s' "%min_time
    if max_time:
        query += " and create_time <='%s'"%max_time

    sql = "select uid from orders  %s group by uid " % query
    print sql
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    return result

def analysisCustomer(uid):
    uid = int(uid)
    print "********uid:%s*********** analysis" %uid
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid,create_time from orders where uid=%s order by create_time"%uid
    result = db.execQueryAssoc(sql)
    if not result:
        return
    if not result[0]["create_time"]:
        return
    first_orders_time = result[0]["create_time"].strftime("%Y-%m")
    conn = getMongoDBConn()
    db = conn.shop
    if db.user_orders_analysis.find_one({"_id":uid}):
        pass
    else:
        db.user_orders_analysis.save({"_id":uid,"first_order_date":first_orders_time})

    dateOrders = {}
    for r in result:
        if not r["create_time"]:
            continue
        d = r["create_time"].strftime("%Y-%m")
        c = dateOrders.get(d,0)
        c += 1
        dateOrders[d] = c
    
    db.user_orders_analysis.update({"_id":uid},{"$set":dateOrders})


def analysisCustomerWeek(uid):
    uid = int(uid)
    print "********uid:%s*********** analysis" %uid
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid,create_time from orders where uid=%s order by create_time"%uid
    result = db.execQueryAssoc(sql)
    if not result:
        return

    if not result[0]["create_time"]:
        return

    conn = getMongoDBConn()
    db = conn.shop
    analysisResult = {"_id":uid,"first_order_date":result[0]["create_time"].strftime("%Y-%m-%d")}
    for r in result:
        d = r["create_time"].strftime("%Y-%m-%d")
        if d not in analysisResult:
            analysisResult[d] = 0

        analysisResult[d] += 1

    db.user_orders_week_analysis.save(analysisResult)


def monthAnalysis(first_order_month,_type="amount"):
    conn = getMongoDBConn()
    db = conn.shop
    returnResult = {}
    returnResult["first_order_month"] = first_order_month
    result = db.user_orders_analysis.find({"first_order_date":first_order_month})
    returnResult["users"]  = result.count()
    first_order_month_user = result.count()
    analysisResult = {}
    for r in result:
        for key,value in r.items():
            if str(key).startswith("201"):
                if key not in analysisResult:
                    analysisResult[key] = {
                        "users":0,
                        "orders":0,
                        "uids":[],
                    }
                analysisResult[key]["users"] += 1
                analysisResult[key]["orders"] += value
                analysisResult[key]["rate"] = round(analysisResult[key]["users"]/float(first_order_month_user),2)
                if _type == "amount":
                    analysisResult[key]["uids"].append(str(r["_id"]))
            else:
                pass

    if _type == "amount":
        for key,value in analysisResult.items():
            if str(key).startswith("201"):
                uids = analysisResult[key].pop("uids")
                if not uids:
                    analysisResult[key]["amount"] = 0
                else:
                    uids = ','.join(uids)
                    analysisResult[key]['amount'] = round(getSumUidOrdersAmount(uids,key),2)
                    
    # print analysisResult
    # db.month_orders_analysis.update({"_id":first_order_month,"users":first_order_month_user},{"$set":analysisResult},upsert=True)
    returnResult.update(analysisResult)
    print returnResult
    return returnResult

def getSumUidOrdersAmount(uids,date):
    date = date.split('-')
    year = int(date[0])
    month = int(date[1])
    from lipin.models import  incrMonth
    d1 = datetime.date(year,month,1)
    d2 = incrMonth(d1,0)
    sql = "select sum(total_price) from orders where create_time>='%s' and create_time<='%s 23:59:59'  \
          and uid in (%s) "%(str(d1),str(d2),uids)
    print sql
    db = DBAccess()
    db.dbName = "billing_record_db"
    return db.execQuery(sql)[0][0]




def getWeekKey(first_day,current_day):
    days = (current_day - first_day).days
    week = days / 7
    start = first_day + datetime.timedelta(days=7*week) 
    end = start + datetime.timedelta(days=7*1) 
    return "%s ~ %s"%(str(start),str(end))


def weekAnalysis(special_date):
    conn = getMongoDBConn()
    db = conn.shop
    first_day = datetime.datetime.strptime(special_date,'%Y-%m-%d').date()
    result = db.user_orders_week_analysis.find({"first_order_date":{"$gte":str(first_day)}})
    analysisResult = {}
    for r in result:
        r["first_order_date"] = datetime.datetime.strptime(r["first_order_date"],'%Y-%m-%d').date()
        weekkey = getWeekKey(first_day,r["first_order_date"])
        if weekkey not in analysisResult:
            analysisResult[weekkey] = {
                "users":0,
            }
            for i in range(1,10):
                analysisResult[weekkey]["week_%s"%i] = 0
                # analysisResult[weekkey]["week_%s_rate"%i] = 0

        analysisResult[weekkey]["users"] += 1
        for key,value in r.items():
            if str(key).startswith("201"):
                d = datetime.datetime.strptime(key,'%Y-%m-%d').date()
                days = (d - r["first_order_date"]).days
                week = days / 7
                if week == 0:
                    continue
                elif week >=9:
                    week = 9
                analysisResult[weekkey]["week_%s"%week] += 1
                
            else:
                pass

    for key,value in analysisResult.items():
        print key,value
    return analysisResult


def userOrderAnalysis(special_month):
    conn = getMongoDBConn()
    db = conn.shop
    d = datetime.datetime.strptime(special_month,'%Y-%m-%d').strftime("%Y-%m")

    start_day = "%s-01"%d
    end_day = "%s-31"%d
    print start_day,'-----',end_day
    result = db.user_orders_week_analysis.find({"first_order_date":{"$gte":start_day,"$lt":end_day}})
    analysisResult = {"users":0,"date":d,"order_1":0,"order_2":0,"order_3":0,"order_4":0,"order_5":0}
    for r in result:
        analysisResult["users"] += 1
        ordersCount = 0
        for key,value in r.items():
            if str(key).startswith("201"):
                ordersCount += r[key]

        if ordersCount >5:
            ordersCount = 5
        for i in range(2,ordersCount+1):
            analysisResult["order_%s"%i] += 1

    print analysisResult
    return analysisResult


def freshMenCheck():
    sql = "select * from orders where create_time >'2014-04-23 0:0:0'"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    totalPrice = 0.0
    dateUidDict = {}
    for item in result:
        totalPrice = item['total_price']
        uid = item['uid']
        dateStr = item["create_time"].strftime("%Y-%m-%d")
        if totalPrice < 1:
            if dateStr in dateUidDict:
                dateUidDict[dateStr][str(uid)] = 1
            else:
                temp = {}
                temp[str(uid)] = 1
                dateUidDict[dateStr] = temp
    return dateUidDict

def getUserOrderNum(uid):
    sql = "select count(*) from orders where uid=%s" % (uid,)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQuery(sql)
    return int(result[0][0])

def freshmenAnalysis(uid):
    sql = "select * from orders where uid=%s order by create_time "%uid
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    if not result:
        return
    if result[0]["total_price"] > 1:
        return

    if len(result) > 5:
        return

    conn = getMongoDBConn()
    db = conn.shop

    _id = result[0]["create_time"].strftime("%Y-%m-%d")

    obj = db.fresh_man_users_analysis.find_one({"_id":_id})
    if not obj:
        return
    


def main3():
    dateUidDict = freshMenCheck()
    conn = getMongoDBConn()
    db = conn.shop
    for date,uidDict in dateUidDict.items():
        result = {"_id":date,"users":len(uidDict),"order_2":0,"order_3":0,"order_4":0,"order_5":0}
        for uid in uidDict:
            uid = int(uid)
            orderCount = getUserOrderNum(uid)
            if orderCount == 1:
                continue
            if orderCount>5:
                orderCount = 5
            for i in range(2,orderCount+1):
                result["order_%s"%i] += 1

        result["count_date"] = str(datetime.date.today())
        print result
        db.fresh_man_users_analysis.save(result)



def dailyCountData():
    d = datetime.date.today() - datetime.timedelta(days=1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    result = getAllUser(min_time,max_time)
    for r in result:
        uid = r["uid"]
        analysisCustomer(uid)
        analysisCustomerWeek(uid)
    main3()

def dailyCountSpecial(specialDate):
    d = specialDate - datetime.timedelta(days=1)
    min_time =  "%s 00:00:00"%str(d)
    max_time =  "%s 23:59:59"%str(d)
    result = getAllUser(min_time,max_time)
    for r in result:
        uid = r["uid"]
        analysisCustomer(uid)
        analysisCustomerWeek(uid)
    main3()


def main():
    result = getAllUser()
    for r in result:
        uid = r["uid"]
        analysisCustomer(uid)

def main2():
    result = getAllUser()
    for r in result:
        uid = r["uid"]
        analysisCustomerWeek(uid)


if __name__ == "__main__":
    #main2()
    # weekAnalysis("2014-05-20")
    # monthAnalysis("2014-04")
    # monthAnalysis("2014-05")
    # monthAnalysis("2014-06")
    # monthAnalysis("2014-07")
    # monthAnalysis("2014-08")
    #main3()
    initialDate = datetime.date(2014,11,1)

    for i in range(0,25):
        d = initialDate + datetime.timedelta(days = i)
        print "begin process"
        print d
        dailyCountSpecial(d)






