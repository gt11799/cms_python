#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding:utf-8

import os,sys
reload(sys)
sys.setdefaultencoding("utf8")

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))


import tempfile
import utility as UTILITY
from qiniusdk import Cow, CowException
from settings import AK, SK, QINIU_IMAGE_BUCKET
import logging
import uuid
import time
import json
from tools.parse_image import ImagePaser
from urllib2 import urlopen
from tornado import gen

cow = Cow(AK, SK)
b = cow.get_bucket(QINIU_IMAGE_BUCKET)
HOST = "http://%s.qiniudn.com/" % QINIU_IMAGE_BUCKET

try:
    from settings import IMAGE_DOMAIN
except:
    IMAGE_DOMAIN = "qiniudn.com"

def replaceQiniuImage(image):
    if IMAGE_DOMAIN == "qiniudn.com":
        return image
    if IMAGE_DOMAIN == "qbox.me":
        if image.startswith("http://you1hui.qiniudn.com"):
            image = image.replace("you1hui.qiniudn.com","dn-you1hui.qbox.me")
        elif image.startswith("http://you1huitest.qiniudn.com"):
            image = image.replace("you1huitest.qiniudn.com","dn-you1huitest.qbox.me")
        else:
            pass
    if IMAGE_DOMAIN == "aliyuncs.com":
        if image.startswith("http://you1hui.qiniudn.com"):
            image = image.replace("you1hui.qiniudn.com","you1hui.oss-cn-hangzhou.aliyuncs.com")
        elif image.startswith("http://you1huitest.qiniudn.com"):
            image = image.replace("you1huitest.qiniudn.com","you1huitest.oss-cn-hangzhou.aliyuncs.com")
        else:
            pass

    return image

def countTime(func):
    def temp(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logStr =  "%s spend %s" % (func.__name__, end - start)
        logging.error(logStr)
        return result
    return temp

@countTime
def uploadImage(filename, content):
    '''直接传递文件内容的形式上传'''
    # raise Exception("it not work")
    level, temp = tempfile.mkstemp()
    with open(temp, "wb") as f:
        f.write(content)
    try:
        p = ImagePaser(temp)
        p.parseExif()
        p.parseSize()
        # p.showInfo()
        # for k,v in p.exif.items():
        #     print k,"   ",v
        if p.exif != {}:
            exif = json.dumps(p.exif)
        else:
            exif = ""
        imgInfo = {
            "exif": exif,
            "width": p.width,
            "height": p.height,
            "image_id": filename,
            "goods_id": "-1",
            "activity_id": "-1",
            "filesize" : len(content)
        }
        # for k,v in imgInfo.items():
        #     print k,":",v
        #
        # print "-"*100
        mongoConn = UTILITY.utils.getMongoDBConn()
        db = mongoConn.shop
        # for k,v in imgInfo.items():
        #     print k, " : ", v
        db.image_upload_detail.insert(imgInfo)
        t = b.put(temp, names={temp: filename})
        os.remove(temp)
        return "%s%s" % (HOST, t["key"])

    except CowException as e:
        # print e.url         # 出错的url
        # print e.status_code  # 返回码
        # print e.reason      # http error的原因
        # print e.content     # api 错误的原因
        logging.error(e.url)
        logging.error(e.reason)
        logging.error(e.content)
        logging.error(e.status_code)
        os.remove(temp)
        raise Exception("图片上传出错")
        return False

@gen.coroutine
def asyncUploadImage(filename,content):
    try:
        t = yield b.asyncPut(filename,content)
        t = json.loads(t)
        raise gen.Return("%s%s" % (HOST, t["key"]))
    except Exception as e:
        import traceback
        print traceback.format_exc()
        logging.error(e)
        raise Exception("图片上传出错")


def changeFileName(oldFilename, newFilename):
    oldFilename = oldFilename.encode("utf-8")
    newFilename = newFilename.encode("utf-8")
    print oldFilename,newFilename
    b.copy(oldFilename, newFilename)
    # b.delete(oldFilename)
    # b.move(oldFilename, newFilename)
    return "%s%s" % (HOST, newFilename)


def uploadImageByStream(filepath, filename):
    '''数据流方式上传'''
    raise Exception("it not work")


def getFileNameFromUrl(url):
    fileName = url.replace(HOST, "")
    return fileName

def deleteFileObj(url):
    return
    filename = getFileNameFromUrl(url)
    filename = filename.encode("utf-8")
    b.delete(filename)


def deleteTempFile(urls):
    return
    for url in urls:
        filename = getFileNameFromUrl(url)
        filename = filename.encode("utf-8")
        if filename.startswith("tmp"):
            try:
                b.delete(filename)
            except:
                pass



def getDefineSizeImage(url,mode=2,w=0,h=0):
    '''
    获取指定大小图片的URL
    '''
    if w == 0 and h ==0 :
        return url
    p = "?imageView/%s"%mode

    if w:
        p += "/w/%s"%w
    if h:
        p += "/h/%s"%h
    return "%s%s"%(url,p)


def cropImage(w,h,x,y,url,newFilename):
    from utility.utils import MyDefineError
    '''
    "http://you1hui.qiniudn.com/home_fuli.jpg?imageMogr/v2/crop/!600x300a0a0"
    '''
    if "imageView" in url:
        raise MyDefineError("目前必须原图裁剪")

    arg = "imageMogr/v2/crop/!%sx%sa%sa%s/thumbnail/!1000x1200"%(w,h,x,y)
    url =  "%s?%s"%(url,arg)
    t = b.saveas(url,newFilename)
    t = json.loads(t)
    return "%s%s" % (HOST, t["key"])

from tornado import gen

@gen.coroutine
def asyncCronImage(w,h,x,y,url,newFilename,thumb_w = 1000,thumb_h = 1200):
    from utility.utils import MyDefineError
    '''
    http://you1hui.qiniudn.com/home_fuli.jpg?imageMogr/v2/crop/!600x300a0a0"
    '''
    if "imageView" in url:
        raise MyDefineError("目前必须原图裁剪")
    if thumb_h:
        arg = "imageMogr/v2/crop/!%sx%sa%sa%s/thumbnail/!%sx%s"%(w,h,x,y,thumb_w,thumb_h)
    else:
        arg = "imageMogr/v2/crop/!%sx%sa%sa%s/thumbnail/!%s"%(w,h,x,y,thumb_w)

    mongoConn = UTILITY.utils.getMongoDBConn(async=True)
    db = mongoConn.shop
    imgInfo = {
            "exif": {},
            "width": thumb_w,
            "height": thumb_h,
            "image_id": newFilename,
            "goods_id": "-1",
            "activity_id": "-1",
            "filesize" : -1
    }
    yield db.image_upload_detail.insert(imgInfo)
    url =  "%s?%s"%(url,arg)
    t = yield b.asyncsaveas(url,newFilename)
    t = json.loads(t)
    raise gen.Return("%s%s"% (HOST, t["key"]))

def getImgInfo(url=''):
    from utility.utils import getRedisObj
    from base64 import b64encode
    '''根据图片URL获取图片的图片格式、图片大小、色彩模型'''
    height = 0
    width = 0
    try:
        r = getRedisObj()
        height = r.get(b64encode(url))
        if not height:
            doc = urlopen(url +"?imageInfo")
            doc = doc.read()
            j = json.loads(doc)
            height = j["height"]
            width = j["width"]
            r.set(b64encode(url),height)
    except:
        pass
    print("height")
    print(height)
    return width,height
