# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


from utility.utils import DBAccess

db = DBAccess()


class fixUser:

    def __init__(self):

        db.dbName = "billing_record_db"


    def findTheSameUid(self):

        sql = "select uid,count(uid) as count_uid from xh_user group by uid having(count(uid)>1);"
        result = db.execQueryAssoc(sql)


    def findSameUidHaveOrders(self):

        result = self.findTheSameUid()
        for item in result:
            uid = item["uid"]
            sql = "select uid,order_no from orders where uid=%s"%uid
            orders = db.execQueryAssoc(sql)
            for o in orders:
                print o["uid"],o["order_no"]


def main():
    from optparse import OptionParser

    parse  = OptionParser(version='0.1 by haifang')

    parse.add_option('-o','--orders',help="find the same uid's orders",nargs=0)

    options,parse = parse.parse_args()
    print options

    if options.orders:
        fixUser().findSameUidHaveOrders()


if __name__ == '__main__':
    main()

