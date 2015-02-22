# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from utility.utils import DBAccess

db = DBAccess()
db.dbName = "billing_record_db"
sql = " select distinct uid from orders where create_time>='2014-08-01 0:0:0' and create_time<'2014-09-01 0:0:0'"
result = db.execQueryAssoc(sql)
count = 0
print "8 : " + str(len(result)) 


def printUsernameAndPhone(uid):
	sql = "select username,phone from xh_user where uid=%s" %(str(uid),)
	db = DBAccess()
	db.dbName = "billing_record_db"

	tResult = db.execQueryAssoc(sql)
	if tResult:
		print tResult[0]["username"] + ","+tResult["phone"]



for item in result:
	sql = "select username,phone from xh_user where uid=%s" %(item["uid"],)
	tResult = db.execQueryAssoc(sql)
	if tResult:
		printUsernameAndPhone(item["uid"])

print ""
print ""
print ""
print ""
print ""

for item in result:
    uid = item[0]
    sql = "select * from orders where create_time>='2014-09-01 0:0:0' and create_time<'2014-10-01 0:0:0' and uid=%s" %(str(uid),)
    result1 = db.execQuery(sql)
    if result1:
    	printUsernameAndPhone(uid)
        count = count + 1



