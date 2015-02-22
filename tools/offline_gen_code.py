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
from utility.utils import getRedisObj
from coupon.models import deliverCashCoupon
from coupon.models import getCouponActivity
import time,random

def genSingleCode():
	currentTimeStamp = str(int(time.time()))
	currentTimeStamp = currentTimeStamp[3:10]
	randomSuffix = str( random.randint(10000,99999))
	finalCode = currentTimeStamp + randomSuffix
	return finalCode

def genGiftCountForActivity(totalCount, activityId):
	for i in range(0,totalCount):
		r = getRedisObj(rdb = 2)
		finalCode = genSingleCode()
		while r.exists(finalCode):
			finalCode = genSingleCode()
		r.set(finalCode,str(activityId))
		print finalCode


args = sys.argv
genGiftCountForActivity(int(args[1]),args[2])

