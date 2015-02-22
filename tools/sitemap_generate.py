#! /usr/bin/env python
# -*- coding=utf8 -*-
'''
gongting@xiaoher.com
用来生成资讯的sitemap
'''
from io import BytesIO
import os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from utility.mail import send_mail

from zixun.models import getCatagoryCompleteUrl

def generateAllUrl():
    '''
    生成资讯所有的url
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    tagUrl = list(r.smembers("tag_url_all"))
    tagUrl = [ "label/" + _ for _ in tagUrl ]
    print tagUrl
    brandUrl = list(r.smembers("brand_url_all"))
    brandUrl = [ "pinpai/" + _ for _ in brandUrl ]
    print brandUrl

    catagoryId = r.hvals("catagory_name_id")
    catagoryIdAndUrl = {}
    for _id in catagoryId:
        try:
            catagoryIdAndUrl[int(_id)] = "zixun/" + getCatagoryCompleteUrl(_id)
        except:
            print _id
    catagoryUrl = catagoryIdAndUrl.values()

    articleInfo = db.execQueryAssoc("select id,catagory_id from article where delete_status=0 and if_display=1")
    ArticleUrl = []
    for article in articleInfo:
        try:
            ArticleUrl.append(catagoryIdAndUrl[ int(article['catagory_id']) ] +  '/' + str(article['id']))
        except(KeyError):
            print article['catagory_id']

    return ["zixun",] + tagUrl+ brandUrl + catagoryUrl + ArticleUrl

def generateSitemap(urls):
    '''
    生成网站地图
    '''
    sitemap = """<?xml version="1.0" encoding="UTF-8"?> \n"""
    sitemap += """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> \n"""
    for url in urls:
        sitemap += "<url>\n"
        sitemap += "    <loc>http://www.xiaoher.com/%s</loc>\n"%url
        sitemap += "    <changefreq>weekly</changefreq>\n"
        sitemap += "</url>\n"
    sitemap += "</urlset>"
    file_path = os.path.join(os.path.dirname(__file__), '../static/csv/Sitemap.xml')
    with open(file_path,'wb') as f:
        f.write(sitemap)
    return 


if __name__ == "__main__":

    urls = generateAllUrl()
    generateSitemap(urls)