#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding:utf-8

from models import *
from tornado.web import RequestHandler
import datetime
from utility.error_code import *
from utility.utils import BasicTemplateHandler,countTime,AsyncHandler,MyDefineError
import time
from utility.checkfile import isImageFileType
import utility.utils as UTILS
import base64
import time
import tornado
import json
import hashlib
import time

class TestUploadHandler(AsyncHandler):

    '''测试图片上传'''

    ##@staff_member()
    def get(self):
        self.render("qiniu/test_upload.html")

    ##@staff_member()
    @gen.coroutine
    def post(self):
        if self.request.files:
            f = self.request.files.get("image")
            f = f[0]
            # print f
            today = str(datetime.date.today())
            fn = f["filename"].encode("utf-8")
            filename = self.get_argument("filename","")
            if not filename:
                filename = 'test/%s/%s' % (today, fn)
            # filename = "xiaoher.ipa"
            try:
                deleteFileObj(filename)
            except:
                pass
            url = yield asyncUploadImage(filename, f["body"])
            if url:
                self.redirect(url)
            else:
                self.write("upload error")


class UploadHandler(BasicTemplateHandler):

    ''' 图片上传接口 '''

    ##@staff_member()
    def post(self):
        return self._post()

    # @countTime
    def DBAction(self, Arguments):
        # print self.request.files
        if self.request.files:
            f = self.request.files.get("file")
            f = f[0]
            if not isImageFileType(f["body"]):
                raise Exception("not pic filetype")
            fn = f["filename"].encode("utf-8")
            timestamp = int(time.time())
            filename = "image/%s.jpg"%str(uuid.uuid1())
            url = uploadImage(filename, f["body"])
            self.write({"status": RET_OK, "url": url})

        elif self.get_argument("file",""):
            f  = self.get_argument("file")
            f = f.replace(" ","+")
            body = base64.b64decode(f)
            filename = "image/%s.jpg"%str(uuid.uuid1())
            url = uploadImage(filename, body)
            self.write({"status": RET_OK, "url": url})
        else:
            raise Exception("file not exist")

class DeleteHandler(BasicTemplateHandler):
    '''
    图片删除接口
    '''
    def getArgument(self):
        url = self.get_argument("url")
        return {"url":url}

    def DBAction(self,Arguments):
        url = Arguments["url"]
        # deleteFileObj(url)
        self.write({"status":RET_OK})


    ##@staff_member()
    def post(self):
        return self._post()

class GoodsImageUpload(BasicTemplateHandler):
    ##@staff_member()
    def post(self):
        return self._post()

    def DBAction(self, Arguments):
        if not self.request.files:
            raise Exception("file not exist")
        try:
            activityID = self.get_argument("activity_id","").split("?")[0]
            type = self.get_argument("upload_type","")
        except:
            raise MyDefineError("上传组件出错，请联系Yejin@xiaoher.com")

        print "In muti upload :",activityID,type
        f = self.request.files.get("file")
        f = f[0]
        fn = f["filename"]
        filename = "image/%s"%str(uuid.uuid1())

        if not activityID or activityID == "0":
            # muti-upload for old version
            try:
                goods_id = int(fn.split(".")[0].split("_")[0])
            except:
                raise MyDefineError("文件命名不规范")
            # print goods_id
            # print "[OLD VERSION ]goods_id is : {}".format(goods_id)
            url = uploadImage(filename, f["body"])
            conn = getMongoDBConn()
            db = conn.shop
            db.goods.update({"_id":goods_id},{"$push":{"image":url}})
            self.write({"status": RET_OK, "url": url})

        else:
            #muti-load for new-activities-page
            try:
                goods_id = int(fn.split(".")[0].split("_")[0])
            except:
                print "Failed  name"
                self.write({"status":"999", "msg": "文件命名不规范,请按照: （商品ID_数字）的格式命名图片"})
                return
            # print "goods_id is : {}".format(goods_id)
            conn = getMongoDBConn()
            db = conn.shop
            # goods = db.activity.find_one({"activity_id":activityID})
            # ret = db.activity_goods.find_one({"goods_id":goods_id,"activity_id":activityID})
            # if not ret:
            #     msg = "id:{}的图片不属于本活动{}".format(goods_id,activityID)
            #     print msg
            #     self.write({"status":"999", "msg": msg})
            #     return

            # 保存图片到骑牛
            url = uploadImage(filename, f["body"])
            # db.goods.update({"_id":goods_id},{"$push":{"image":url}})
            query = {"_id":goods_id}
            update = {"$push":{"image":url}}
            asyncUpdateGoodsAttrBYQuery(query,update)
            self.write({"status":0 , "msg":"OK"})


class TestsaveasHandler(AsyncHandler):
    #@staff_member()
    @tornado.gen.coroutine
    def get(self):
        filename = "test_test"
        url = self.get_argument("url")
        result = yield b.asyncsaveas(url,filename)
        # print result
        self.write(result)


class GenUploadToken(BasicTemplateHandler):

    #@staff_member()
    @tornado.gen.coroutine
    def get(self):
        self._post()

    #@staff_member()
    @tornado.gen.coroutine
    def post(self):
        self._post()


    def DBAction(self,Arguments):
        bucket = self.get_argument("bucket")
        token = cow.generate_upload_token(bucket)
        self.write({"status":RET_OK,"token":token})


class uploadClientImageInfoHandler(BasicTemplateHandler):
    def post(self, *args, **kwargs):
        self._post()

    def DBAction(self, Arguments):
        data = self.get_argument("data","")
        if not data:
            self.write({"status":90991,"msg":"No data posted"})
            return

        try:
            data = json.loads(data)
            nonce = data['nonce']
            timestamp = int(data['timestamp'])
            _hash = data['hash']
            image_id = data['image_id']
            width = int(data['width'])
            height = int(data['height'])
            filesize = int(data['filesize'])
            deltaTime = time.time() - timestamp
            print deltaTime
            if deltaTime > 1200:
                self.write({"status":90994,"msg":"Data is duplicated!"})
                return

            TOKEN = "x1i2a3o4h5e6r"
            tmpString = "{}{}{}".format(timestamp,nonce,TOKEN)
            md5Obj = hashlib.md5()
            md5Obj.update(tmpString)
            __hash = md5Obj.hexdigest().lower()[:20]
            if _hash != __hash:
                self.write({"status":90993, "msg":"Token is failed!"})
                return

            imgInfo = {
                "exif": {},
                "width": width,
                "height": height,
                "image_id": image_id,
                "goods_id": "-1",
                "activity_id": "-1",
                "filesize": filesize,
            }
            mongoConn = UTILS.getMongoDBConn()
            db = mongoConn.shop
            db.image_upload_detail.insert(imgInfo)
            self.write({"status":0, "msg": "OK"})


        except Exception,e:
            print e
            self.write({"status":90992,"msg":"Data format is invalid"})
            return


