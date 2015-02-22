# coding:utf-8
import os
import sys
print "hello,window"
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess

#from shop_admin.models import NewSQLInsertBuilder,offlineDataCount

import datetime

sql = "select total_price,cargo_fee,client,create_time from orders where create_time > '2014-08-15 0:0:0'"

db = DBAccess()
db.dbName = "billing_record_db"

result = db.execQueryAssoc(sql)

final = {}
for r in result:
	createDate = r['create_time'].strftime("%Y-%m-%d")
	curPrice = r["total_price"] + r["cargo_fee"]

	if createDate in final:
		if r["client"] == "ios":
			final[createDate]["ios"] += curPrice
		elif r["client"] == "android":
			final[createDate]["android"] += curPrice
		elif r["client"] == "web":
			final[createDate]["web"] += curPrice
		elif r["client"] == "wap":
			final[createDate]["wap"] += curPrice
		else:
			final[createDate]["web"] += curPrice

	else:
		temp = {}
		temp["ios"] = 0
		temp["web"] = 0
		temp["wap"] = 0
		temp["android"] = 0

		final[createDate] = temp

		if r["client"] == "ios":
			final[createDate]["ios"] += curPrice
		elif r["client"] == "android":
			final[createDate]["android"] += curPrice
		elif r["client"] == "web":
			final[createDate]["web"] += curPrice
		elif r["client"] == "wap":
			final[createDate]["wap"] += curPrice
		else:
			final[createDate]["web"] += curPrice
finalResult = sorted(final.iteritems(), key = lambda d:d[0])

print "date,ios,android,web,wap"
for item in finalResult:
	dic = item[1]
	print item[0] + "," +  str(dic["ios"]) + "," + str(dic["android"]) + "," + str(dic["wap"]) + "," + str(dic["web"])




