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



