#coding:utf8
import sys,os


path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getRedisObj

from utility.utils import DBAccess


from shop_admin.models import pickExpressByPackageId
__author__ = 'David'


class Tester():
    def __init__(self):
        self.num = 0

    def _fetch(self):
        # db = DBAccess()
        # db.dbName = "billing_record_db"
        # sql = "select package_id from order_goods where product_status = 'waitdeliver' group by package_id;"
        # print sql
        # self.datas = db.execQueryAssoc(sql)
        r = getRedisObj()
        packageIds = list(r.smembers("wait_deliver_package_to_print"))
        packageIds += list(r.smembers("wait_deliver_package_printing"))
        self.datas = packageIds
        print "len of self.datas is {}".format(len(self.datas))


    def test(self):
        self._fetch()
        db = DBAccess()
        db.dbName = "billing_record_db"
        count = 0
        for data in self.datas:
            ret = pickExpressByPackageId(data)
            print ret
            sql = "select address_id,order_no from order_goods where package_id={0}".format(data)
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
            count += 1
            print "=-=-"*10
        print "{} lines".format(count)

    def reassign(self):
        self._fetch()
        db = DBAccess()
        db.dbName = "billing_record_db"
        fp = open("package_reassign.log","w")
        for data in self.datas:
            ret = pickExpressByPackageId(data)
            print ret
            sql = "update order_goods set deliver = '{}' where package_id = {} ".format(ret,data)
            print sql
            db.execNonQuery(sql)
            fp.write(ret)
            sql = "select address_id,order_no from order_goods where package_id={0}".format(data)
            try:
                ret = db.execQueryAssoc(sql)[0]
            except:
                fp.write("No address_id")
                print "No address_id"
                continue

            sql = "select province,city,district,street from address where address_id={0} limit 1;".format(ret['address_id'])
            try:
                add = db.execQueryAssoc(sql)
                humanAddr = ""
                for k,v in add[0].items():
                    humanAddr += v
                print humanAddr
                fp.write(humanAddr)

            except:
                fp.write("no address")
                print "no address"

            print "=-=-"*10
            fp.write("=-=-"*10)
        fp.close()


if __name__ == "__main__":
    try:
        action = sys.argv[1]
        assert action in ['test','reassign']
    except:
        print "reassignPackageDeliver.py test or reassign"
        exit()

    t = Tester()
    getattr(t,action)()



