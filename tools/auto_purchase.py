# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getNowUTCtime,getRedisObj

from check_bill.models import getResultFromMySQL,updateItemToMysql


def autoPickingToPurchase():

    query_dict = {"product_status":"picking"}
    result = getResultFromMySQL("billing_record_db","order_goods",query_dict=query_dict,fields=["id","original_goods_id","product_size",
                                "count"],page="nopage",order_by="order by id desc")

    if not result:
        return
    goods_stock_dict = {} # 保存库存
    goods_need_stock_dict = {} #保存实际需要的库存
    goods_should_pass_dict = {} #保存pass的商品

    print "result length %s"%len(result)

    for r in result:
        original_goods_id = r["original_goods_id"]
        product_size = r["product_size"]
        key = "%s__%s"%(original_goods_id,product_size)

        if key not in goods_should_pass_dict:
            # query_dict  = {"product_status":"purchase","purchase_list_id__neq":-1,"original_goods_id":original_goods_id,"product_size":product_size}
            # 检查是否有采购
            query_dict  = {"product_status":"purchase","purchase_list_id__neq":-1,"original_goods_id":original_goods_id,}
            if getResultFromMySQL("billing_record_db","order_goods",query_dict=query_dict,page=1,pageNum=1):
                goods_should_pass_dict[key] = True
            else:
                goods_should_pass_dict[key] = False


            query_dict = {"original_goods_id":original_goods_id,"product_size":product_size,"product_status":"purchase","purchase_list_id":-1}
            fields = ["sum(count) as count"]
            purchase_stock = getResultFromMySQL("billing_record_db","order_goods",query_dict=query_dict,fields=fields,print_sql=False,page="nopage")
            goods_need_stock_dict[key] = purchase_stock[0]['count'] or 0

            # 获取库存
            query_dict = {"product_id":original_goods_id,"size":product_size}
            stock = getResultFromMySQL("billing_record_db","new_stock",query_dict=query_dict,fields=['*'],pageNum=1,page=1)
            if not stock:
                goods_stock_dict[key] = 0
            else:
                goods_stock_dict[key] = stock[0]['count'] or 0


        # 判断如果有此类商品在采购中，直接过滤，
        if goods_should_pass_dict[key]:
            print "goods_should_pass",key
            continue

        # 需要多少库存
        goods_need_stock_dict[key] += r["count"]

        # 判断有无库存
        if goods_need_stock_dict[key] > goods_stock_dict[key]:
            goods_should_pass_dict[key] = True
            print "goods_need_stock_lt_stock",key,goods_stock_dict[key]
            continue


    max_order_goods_id = result[0]["id"]
    for key,value in goods_should_pass_dict.items():
        if value:
            continue

        original_goods_id,product_size = key.split('__')
        print original_goods_id,product_size
        update_dict = {"product_status":"purchase","purchase_list_id":-1}
        query_dict = {"id__lte":max_order_goods_id,"original_goods_id":original_goods_id,"product_status":"picking","product_size":product_size}
        print updateItemToMysql("billing_record_db","order_goods",update_dict,query_dict,print_sql=False)

    query_dict = {"id__lte":max_order_goods_id,"product_status":"purchase","purchase_list_id":-1}
    result = getResultFromMySQL("billing_record_db","order_goods",query_dict=query_dict,fields=["id","uid"],page="nopage")

    from shop_admin.models import outOfStock,setpackDone

    for item in result:
        try:
            # outOfStock(item["id"],'系统')
            # setpackDone(item['uid'],item["id"],'系统')
            pass
        except Exception as e:
            print e




if __name__ == "__main__":
    autoPickingToPurchase()






