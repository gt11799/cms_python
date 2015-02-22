#!coding:utf8
import os
import sys

path =  os.path.dirname(__file__)
sys.path.append(os.path.join(path,".."))

__author__ = 'Liang Yejin'
import os
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from shop_admin.models import pickExpressByPackageId,queryExpressByAddress,checkZJSExpress
from utility.utils import DBAccess
import random
import sys
reload(sys)
sys.setdefaultencoding("utf8")

class MyTester():
    def __init__(self, testcaseNum = 20):
        self.testcaseNum = testcaseNum
        self.packageIds = []


    def _fetchPackageId(self):
        dbop = DBAccess()
        dbop.dbName = "billing_record_db"
        sql = "select count(*) from order_goods;"
        total = dbop.execQueryAssoc(sql)[0]["count(*)"]
        if self.testcaseNum > total:
            self.testcaseNum = total
            offset = 1
        else:
            offset = random.randint(1,total)
            while total-offset < self.testcaseNum:
                offset = random.randint(1, total)

        dbop = DBAccess()
        dbop.dbName = "billing_record_db"
        sql = "select package_id from order_goods where package_id<>0 order by package_id desc limit {1};".format(offset, self.testcaseNum)
        print sql
        ret = [t['package_id'] for t in dbop.execQueryAssoc(sql)]
        ret = list(set(ret))
        if ret[0] == 0:
            ret.pop(0)
        return ret

    def testAddress(self,address):
        unknownWords = ["不详", "我不清楚", "null","区/县","乡镇/街道"]
        _levels = []
        for l in address:
            l = l.strip()
            if l in unknownWords:
                _levels.append("")
            else:
                _levels.append(l)
        levels = _levels
        if levels[0] == "" or levels[1] == "":
            return []
        return queryExpressByAddress(*levels)

    def testZJSAddress(self,*address):
        return checkZJSExpress(*address)

    def test(self):
        ids = self._fetchPackageId()
        print "ids is [{0}]".format(ids)
        for packageId in ids:
            print packageId,
            print pickExpressByPackageId(packageId)
        print "Done."

if __name__ == "__main__":
    t = MyTester(50)
    # t.test()
    # address = ["重庆市","沙坪坝区","曾家镇","不详"]
    # address = ["浙江省","杭州市","余杭区","良渚镇","良诸镇七贤桥村东庄水产自然村20 组(送货时间不限)"]
    # address = ["陕西省","西安市","未央区","乡镇/街道","梨园路紫云溪小区6栋806"]
    # address = ["贵州省","遵义市","红花岗区","忠庄黔贵未来小区"]
    # address = ["湖北省","黄冈市","英山县","温泉镇"]
    # address = ["青海省","海西蒙古族藏族自治州","格尔木市","河西街道","盐桥北路三十四号"]
    # address = ["河南省","商丘市","虞城县","乡镇/街道","河南省虞城县人民路广播电视局"]
    # ret = t.testAddress(address)
    # for i in ret:
    #     print i,len(i), " | ",
    # print "宅急送" in ret
    # print t.testZJSAddress(address)

