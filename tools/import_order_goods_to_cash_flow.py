##coding:utf-8
import os
import sys
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess
import datetime
from shop_admin.models import getDetailOrderGoodsfee,updateCashFlowStatusById
from orders.models import getKuaiDiCompany
import json
import urllib2
import time
def addCashFlowRecord():
    '''根据order_id生成cash_flow记录'''
    sql = "select * from order_goods where id>31655"

    db = DBAccess()
    db.dbName = "billing_record_db"
    r = db.execQueryAssoc(sql)
    for x in r:
        if x["payment_method"] == "0":#货到付款添加一条记录
            result = {}
            result["order_no"] = x["order_no"]
            result["order_goods_id"] = x["id"]
            result["product_name"] = x["product_name"]
            result["deliver"] = x["deliver"]
            result["deliver_no"] = x['deliver_no']
            result["fee"] = getDetailOrderGoodsfee(x,'revised_should_pay')
            insertCashFlow(result)
def insertCashFlow(Arguments):
    '''插入一条记录到财务账目流水表 cash_flow'''

    order_no = Arguments["order_no"]
    order_goods_id = Arguments["order_goods_id"]
    product_name = Arguments["product_name"]
    deliver = Arguments["deliver"]
    deliver_no = Arguments["deliver_no"]
    fee = Arguments["fee"]
    create_time = datetime.datetime.now()
    sql = "insert into cash_flow(order_goods_id,order_no,product_name,deliver,deliver_no,fee,create_time,status) " \
          "values(%s,'%s','%s','%s','%s',%s,'%s','%s');" %(order_goods_id,order_no,product_name,deliver,deliver_no,fee,create_time,'not_sign')
    print(sql)
    db = DBAccess()
    db.dbName = "billing_record_db"
    db.execNonQuery(sql)

def autoSign():
    sql = "select * from cash_flow where status!='finished' and status!='1' and status!='2' and deliver_no!='' limit 50"

    db = DBAccess()
    db.dbName = "billing_record_db"
    cash_flow_list = db.execQueryAssoc(sql)

    for x in cash_flow_list:
        time.sleep(5)
        deliver = getKuaiDiCompany(x["deliver"])
        url = "http://www.kuaidi100.com/query?type="+deliver+"&postid="+x["deliver_no"]
        # url = "http://www.kuaidi100.com/query?type=yuantong&postid=D053500066"
        try:
            print(url)
            f = urllib2.urlopen(url)
            content = f.read()
            content_json = json.loads(content)
            print(content_json)
            try:
                if content_json["data"][0]["context"].find("签收")>-1 or content_json["data"][0]["context"].find("代收")>-1:
                    print(x["id"])
                    #更新财务账目流水
                    updateCashFlowStatusById(status="finished",id=x["id"])
                else:
                    updateCashFlowStatusById(status="1",id=x["id"])
            except:
                updateCashFlowStatusById(status="2",id=x["id"])

        except:
            pass


if __name__ == "__main__":
    # addCashFlowRecord()
    autoSign()