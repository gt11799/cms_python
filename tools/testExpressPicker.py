#coding:utf8
import sys,os

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import DBAccess


from shop_admin.models import pickExpressByPackageId
__author__ = 'David'


class Tester():
    def __init__(self,num):
        self.num = num

    def _fetch(self):
        db = DBAccess()
        db.dbName = "billing_record_db"
        sql = "select distinct(package_id) from order_goods where product_status='waitdeliver' order  by package_id desc limit {};".format(self.num)
        print sql
        self.datas = db.execQueryAssoc(sql)
        print "len of self.datas".format(len(self.datas))

    def test(self):
        self._fetch()
        db = DBAccess()
        db.dbName = "billing_record_db"
        for data in self.datas:
            ret = pickExpressByPackageId(data['package_id'])
            print ret

            sql = "select address_id,order_no from order_goods where package_id={0}".format(data['package_id'])
            try:
                ret = db.execQueryAssoc(sql)[0]
            except:
                print "No address_id"
                continue

            sql = "select province,city,district,street from address where address_id={0} limit 1;".format(ret['address_id'])

            try:
                add = db.execQueryAssoc(sql)
                humanAddr = ""
                for k,v in add[0].items():
                    humanAddr += v
                print humanAddr

            except:
                print "no address"
            print "=-=-"*10




if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
    except:
        num = 20

    t = Tester(num)
    t.test()



