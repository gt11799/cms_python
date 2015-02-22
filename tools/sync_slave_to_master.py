# coding:utf-8

##在从机上面运行

import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import DBAccess


db1 = DBAccess()
db1.host = "127.0.0.1"

db2 = DBAccess()
db2.host = "10.168.20.1"


sql1 = "select * from package_flow where deliver_time>='2014-10-08 00:00:00'"
result = db1.execQueryAssoc(sql1)

for r in result:
    package_id = r["package_id"]
    sql2 = "select package_id from package_flow where package_id=%s"%package_id
    if db2.execQueryAssoc(sql2):
        continue
    else:
        print package_id,r["deliver_no"],r["deliver"]
