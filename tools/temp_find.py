# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
import datetime

from utility.utils import DBAccess,getMongoDBConn


def incrMonth(date,n):
    m = date.month
    year = date.year
    m += n
    if m == 13:
        year = date.year + 1
        m = 1
    if m in (1,3,5,7,8,10,12):
        date = datetime.date(year,m,31)
    else:
        date = datetime.date(year,m,30)
    
    return date


def getSupplierCount(date):
    date = str(date)
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select supplier_id from new_purchase_list where purchase_time < '%s 23:59:59' group by supplier_id;"%date
    result = db.execQueryAssoc(sql)
    return len(result)


def getUserCount(date):
    date = str(date)
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid from orders where create_time < '%s 23:59:59' group by uid;"%date
    result = db.execQueryAssoc(sql)
    return len(result)

def supplierCount():
    start_date = datetime.date(2014,8,30)
    print "截至日期",'汇总','新增'
    while start_date < datetime.date(2015,1,1):
        
        a = getSupplierCount(start_date)
        b = getSupplierCount(incrMonth(start_date,-1))
        print start_date,a,a-b
        start_date = incrMonth(start_date,1)
        
def userCount():
    start_date = datetime.date(2014,5,31)
    print "截至日期",'汇总','新增'
    while start_date < datetime.date(2015,1,1):
        
        a = getUserCount(start_date)
        b = getUserCount(incrMonth(start_date,-1))
        print start_date,a,a-b
        start_date = incrMonth(start_date,1)
        




userSales = {}
def userTotalSales():
    sql = "select total_price,cargo_fee,uid from orders"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    for r in result:
        if r['uid'] not in userSales:
            userSales[r['uid']] = r['total_price']
        else:
            userSales[r['uid']] = userSales[r['uid']] + r['total_price']

def cityUserCount():
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select city_id,province,city from address group by city_id"
    result = db.execQueryAssoc(sql)
    for r in result:
        city_id = r['city_id'] 
        if city_id is None or city_id == "":
            continue
        sql = "select uid from address where city_id=%s group by uid"%city_id
        result = db.execQueryAssoc(sql)
        l = len(result)
        total = 0
        for rr in result:
            if rr['uid'] in userSales:
                total = total + userSales[rr['uid']]
        print '%s%s,%s,%f'%(r['province'],r['city'],l,round(total,2))

print "begin gen user sales data"
userTotalSales()
print "begin gen city data"
cityUserCount()
