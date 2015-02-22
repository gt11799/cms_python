#!coding:utf8
import os,sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

path = os.path.join( os.path.dirname( os.path.abspath(__file__)), "..")
sys.path.append(path)

from utility.utils import DBAccess

__author__ = 'David'

class StorageTestingItemPicker():
    def __init__(self):
        self.db = DBAccess()
        self.secure_windows = datetime.timedelta(days=5)

    def pickGoodsIdFromStorage(self,limit=4000,offset = 0):
        self.db.dbName = "stock_log_db"
        sql = "select goods_id,count,size,update_time from stock_location_goods where count>0 order by update_time desc " \
              "limit {},{};".format(offset,limit)
        print sql
        items = self.db.execQueryAssoc(sql)
        return items



    def testIfExist(self, goodsId):
        pass

if __name__ == "__main__":
    STP = StorageTestingItemPicker()
    ret = STP.fetchGoodsIds()



