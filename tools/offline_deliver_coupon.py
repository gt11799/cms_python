# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
try:
    from settings import HOST
except:
    HOST = "http://127.0.0.1:8000"
import urllib2

from coupon.models import deliverCashCoupon
import datetime
count  = 4
uid = str(100165)
i = 0
for i in range(0,count):
	deliverCashCoupon(uid,datetime.datetime.now(),100,limitedOrderPrice = 200,availIntevalDay = 180,source='分享给好友',
		activityId = -2)


