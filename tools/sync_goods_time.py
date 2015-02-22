##coding:utf-8

import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import getMongoDBConn,DBAccess,getNowUTCtime
from shop_admin.models import getTaobaoSource

conn = getMongoDBConn()
db = conn.shop

def sync_time():
    '''同步商品上线线时间'''
    mysql = DBAccess()
    mysql.dbName = "backend_log_db"
    activity_list = db.activity.find({"status":{"$in":[3,-3]}}).sort("end_time",1)

    for x in activity_list:
        activity_goods = x.get("goods_id",[])
        for k in activity_goods:
            goods = db.activity_goods.find_one({"_id":k},{"goods_id":1})
            if goods:
                goods_id = goods.get("goods_id",0)

                if goods_id:
                    print(goods_id)
                    start_time = x["start_time"]
                    end_time = x["end_time"]
                    now_time = getNowUTCtime()

                    sql = "insert into goods_time_log(create_time,goods_id,start_time,end_time,operator) " \
                                      "values('%s',%s,'%s','%s','%s');" %(now_time,goods_id,start_time,end_time,"")
                    print(sql)
                    mysql.execNonQuery(sql)



if __name__ == "__main__":
    sync_time()
    print("完成")