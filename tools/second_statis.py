# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import *


import datetime


monthUV = {}
monthAver = {}

def countMonthUV(curDate):
    r = getRedisObj()
    dateStr = curDate.strftime("%Y-%m-%d")
    webCount = r.get("%s:web"%dateStr) or 0
    key = str(curDate.month)
    if key not in monthUV:
        monthUV[key] = int(webCount)
    else:
        monthUV[key] = monthUV[key] + int(webCount)

    monthAver[key] =  monthUV[key]/30
    pass

mobMonthUV = {}
mobMonthAver = {}
def countMobMonthUV(curDate):
    r = getRedisObj()
    dateStr = curDate.strftime("%Y-%m-%d")
    wapCount = r.get("%s:wap"%dateStr) or 0
    iosCount = r.get("%s:ios"%dateStr) or 0
    androidCount = r.get("%s:android"%dateStr) or 0

    totalCount = wapCount + iosCount + androidCount


    key = str(curDate.month)
    if key not in monthUV:
        mobMonthUV[key] = int(totalCount)
    else:
        mobMonthUV[key] = mobMonthUV[key] + int(totalCount)

    mobMonthAver[key] =  mobMonthAver[key]/30
    pass

monthOrders = {}
monthUsers = {}
def countOrdersAndAmount():
    db = DBAccess()
    db.dbName = "billing_record_db"
    for month in range(5,7):
        beginDate = datetime.datetime(year=2014,month=month,day=1)
        if month == 12:
            endDate = datetime.datetime(year=2015,month=1,day=1)
        else:

            endDate = datetime.datetime(year=2014,month=month+1,day=1)

        sql = "select count(order_no) from orders where create_time>'%s' and create_time<'%s' and client='web'"
        result = db.execQuery(sql)
        monthOrders[str(month)] = result[0][0]


        sql = "select count(distinct uid) from orders where create_time>'%s' and create_time<'%s' and client='web'"
        result = db.execQuery(sql)
        monthUsers[str(month)] = result[0][0]

users = {}
oldReturn = {}
oldDecline = {}
oldTotal = {}
newReturn = {}
newDecline = {}
newTotal = {}
def countNewAndOldReturn(curDate):
    print "begin process " + str(curDate)
    beginDate = "%s 0:0:0" % (curDate.strftime("%Y-%m-%d"),)
    endDate = "%s 23:59:59" % (curDate.strftime("%Y-%m-%d"),)
    print beginDate,endDate


    sql = "select product_status,uid from order_goods where create_time>'%s' and create_time<'%s'" % (beginDate,endDate,)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)

    key = str(curDate.month)

    for item in result:
        uid = item["uid"]
        if uid in users:
            oldTotal[key] = oldTotal.get(key,0) + 1

            if item['product_status'].find("return") != -1:
                oldReturn[key] = oldReturn.get(key,0) + 1

            if item['product_status'].find("declined") != -1:
                oldDecline[key] = oldDecline.get(key,0) + 1
        else:
            newTotal[key] = newTotal.get(key,0) + 1
            if item['product_status'].find("return") != -1:
                newReturn[key] = newReturn.get(key,0) + 1

            if item['product_status'].find("declined") != -1:
                newDecline[key] = newDecline.get(key,0) + 1


    sql = "select distinct uid from orders where create_time>'%s' and create_time<'%s'" % (beginDate,endDate,)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQuery(sql)
    for item in result:
        users[item[0]] = 1
    pass


def countSupplier():
    sql = "select address from buyer_brands_detail"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    cities = ["广州","东莞","浙江","深圳","北京","山东","江苏","上海","福建",'江西']
    dist = {}
    for item in result:
        address = item['address']
        for city in cities:
            if address.find("city") != -1:
                dist[city] = dist.get(city,0) + 1
            break


if __name__ == '__main__':
    initial = "2014-04-22"
    date = datetime.datetime.strptime(initial,"%Y-%m-%d")
    today = datetime.date.today()
    r = getRedisObj()
    '''
    while date.date() <= today:
        #countMonthUV(date)
        #countMobMonthUV(date)
        countNewAndOldReturn(date)
        date = date + datetime.timedelta(days = 1)
    
    monthUV = sorted(monthUV.iteritems(),key = lambda d:int(d[0]))
    for item in monthUV:
        print item[0] + "," + str(item[1])+ "," + str(monthAver[item[0]])


    print ""


    mobMonthUV = sorted(mobMonthUV.iteritems(),key = lambda d:int(d[0]))
    for item in mobMonthUV:
        print item[0] + "," + str(item[1])+ "," + str(mobMonthAver[item[0]])
    '''



    '''
    newTotalTuple = sorted(newTotal.iteritems(), key = lambda d:int(d[0]))
    print newTotal
    print newReturn
    print newDecline
    print oldTotal
    print oldReturn
    print oldTotal
    for item in newTotalTuple:

        oldReturnRate = float(oldReturn.get(item[0],0)) / oldTotal.get(item[0],1)
        oldDeclineRate = float(oldDecline.get(item[0],0)) / oldTotal.get(item[0],1)
        newReturnRate = float(newReturn.get(item[0],0)) / newTotal.get(item[0],1)
        newDeclineRate = float(newDecline.get(item[0],0)) / newTotal.get(item[0],1)
        print item[0] + "," +str(round(oldReturnRate,4)* 100) + "%," + str(round(oldDeclineRate,4)*100) + "%," +\
        str(round(newReturnRate,4)*100) + "%," + str(round(newDeclineRate,4)*100) + "%"
    '''


    countSupplier()



