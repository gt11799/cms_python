# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import DBAccess

sql = "select date_format(create_time,'%Y-%m-%d') \
    as count_date,sum(paid_by_coupon) as paid_by_coupon ,\
    sum(paid_by_hercoin) as paid_by_hercoin  from orders group by count_date;"



db = DBAccess()

db.dbName = "billing_record_db"

result = db.execQueryAssoc(sql)

for r in result:
    sql = "update data_count set paid_by_coupon=%s,paid_by_hercoin=%s \
        where count_date='%s'"%(r["paid_by_coupon"],r["paid_by_hercoin"],r["count_date"])

    db.execQuery(sql)