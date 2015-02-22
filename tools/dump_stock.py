#coding: utf-8

import os
import sys
import datetime
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from check_bill.models import getResultFromMySQL, transMysqlExec,getUpdateSql
from stock_log.barcode_models import BARCODE_LOG
from utility.utils import NewSQLInsertBuilder, getMongoDBConn, getNowUTCtime ,DBAccess

def getAllStorageLocation():

    query_dict = {}
    fields = ["storage_type", "id"]
    t_result = getResultFromMySQL("stock_log_db", "storage_location", query_dict=query_dict, fields=fields, page='nopage')
    result = { x["id"]: x["storage_type"] for x in t_result }
    return result


def insert_sku():
    query_dict = {
       "stock_location_id__gt": 0,
    }
    result = getResultFromMySQL("stock_log_db", "stock_location_barcode", query_dict=query_dict, page='nopage')

    shop_db = getMongoDBConn().shop
    storage_type_dict = getAllStorageLocation()

    for item in result:

        sql_list = []

        barcode = item["barcode"]
        goods_id, size, _ = BARCODE_LOG.parse_barcode(barcode)

        goods = shop_db.goods.find_one({"_id":goods_id},{"brand_id": 1,"code": 1})
        if not goods:
            continue

        brand_id = goods['brand_id']
        code = goods['code']

        sql1 = NewSQLInsertBuilder(item, "stock_location_barcode")

        sql_list.append(sql1)

        obj_dict2 = {
            "stock_location_id": item['stock_location_id'],
            "goods_id": goods_id,
            "size": size,
            "count": 1,
            "code": code,
            "brand_id": brand_id,
        }

        sql2 = NewSQLInsertBuilder(obj_dict2, "stock_location_goods")
        sql2 += " ON DUPLICATE KEY UPDATE count=count+1"
        sql_list.append(sql2)

        storage_type = storage_type_dict.get(item['stock_location_id'])
        if storage_type == '1':
            #待退货区
            table_name = "return_goods_stock"
        elif storage_type == "2":
            #库存区
            table_name = "storage_goods_stock"
        elif storage_type == "4":
            #待发货库区
            table_name = "sending_goods_stock"
            obj_dict4 = {
                "barcode": barcode,
                "status": "free",
                "goods_id": goods_id,
                "size": size,
                "create_time":  getNowUTCtime(),
            }
            sql4 = NewSQLInsertBuilder(obj_dict4, "barcode_order_goods")
            sql_list.append(sql4)
        else:
            continue # 忘记 continue  wtf!!!!

        obj_dict3 = {
            "brand_id": brand_id,
            "goods_id": goods_id,
            "size": size,
            "locked_stock": 0,
            "free_stock": 1,
        }
        sql3 = NewSQLInsertBuilder(obj_dict3, table_name)
        sql3 += " ON DUPLICATE KEY UPDATE free_stock=free_stock+1"
        sql_list.append(sql3)

        try:
            transMysqlExec("xiaoher_stock_db", sql_list, print_sql=False)
            print "barcode:%s insert done" % barcode
        except Exception as e:
            print e
            continue


def init_stock():

    from stock_log.models import init_purchase

    query_dict = {
        "sql": " and product_status in ('purchase','picking')"
    }

    fields = ["brand_id"]

    result = getResultFromMySQL("billing_record_db", "order_goods", query_dict=query_dict, fields=fields, page="nopage", group_by="group by brand_id")

    for r in result:
        brand_id = r["brand_id"]
        init_purchase(brand_id)


def debug_stock():

    with open("dump_stock_log") as f:
        lines = f.readlines()

    for line in lines:
        table_name, barcode = line.strip().split()
        sql_list = []
        goods_id, size, _ = BARCODE_LOG.parse_barcode(barcode)
        # print table_name, barcode
        query_dict = {
            "goods_id": goods_id,
            "size": size,
            "free_stock__gt": 0,
        }
        update_dict = {"sql": "free_stock=free_stock-1"}

        sql = getUpdateSql(table_name, update_dict=update_dict, query_dict=query_dict)
        sql_list.append((sql, 1))


        query_dict = {
            "barcode": barcode,
        }

        result = getResultFromMySQL("xiaoher_stock_db", "stock_location_barcode", query_dict=query_dict, fields=['*'])

        if not result:
            print "barocode:%s not found" % barcode
            continue
        else:
            stock_location_id = result[0]['stock_location_id']

        query_dict = {
            "stock_location_id": stock_location_id,
            "goods_id": goods_id,
            "size": size,
            "count__gt": 0,
        }
        update_dict = {"sql": "count=count-1"}
        sql = getUpdateSql("stock_location_goods", update_dict=update_dict, query_dict=query_dict)
        sql_list.append((sql, 1))

        sql = "delete from stock_location_barcode where barcode='%s'" % barcode
        sql_list.append((sql, 1))

        try:
            transMysqlExec("xiaoher_stock_db",sql_list=sql_list,print_sql=True)
        except :
            import traceback
            print traceback.format_exc()


def init__sending_goods_stock(product_id=None):

    db = DBAccess()
    db.dbName = "xiaoher_stock_db"

    query_dict = {}
    if product_id is not None:
        query_dict['goods_id'] = product_id

    fields = ['count(*) as count', "goods_id", "size", "status", "barcode"]
    result = getResultFromMySQL("xiaoher_stock_db", "barcode_order_goods", query_dict=query_dict, fields=fields,
                                group_by="group by goods_id,size,status", page="nopage")
    goods_dict = {}
    for r in result:
        goods_id = r['goods_id']
        size = r['size']
        key = "%s__%s" % (goods_id,size)

        if key not in goods_dict:
            goods_dict[key] = {
                "locked_stock": 0,
                "free_stock": 0,
            }

        if r['status'] in ("blocked", "delivering"):
            goods_dict[key]['locked_stock'] += r['count']

        elif r['status'] in ("free", ):
            goods_dict[key]['free_stock'] += r['count']


    for key,t in goods_dict.iteritems():

        goods_id, size = key.split('__')
        goods_id = int(goods_id)

        query_dict = {
            "goods_id": goods_id,
            "size": size,
        }

        fields = ['*']

        t_result = getResultFromMySQL("xiaoher_stock_db", "sending_goods_stock", query_dict=query_dict, fields=fields)
        if not t_result:
            print "not found the %s %s " % (goods_id, size)
            continue

        t_result = t_result[0]
        if t_result['locked_stock'] + t_result['free_stock'] != t['locked_stock'] + t['free_stock']:
            print "not equals the %s %s " % (goods_id, size)
            #continue

        if t_result['locked_stock'] == t['locked_stock'] and t_result['free_stock'] == t['free_stock']:
            continue

        update_dict = {
            "locked_stock": t["locked_stock"],
            "free_stock": t["free_stock"],
            "sql": "version=version+1",
        }

        query_dict['version'] = t_result['version']

        sql_list = []

        sql = getUpdateSql("sending_goods_stock", update_dict=update_dict, query_dict=query_dict)

        sql_list.append(sql)

        t_result.pop("version")
        t_result.pop("update_time", '')
        t_result['create_time'] = getNowUTCtime()
        t_result['source'] = "sync_stock"
        t_result['free_stock'] = t['free_stock']
        t_result['locked_stock'] = t['locked_stock']

        sql2 = NewSQLInsertBuilder(t_result, "sending_area_stock_flow")

        sql_list.append(sql2)

        try:
            transMysqlExec("xiaoher_stock_db", sql_list,print_sql=False)
            print goods_id,size,t['locked_stock'],t['free_stock']
        except:
            import  traceback
            print traceback.format_exc()


def fix_barcode_order_goods():

    db = DBAccess()
    db.dbName = "xiaoher_stock_db"
    sql = "select order_goods_id,goods_id,size,count(*) as count from barcode_order_goods where status = 'blocked' group by order_goods_id,goods_id,size having count(*) >1;"
    result = db.execQueryAssoc(sql)

    for r in result:

        order_goods_id = r['order_goods_id']
        count = r['count']
        query_dict = {
            "id": order_goods_id,
        }
        fields = ['count', 'product_status']

        t = getResultFromMySQL("billing_record_db", "order_goods", query_dict=query_dict,fields=fields)
        if t[0]['count'] == count:
            print "count is equal"
            continue
        
        else:
            print order_goods_id,count


        t = t[0]
        if t['product_status'] in ("packing", "packed", "picking", "purchase"):

            sql = "update order_goods set product_status='purchase' where id=%s" % order_goods_id
            db.dbName = "billing_record_db"
            db.execQuery(sql)

            sql = "update barcode_order_goods set status='free' where order_goods_id=%s" % order_goods_id
            db.dbName = "xiaoher_stock_db"
            db.execQuery(sql)

        if t['product_status'] in ("delivering", ):

            sql = "update barcode_order_goods set status='free' where order_goods_id=%s and status !='delivered' " % order_goods_id
            db.dbName = "xiaoher_stock_db"
            db.execQuery(sql)

        if t['product_status'] in ("waitdeliver", ):

            query_dict = {
                "order_goods_id": order_goods_id
            }
            fields = ['status', 'barcode']

            _b = getResultFromMySQL("xiaoher_stock_db", "barcode_order_goods", query_dict=query_dict, fields=fields, page="nopage")

            barcode_list = []
            for _t in _b:
                if _t['status'] in ("delivering",):
                    continue
                else:
                    barcode_list.append(_t['barcode'])

            if len(_b) - len(barcode_list) < t['count']:

                _m = t["count"] - (len(_b) - len(barcode_list))
            else:
                _m = 0
            barcode_list = barcode_list[_m:]

            if not barcode_list:
                continue

            sql = "update barcode_order_goods set status='free' where barcode in (%s) " % ','.join(barcode_list)
            db.dbName = "xiaoher_stock_db"
            db.execQuery(sql)

        else:
            continue

        init__sending_goods_stock(order_goods_id)


def fix_waitdeliver_order_goods(goods_id=None):

    from stock_log.barcode_models import BARCODE_LOG
    def _findBarcode(barcode_result, c):

        barcode_list = []

        for item in barcode_result:
            if item['status'] == "blocked":
                barcode_list.append(item['barcode'])

            if len(barcode_list) == c:
                return barcode_list


        for item in barcode_result:
            if item['status'] == "delivering":
                barcode_list.append(item['barcode'])

            if len(barcode_list) == c:
                return barcode_list

        return barcode_list


    query_dict = {
        "product_status": "waitdeliver",
    }
    if goods_id is not None:
        query_dict['original_goods_id'] = goods_id

    fields = ['order_no', "id as order_goods_id", "count"]
    result = getResultFromMySQL("billing_record_db", "order_goods", query_dict=query_dict, fields=fields, page="nopage")

    for item in result:
        order_no = item['order_no']
        order_goods_id = item['order_goods_id']
        count = item['count']

        query_dict = {
            "order_no": order_no,
            "order_goods_id": order_goods_id,
            "sql": " and status in ('blocked','delivering','delivered') "
        }

        fields = ['barcode','status']
        _b = getResultFromMySQL("xiaoher_stock_db", "barcode_order_goods", query_dict=query_dict,fields=fields)

        if len(_b) == count:
            continue

        _c = len(_b) - count

        if _c < 0:
            print "不满足实际需要 %s" % order_no
            continue

        barcode_list = _findBarcode(_b, _c)

        if len(barcode_list) != _c:
            print "barcode_list 不满足实际需要 %s" % order_no
            continue

        print barcode_list
        continue

        for barcode in barcode_list:
            t = BARCODE_LOG(stock_location_id=0,barcode=barcode,source="cancelled_barcode_locked", operator="系统")
            if not t.result:
                print "fail"

if __name__ == "__main__":
    # insert_sku()
    # debug_stock()
    #fix_barcode_order_goods()
    init__sending_goods_stock(221493)
