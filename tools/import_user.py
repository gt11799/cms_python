# coding:utf-8
import os
import sys
print "hello,window"
import datetime
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime


def import1():
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid from orders where create_time >'2014-07-01 00:00:00' and create_time <'2014-07-31 23:59:59' "
    result1 = db.execQueryAssoc(sql)
    sql = "select uid from orders where create_time >'2014-08-01 00:00:00' and create_time <'2014-08-31 23:59:59' "
    result2 = db.execQueryAssoc(sql)

    uidDict = {}
    uids = []
    for r in result1:
        uid = r["uid"]
        uidDict[uid] = ''

    for r in result2:
        uid = r["uid"]
        if uid in  uidDict and uid not in uids:
            uids.append(uid)


    return uids

def import2():
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select uid from orders where create_time >'2014-06-01 00:00:00' and create_time <'2014-06-01 23:59:59' "
    result1 = db.execQueryAssoc(sql)
    sql = "select uid from orders where create_time >'2014-07-01 00:00:00' and create_time <'2014-08-31 23:59:59' "
    result2 = db.execQueryAssoc(sql)

    uidDict = {}
    uidDict2 = {}
    uids = []
    for r in result1:
        uid = r["uid"]
        uidDict[uid] = ''

    for r in result2:
        uid = r["uid"]
        uidDict2[uid] = ''
    for uid in uidDict:
        if uid not in uidDict2:
            uids.append(uid)


    return uids

def getUserInfo(uid):
    db = DBAccess()
    db.dbName = "billing_record_db"
    sql = "select * from orders where uid=%s order by create_time limit 1"%uid
    result = db.execQueryAssoc(sql)
    return result[0]


def main():
    uids = import2()
    with open("users06.txt","w") as f:
        for uid in uids:
            r = getUserInfo(uid)
            f.write("%s,%s,%s\n"%(r["receiver_name"],r["phone"],r["human_address"]))


if __name__ == "__main__":
    main()
