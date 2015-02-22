#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = '''
Check if package_id in REDIS which "product_status" is "waitdeliver" & add.
'''

import os
import sys
import urllib2,urllib
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import DBAccess,getMongoDBConn
from orders.models import getPackage
from shop_admin.models import pickExpressByPackageId
from utility.utils import getRedisObj
import random


class Patch():
    def __init__(self):
        self.packageIdInRedis = []
        self.packageIdInWait = []

    def _fetchPackageIdInRedis(self):
        print "Query package id in redis."
        r = getRedisObj()
        wait = r.smembers("wait_deliver_package_to_print")
        printing = r.smembers("wait_deliver_package_printing")
        printed  = r.smembers("wait_deliver_package_printed")
        _ret = list(wait) + list(printed) + list(printing)
        self.packageIdInRedis = list(set(_ret))

    def _fetchPackageIdInWait(self):
        print "Query package id in order_goods."
        db = DBAccess()
        db.dbName = "billing_record_db"
        sql = "select package_id from order_goods where product_status='waitdeliver'"
        datas = db.execQueryAssoc(sql)
        ret = []
        if not datas or len(datas) == 0:
            return []
        for row in datas:
            ret.append(row['package_id'])
        self.packageIdInWait = list(set(ret))

    def _fix(self):
        print "Fixing...",
        self._fetchPackageIdInRedis()
        self._fetchPackageIdInWait()
        print self.packageIdInRedis
        print self.packageIdInWait
        if not self.packageIdInRedis or len(self.packageIdInRedis) <= 0:
            print "NO packageid in REDIS , BYE."
            return

        if not self.packageIdInWait or len(self.packageIdInWait) <= 0:
            print "NO packageid in wait delivery,BYE"
            return

        r = getRedisObj()
        added = []
        for packageId in self.packageIdInWait:
            if str(packageId) in self.packageIdInRedis:
                continue

            if packageId == 0:
                continue

            added.append(packageId)
            r.sadd("wait_deliver_package_to_print",packageId)
        print "done."
        print "Package Id below had been add to REDIS."
        print "= END ="
        for a in added:
            print a


    def fix(self):
        self._fix()

if __name__ == "__main__":
    p = Patch()
    p.fix()