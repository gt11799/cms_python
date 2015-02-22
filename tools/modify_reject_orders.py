#!/usr/bin/env python
# -*- coding: utf-8 -*-

#coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess
import xlrd

print len(sys.argv)

test = False 
if len(sys.argv) == 2 or len(sys.argv) == 3:
	path = sys.argv[1]
	if len(sys.argv) == 3 and sys.argv[2] == 'test':
		test = True
else:
	path = 'test.xlsx'

print 'test',test
print path

'''
订单编号			快递单号
14114365904221 	D066375318
14098960992804 	D066215031
14107607021365 	D066215108
14094805853342 	D066219955
14104031625052 	D061675403

'''
book = xlrd.open_workbook(path) 
table = book.sheet_by_index(0)

d = {}
for rownum in range(1,table.nrows):
	row = table.row_values(rownum)
	order_no = str(int(float(row[0])))
	deliver_no = str(int(float(row[1])) if type(row[1]) == float else row[1]).strip()
	k = (order_no,deliver_no)
	d[k] = order_no

db = DBAccess()
db.dbName = 'billing_record_db'
#orders_sql = orders_sql_base = "update orders set order_status='declined' where "
order_goods_sql = order_goods_sql_base = "update order_goods set product_status='declined' where "

item_len = len(d)
for i,x in enumerate(d.keys()):

        order_goods_sql = order_goods_sql_base = "update order_goods set product_status='declined' where "
        result = db.execQueryAssoc("select * from order_goods where product_status !='declined' and order_no='%s' and deliver_no='%s' "% (x[0],x[1]))
        if result:
            #orders_sql += " order_no='%s' " % (x[0],)
	    order_goods_sql += " order_no='%s' and deliver_no='%s' " % (x[0],x[1])
            print order_goods_sql
	#if i % 10 == 0 and i != 0 or item_len-i == 1:
	#	print ''
	#	print item_len,i,orders_sql
	#	print item_len,i,order_goods_sql
	#	db.execNonQuery(orders_sql)
	    db.execNonQuery(order_goods_sql)
	#	orders_sql = orders_sql_base
	#	order_goods_sql = order_goods_sql_base
	#else:
	#	orders_sql += ' or '
	#	order_goods_sql += ' or '

	# #orders_sql += " order_no='%s' " % (x[0],)
	# order_goods_sql += " (order_no='%s' and deliver_no='%s') " % (x[0],x[1])
	# if i % 10 == 0 and i != 0 or item_len-i == 1:
	# 	print ''
	# 	#print item_len,i,orders_sql
	# 	print item_len,i,order_goods_sql
	# 	#db.execNonQuery(orders_sql)
	# 	if not test:
	# 		db.execNonQuery(order_goods_sql)
	# 	#orders_sql = orders_sql_base
	# 	order_goods_sql = order_goods_sql_base
	# else:
	# 	#orders_sql += ' or '
	# 	order_goods_sql += ' or '




'''
14080849651835 | 18572422     |
14081779618602 | 1q2w3e4r     |
14085205351682 | V217061874   |
14085205351682 | V217061874   |
14090212682901 | 280188665927 |
14090212682901 | 1q2w3e4r     |
14090212682901 | 1q2w3e4r     |
14090213023243 | V217061874   |
14090356507083 | 45211        |
14090361250067 | V217061874   |

select order_no,order_status from orders where 
order_no='14081779618602' or 
order_no='14085205351682' or 
order_no='14090212682901' or 
order_no='14090213023243' or 
order_no='14090356507083' or 
order_no='14090361250067';
'''

'''
orders_sql = orders_sql_base = "select order_no,order_status from orders where "
order_goods_sql = order_goods_sql_base = "select order_no,deliver_no,product_status from order_goods where "
item_len = len(d)
for i,x in enumerate(d.keys()):
	orders_sql += " order_no='%s' " % (x[0],)
	order_goods_sql += " (order_no='%s' and deliver_no='%s') " % (x[0],x[1])
	if i % 3 == 0 and i != 0 or item_len-i == 1:
		print ''
		print orders_sql
		result = db.execQueryAssoc(orders_sql)
		print result

		print order_goods_sql
		result = db.execQueryAssoc(order_goods_sql)
		print result
		orders_sql = orders_sql_base
		order_goods_sql = order_goods_sql_base
	else:
		orders_sql += ' or '
		order_goods_sql += ' or '
'''
