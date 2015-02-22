# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import DBAccess,NewSQLInsertBuilder
db = DBAccess()
db.dbName = "appsupport"

with open("phone.txt") as f:
    for line in f:
        line = line.split(',')
        phone = line[0]
        app_type = line[1]
        dataDict = {"phone":phone,"app_type":app_type,"sent_count":0}
        sql = NewSQLInsertBuilder(dataDict,"apps_phone_list")
        try:
            db.execQuery(sql)
        except Exception as e:
            print str(e)

