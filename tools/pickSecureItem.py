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

    def checkIfGoodsIdIsSecure(self, goodsId):
        #first query in online/offline time of items
        self.db.dbName = "backend_log_db"
        sql = "select start_time,end_time,activity_id from goods_time_log where goods_id ='{}' and is_xinshou='{}' order by id desc limit 1".format(
            goodsId, 1)

        data = self.db.execQueryAssoc(sql)
        if not data:
            print "goods_id {} is not found in online/offline table".format(goodsId)
            return False # handle as insecure goods_id

        data = data[0]
        s_time = data['start_time']
        e_time = data['end_time']

        now = datetime.datetime.now()

        if abs(now - s_time) < self.secure_windows:
            return False

        if abs(e_time - now) < self.secure_windows:
            return False

    def fetchGoodsIds(self,amount=3000):
        ret = []
        offset = 0
        limit = amount
        goodsIds = self.pickGoodsIdFromStorage()
        print goodsIds
        while len(goodsIds) > 0 and len(ret) < amount:
            for goods in goodsIds:
                if self.checkIfGoodsIdIsSecure(goods['goods_id']):
                    t = (goods['goods_id'], goods['size'])
                    ret.append(t)
            offset = offset + limit
            goodsIds = self.pickGoodsIdFromStorage(offset=offset,limit=limit)
        return ret

if __name__ == "__main__":
    STP = StorageTestingItemPicker()
    ret = STP.fetchGoodsIds()



