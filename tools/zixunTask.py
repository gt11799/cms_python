#! /usr/bin/env python
#! -*- coding=utf8 -*-
'''
本文件包含了在写 资讯 网站的时候用到的一些工具，包括redis回到初始状态，和redis宕机了之后的恢复。
另外，每天凌晨需要执行一些定时任务，也放到了该脚本中。
author: 宫亭
mail: gongting@xiaoher.com
'''
import os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from zixun.models import getCatagoryInfo

db = DBAccess()
db.dbName = "zixun"
r = getRedisObj()

def resetRedis():
    '''
    删除redis已经存在的key
    '''

    r.delete("catagory_url_all")
    r.delete("tag_url_all")
    r.delete("catagory_name_id")
    r.delete("tag_name_id")
    r.delete("catagory_id_url")
    return

def recoverRedis():
    '''
    删除之后从数据库中恢复
    '''
    catagories = db.execQueryAssoc("select name,id,url,parent_id from catagory")
    for catagory in catagories:
        r.hset("catagory_name_id",catagory['name'],catagory['id'])
        r.sadd("catagory_url_all",catagory['url'])

        if int(catagory['parent_id']):
            url = getCatagoryInfo(name=catagory['name'])['url'] + '/' + url
        else:
            url = catagory['url']
        r.hset("catagory_id_url",catagory['id'],url)

    tags = db.execQueryAssoc("select name,id,click_time,url from tag")
    for tag in tags:
        r.hset("tag_name_id",tag['name'],tag['id'])
        r.sadd("tag_url_all",tag['url'])
        r.set("click_time_tag_%s"%tag['id'], tag['click_time'])
    return

def removeDiagonal():
    '''
    去掉文章的网页标题网页关键字中的斜线
    '''
    sql = "update article set meta_title=replace(meta_title, '/', ''), meta_keyword=replace(meta_keyword,'/','')"
    db.execNonQuery(sql)
    return



if __name__ == '__main__':
    resetRedis()
    recoverRedis()