#coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
@countTime
def getPackageId():
    sql = "select distinct package_id from package_flow where deliver_time>'2014-11-08 0:0:0' and package_id!=0"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)
    return [int(x['package_id']) for x in result]
    pass

@countTime
def performanceTest1(pids):
    db = DBAccess()
    db.dbName = "billing_record_db"


    final = []
    for pid in pids:
        sql = "select * from order_goods where package_id=%s" %  (str(pid),)
        result = db.execQueryAssoc(sql)
        for item in result:        
            final.append(item)
    return final

    pass 

@countTime
def performanceTest2(pids):
    db = DBAccess()
    db.dbName = "billing_record_db"

    sql = "select * from order_goods where package_id in %s" % str(tuple(pids))
    result = db.execQueryAssoc(sql)

    return result

@countTime
def performanceTest3():
    #pids = getPackageId()
    db = DBAccess()
    db.dbName = "billing_record_db"

    sql = "select * from order_goods,package_flow where order_goods.package_id=package_flow.package_id and package_flow.deliver_time>'2014-11-08 0:0:0'"

    result = db.execQueryAssoc(sql)
    return result
    pass



if __name__ == "__main__":
    import sys
    pids = getPackageId()
    print len(performanceTest1(pids))
    print len(performanceTest2(pids))
    print len(performanceTest3())

    
