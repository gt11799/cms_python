# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
from orders.models import getAddressInfo,getHumanAddress

from utility.utils import DBAccess

from register.models import encryPassword


sql = "select uid,password from xh_user where length(password) != 32"
db = DBAccess()
db.dbName = "billing_record_db"

result = db.execQueryAssoc(sql)
for r in result:
    uid = r["uid"]
    password = r["password"]
    en_password = encryPassword(password)
    print password
    sql = "update xh_user set password='%s'  where uid=%s"%(en_password,uid)
    db.execQuery(sql)