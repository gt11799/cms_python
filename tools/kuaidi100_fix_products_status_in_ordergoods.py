#coding:utf8
__author__ = 'Liang Yejin'

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from kuaidi100.models import kuaidi_const
from utility.utils import DBAccess

import os
import sys
# import datetime



class Fix():
    def __init__(self):
        self.db = DBAccess()
        self.db.dbName = "billing_record_db"
        self.auto_sign_packages = []
        self.delined_packages = []

    def fetchRecordNeedFix(self):
        arr = [kuaidi_const.PACKAGE_STATUS_AUTO_SIGN,kuaidi_const.PACKAGE_STATUS_DECLINED]
        ret = []
        for s in arr:
            sql = "select package_id,ftime from package_flow where state='{0}'".format(s)
            datas = self.db.execQueryAssoc(sql)
            ret.append(datas)
        [self.auto_sign_packages, self.delined_packages] = ret

    def fix(self):
        self._fix()

    def _fix(self):

        self.fetchRecordNeedFix()
        print "Start fix..."
        if self.auto_sign_packages == [] and self.delined_packages == []:
            print "No packages need be fix."
            return

        tempcount = 0
        print "updating auto_sign package."
        total = len(self.auto_sign_packages)
        for row in self.auto_sign_packages:
            package_id,ftime = row['package_id'],row['ftime']
            # update status in TABLE order_goods
            sql = "update order_goods set product_status='{0}' where package_id='{1}' and  \
            (product_status in （'delivering','finished','complete'))\
             ".format("auto_sign",package_id)
            self.db.execNonQuery(sql)
            # print sql
            tempcount += 1
            remain = total - tempcount
            if remain % 57 == 0:
                print "remain:",remain

            # send goupon fee
            # sql = "select order_no from order_goods where package_id={0}".format(package_id)
            # r = self.db.execQueryAssoc(sql)
            # for x in r:
            #     handleOrderFinishedMessage(x)


        print "Fix:update order_goods for auto_sign package (fiexd/all):{0}/{1}".format(tempcount,
                                                                                        len(self.auto_sign_packages))
        tempcount = 0
        total = len(self.delined_packages)
        for row in self.delined_packages:
            package_id,ftime = row['package_id'],row['ftime']
            sql = "update order_goods set product_status='{0}' where package_id='{1}' and \
            (product_status in ('delivering','finished','complete'))\
             ".format("declined",package_id)
            self.db.execNonQuery(sql)
            tempcount += 1
            remain = total - tempcount
            if remain % 57 == 0:
                print "remain:",remain
        print "Fix:update order_goods for declined package (fiexd/all):{0}/{1}".format(tempcount,
                                                                                        len(self.delined_packages))
        print "Done."

def unit_test():
    patch = Fix()
    patch.fix()

if __name__ == "__main__":
    unit_test()

