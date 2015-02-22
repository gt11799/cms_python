#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utility.utils import *
import datetime,random
from xpinyin import Pinyin
from qiniu.models import replaceQiniuImage

NAVIGATE = ["服装品牌","服装设计","服装搭配","服装配饰","女士服装","儿童服装","儿童玩具"]
COLLOCATION_URL = "fzdp"

def addArticle(title,tag,catagory,cover_image,description,content,author,meta_title,meta_keyword,meta_description,if_display,brand):
    '''
    增加文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    if not (title and tag and catagory and cover_image and description and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')

    catagory_id = r.hget("catagory_name_id",catagory)
    if not catagory_id:
        raise MyDefineError('没有这个栏目')
    brand_id = r.hget("brand_name_id",brand)
    if not brand_id:
        brand_id = 0
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into article (title,catagory_id,cover_image,description,content,author,create_time,meta_title,meta_keyword,meta_description,update_time,if_display,brand_id) values ('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s)"\
    		%(title,catagory_id,cover_image,description,content,author,create_time,meta_title,meta_keyword,meta_description,create_time,if_display,brand_id)
    article_id = db.execNonQuery(sql)
    print article_id
    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = r.hget("tag_name_id",tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    r.set("click_time_article_%s"%article_id, 0)
    complete_url = getCatagoryCompleteUrl(catagory_id)
    recordFlow(author,"add","article",sql)
    return complete_url + '/' + str(article_id),article_id

def changeArticle(article_id,tag,title,catagory,cover_image,description,content,meta_title,meta_keyword,meta_description,author,if_display,brand):
    '''
    修改文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    if not (title and tag and catagory and cover_image and description and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')
    catagory_id = r.hget("catagory_name_id",catagory)
    if not catagory_id:
        raise MyDefineError('没有这个目录')
    brand_id = r.hget("brand_name_id",brand)
    if not brand_id:
        brand_id = 0

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update article set title='%s',catagory_id='%s',cover_image='%s',description='%s',content='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',if_display=%s,brand_id=%s where id=%s"\
                %(title,catagory_id,cover_image,description,content,meta_title,meta_keyword,meta_description,update_time,if_display,brand_id,article_id)
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)
    recordFlow(author,"modify","article",sql)

    sql = "delete from article_tag where article_id=%s"%article_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)

    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = r.hget("tag_name_id",tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    complete_url = getCatagoryCompleteUrl(catagory_id)
    return complete_url + '/' + str(article_id)

def changeArticleWithTag(status,article_id,tag_name):
    '''
    实时修改文章与标签的对应关系
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    tag_id = r.hget("tag_name_id",tag_name)
    if not tag_id:
        tag_id = addTag(tag_name)
    if status == "remove":
        sql = "delete from article_tag where article_id=%s and tag_id=%s "%(article_id,tag_id)
    elif status == "add":
        sql = "insert into article_tag (article_id,tag_id) values (%s,%s)"%(article_id,tag_id)
    else:
        raise MyDefineError("状态不对")
    db.execNonQuery(sql)
    return 

def addTag(parent_name,name,meta_title,meta_keyword,meta_description,author):
    '''
    增加标签,MySQL与Redis都要添加
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()
    p = Pinyin()

    if parent_name:
        parent_id = r.hget("tag_name_id",parent_name)
        if not parent_id:
            raise MyDefineError("一级标签不存在")
    else:
        parent_id = 0

    if name in r.hkeys("tag_name_id"):
        raise MyDefineError("标签已存在")

    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    while url in r.smembers("tag_url_all"):
        url += str(random.randint(0,30))

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into tag (name,url,update_time,parent_id,meta_title,meta_keyword,meta_description) values ('%s','%s','%s',%s,'%s','%s','%s')"\
            %(name,url,update_time,parent_id,meta_title,meta_keyword,meta_description)
    tag_id = db.execNonQuery(sql)
    r.hset("tag_name_id",name,tag_id)
    r.sadd("tag_url_all",url)
    r.set("click_time_tag_%s"%tag_id, 0)
    recordFlow(author,"add","tag",sql)
    return tag_id

def addTagsAndArticle(article_id,tag_names):
    '''
    增加文章与多个标签的对应关系
    如果标签不存在，会添加标签
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    tag_names_exists = r.hkeys("tag_name_id")
    tag_ids = []
    for tag_name in tag_names:
        if tag_name not in tag_names_exists:
            tag_ids.append(addTag(tag_name))
        else:
            tag_ids.append(r.hget("tag_name_id",tag_name))
    for tag_id in tag_ids:
        addTagAndArticle(article_id,tag_id)

def addTagAndArticle(article_id,tag_id):
    '''
    增加文章与标签的对应关系，需要保证文章与标签都存在
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "insert into article_tag (article_id,tag_id) values (%s,%s)" %(article_id,tag_id)
    return db.execNonQuery(sql)

def getArticleByID(article_id,catagory='',tag_url='',brand_url='',page=-1):
    '''
    根据文章id取出文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    page = 1 if page < 1 else page
    sql = "select * from article where id = %s "%article_id

    if catagory:
        catagory_id = r.hget("catagory_name_id",catagory)
        sql += " and catagory_id=%s" %catagory_id
    if tag_url:
        sql += " and id in (select article_id from article_tag where tag_id in (select id from tag where url = '%s'))"%tag_url
    if brand_url:
        sql += " and brand_id in (select id from brand where url = '%s')"%brand_url
    try:
        article = db.execQueryAssoc(sql)[0]
    except(IndexError):
        return []
    article['tag'] = getTagInfoByArticle(article_id)
    pageCount,article['content'] = articleContentHandle(article['content'],page)
    r.incr("click_time_article_%s"%article_id)
    article['catagory_name'] = getCatagoryNameWithID(article['catagory_id'])
    return pageCount,article

def getArticleByIDForBacker(article_id):
    '''
    根据文章id取出文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select * from article where delete_status=0 and id = %s"%article_id

    try:
        article = db.execQueryAssoc(sql)[0]
    except(IndexError):
        return []
    try:
        article["brand_name"] = getBrandByID(article['brand_id']).get('name')
    except(IndexError):
        article['brand_name'] = ''
    article['tag'] = getTagInfoByArticle(article_id)
    article['catagory_name'] = getCatagoryNameWithID(article['catagory_id'])
    return article

def getArticleByTag(tag_url,page=-1):
    '''
    根据标签返回文章列表和文章导读
    '''

    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    pageNum = 10
    page = 1 if page < 1 else page
    start = pageNum * (page - 1)
    tag_info = db.execQueryAssoc("select id,parent_id from tag where url='%s'"%tag_url)
    if tag_info[0]['parent_id'] == 0:
        tag_info = db.execQueryAssoc("select id from tag where parent_id=%s"%tag_info[0]['id'])
    tag_ids = tuple([ int(_['id']) for _ in tag_info ])
    page_p = " limit %s,%s"%(start,pageNum)
    if len(tag_ids) > 1:
        query = " where delete_status=0 and if_display=1 and id in (select article_id from article_tag where tag_id in %s) and catagory_id !=0 "%(tag_ids,)
    else:
        query = " where delete_status=0 and if_display=1 and id in (select article_id from article_tag where tag_id = %s) and catagory_id !=0 "%tag_ids[0]
    sql = "select id,title,cover_image,description,create_time,catagory_id,meta_description from article %s order by update_time desc %s "%(query,page_p)
    print sql
    articles = db.execQueryAssoc(sql)
    for article in articles:
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(article['id'])
        article['tag'] = db.execQueryAssoc(sql)
        article['complete_url'] = getCatagoryCompleteUrl(article['catagory_id'])
    recordNum = db.execQuery('select count(id) from article %s'%query)[0][0]
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,articles

def getArticles(catagory_name='',start_time='',end_time='',title='',description='',author='',
                            meta_title='',meta_keyword='',meta_description='',if_display='',page=-1,sort=''):
    '''
    后台 编辑文章列表显示
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    page = 1 if page < 1 else page
    pageNum = 30
    start = pageNum * (page - 1)
    page_p = " limit %s,%s "%(start,pageNum)

    sql = "select id,catagory_id,title,description,cover_image,author,create_time,meta_title,meta_keyword,meta_description,if_display,update_time,click_time,brand_id from article"

    query = " where delete_status=0 "
    if catagory_name:
        catagory_id = r.hget("catagory_name_id",catagory_name)
        query += " and catagory_id = %s" %catagory_id
    if start_time:
        query += " and create_time > '%s' " %start_time
    if end_time:
        query += " and create_time < '%s' "%end_time
    if title:
        title = title.replace(' ','.*')
        query += " and title regexp '%s' " %title
    if description:
        description = description.replace(' ','.*')
        query += " and description regexp '%s' "%description
    if author:
        query += " and author = '%s' "%author
    if meta_title:
        meta_title = meta_title.replace(' ','.*')
        query += " and meta_title regexp '%s' "%meta_title
    if meta_keyword:
        meta_keyword = meta_keyword.replace(' ','.*')
        query += " and meta_keyword regexp '%s' "%meta_keyword
    if meta_description:
        meta_description = meta_description.replace(' ','.*')
        query += " and meta_description regexp '%s' "%meta_description
    if if_display != '':
        query += " and if_display = %s "%if_display

    if sort == 'click':
        order = " order by click_time desc "
    else:
        order = " order by create_time desc "
    sql = "%s %s %s %s" %(sql,query,order,page_p)
    print sql
    result = db.execQueryAssoc(sql)

    for r in result:
        r['tags'] = getTagByArticle(r['id'])
        if int(r['catagory_id']):
            r['catagory_name'] = getCatagoryByID(r['catagory_id'])
            r['complete_url'] = getCatagoryCompleteUrl(r['catagory_id'])
        else:
            r['catagory_name'] = ''
            r['complete_url'] = ''
        if int(r['brand_id']):
            r['brand_name'] = getBrandByID(r['brand_id'])['name']
        else:
            r['brand_name'] = ''

    sql = "select count(id) from article %s" %query
    recordNum = db.execQueryAssoc(sql)[0]['count(id)']
    print recordNum
    PageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,PageCount,result

def deleteArticle(article_id,author):
    '''
    删除文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    article_info = db.execQueryAssoc("select catagory_id,title from article where id = %s"%article_id)[0]
    sql = "delete from article_tag where article_id = %s"%article_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update article set delete_status=1,update_time='%s' where id = %s"%(update_time,article_id)
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)

    r.delete("click_time_article_%s"%article_id)
    recordFlow(author,"delete","article",sql)
    return


def getTagByArticle(article_id):
    '''
    取出文章的所有标签
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %article_id
    tags = db.execQueryAssoc(sql)
    return tags

def getFirstLevelTag(tag_name):
    '''
    取出一级标签
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name from tag where id in (select parent_id from tag where name = '%s')" %tag_name
    try:
        tag = db.execQueryAssoc(sql)[0]['name']
    except(IndexError):
        tag = ''
    return tag

def getTagInfoByArticle(article_id):
    '''
    根据article_id获取文章的所有标签
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(article_id)
    return db.execQueryAssoc(sql)

def getTagByID(tag_id):
    '''
    通过id获取标签页面信息
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select * from tag where id = %s"%tag_id
    tag_info = db.execQueryAssoc(sql)
    if tag_info:
        return tag_info[0]
    else:
        return {}

def getTagInfo(url):
    '''
    返回tag的详细信息
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select * from tag where url = '%s' "%url
    tag_info = db.execQueryAssoc(sql)[0]
    r.incr("click_time_tag_%s"%tag_info["id"])
    return tag_info

def deleteTag(tag_id,author):
    '''
    删除标签，tag表，article_tag表，以及Redis都要删除
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    son_tag = db.execQueryAssoc("select id from tag where parent_id=%s"%tag_id)
    if son_tag:
        raise MyDefineError("有子标签不能删除")
    tag_info = db.execQueryAssoc('select url,name from tag where id = %s'%tag_id)[0]
    sql = "delete from article_tag where tag_id = %s" %tag_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)
    sql = "delete from tag where id = %s" %tag_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","tag",sql)

    r.hdel("tag_name_id",tag_info['name'])
    r.srem("tag_url_all",tag_info['url'])
    r.delete("click_time_tag_%s"%tag_id)
    db.execNonQuery("delete from hot_tag where tag_id = %s"%tag_id)
    return

def getTags(name='',meta_title='',meta_keyword='',meta_description='',start_time='',end_time='',sort='',page=-1,parent_tag=''):
    '''
    编辑：获得所有标签列表
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    page = 1 if page < 0 else page
    pageNum = 30
    start = pageNum * (page - 1)
    page_p = " limit %s,%s"%(start, pageNum)

    sql = "select * from tag "
    query = " where  1=1 "
    if name:
        name = name.replace(" ",'.*')
        query += " and name regexp '%s' "%name
    if meta_title:
        meta_title = meta_title.replace(' ','.*')
        query += " and meta_title regexp '%s' "%meta_title
    if meta_keyword:
        meta_keyword = meta_keyword.replace(' ', '.*')
        query += " and meta_keyword regexp '%s' "%meta_keyword
    if meta_description:
        meta_description = meta_description.replace(' ','.*')
        query += " and meta_description regexp '%s' "%meta_description
    if start_time:
        query += " and update_time > '%s' "%start_time
    if end_time:
        query += " and update_time < '%s' "%end_time
    if parent_tag:
        parent_id = r.hget("tag_name_id",parent_tag)
        if parent_id:
            query += " and parent_id = %s "%parent_id
    if sort == 'click':
        order = " order by click_time desc"
    else:
        order = " order by update_time desc"
    sql = "%s %s %s %s" %(sql,query,order,page_p)
    result = db.execQueryAssoc(sql)

    for r in result:
        r['parent_name'] = getTagByID(r['parent_id']).get('name','')

    sql = "select count(id) from tag %s"%query
    recordNum = db.execQueryAssoc(sql)[0]['count(id)']
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,result


def changeTag(tag_id,name,parent_name,meta_title,meta_keyword,meta_description,author):
    '''
    改变标签详情
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()


    sql = "select name,url from tag where id=%s" %tag_id
    tag_info = db.execQueryAssoc(sql)[0]
    if name != tag_info['name']:
        if name in r.hkeys("tag_name_id"):
            raise MyDefineError("标签已存在")

    if parent_name:
        parent_id = r.hget("tag_name_id",parent_name)
        if not parent_id:
            raise MyDefineError("一级标签不存在")
    else:
        parent_id = 0

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update tag set name='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',parent_id=%s where id=%s"\
        %(name,meta_title,meta_keyword,meta_description,update_time,parent_id,tag_id)
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"modify","tag",sql)

    if name != tag_info['name']:
        r.hdel("tag_name_id",tag_info['name'])
        r.hset("tag_name_id",name,tag_id)
    return

def getAllTags():
    '''
    以多层字典的方式返回所有的标签的名称
    只支持两级
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select id,name from tag where parent_id = 0"
    first_levels = db.execQueryAssoc(sql)
    result = {}
    for first_level in first_levels:
        sql = "select name from tag where parent_id = %s" %first_level['id']
        second_level = db.execQueryAssoc(sql)
        result[first_level['name']] = [ _['name'] for _ in second_level]
    return result

def getFirstLevelTags():
    '''
    返回一级标签
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select id,name from tag where parent_id = 0"
    first_levels = db.execQueryAssoc(sql)
    result = {}
    for tag in first_levels:
        result[tag['id']] = tag['name']
    return result

def getSecondLevelTagByName(tag_name):
    '''
    根据一级标签的ID，返回二级标签
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name from tag where parent_id in (select id from tag where name = '%s')"%tag_name
    second_levels = db.execQueryAssoc(sql)
    result = [ _['name'] for _ in second_levels]
    return result

def getAllCatagory():
    '''
    以多层字典的方式返回所有的目录的名称
    只支持两级目录
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select id,name from catagory where parent_id = 0 and delete_status=0"
    first_levels = db.execQueryAssoc(sql)
    result = {}
    for first_level in first_levels:
        sql = "select name from catagory where parent_id = %s and delete_status=0" %first_level['id']
        second_level = db.execQueryAssoc(sql)
        result[first_level['name']] = [_['name'] for _ in second_level]
        print result[first_level['name']]
    return result

def getCollocationCatagory():
    '''
    以列表的方式返回搭配的目录的名称
    只支持两级目录
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    result = []
    parent_id = r.hget("catagory_name_id","服装搭配")
    result.append("服装搭配")
    sql = "select name from catagory where parent_id = %s and delete_status=0" %parent_id
    second_level = db.execQueryAssoc(sql)
    print second_level
    result.append([_['name'] for _ in second_level])
    print result
    return result

def getCatagories():
    '''
    获得全部目录字典
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select * from catagory where delete_status = 0"
    result = db.execQueryAssoc(sql)
    catagories = {}
    for item in result:
        hot_tag = getHotTags(catagory_id=item['id'])
        item['hot_tag'] = [ _[0] for _ in hot_tag]
        hot_brand = getHotBrands(catagory_id=item['id'])
        item['hot_brand'] = [ _[0] for _ in hot_brand]
        catagories[item['name']] = item
    return catagories

def getCatagoryByID(catagory_id):
    '''
    通过目录ID获得目录名称
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name from catagory where id = %s and delete_status=0"%catagory_id
    return db.execQueryAssoc(sql)[0]['name']

def addCatagory(name,parent_name,meta_title,meta_keyword,meta_description,hot_tag,hot_brand,author,cover_image):
    '''
    增加一个目录，一级目录的parent_id=0
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()
    p = Pinyin()

    if not name:
        raise MyDefineError("名称不能为空")
    if name in r.hkeys("catagory_name_id"):
        raise MyDefineError("栏目已存在")
    if parent_name:
        parent_id = r.hget("catagory_name_id",parent_name)
        if not parent_id:
            raise MyDefineError("父栏目不存在")
    else:
        parent_id = 0
    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    while url in r.smembers("catagory_url_all"):
        url += str(random.randint(0,30))

    sql = "insert into catagory (name, parent_id,url, meta_title,meta_keyword,meta_description,cover_image) values ('%s','%s','%s','%s','%s','%s','%s')" \
            %(name,parent_id,url,meta_title,meta_keyword,meta_description,cover_image)
    catagory_id = db.execNonQuery(sql)
    r.hset("catagory_name_id",name,catagory_id)
    r.sadd("catagory_url_all",url)
    if hot_tag:
        updateHotTag(catagory_id,hot_tag)
    if hot_brand:
        updateHotBrand(catagory_id,hot_brand)
    recordFlow(author,"add","catagory",sql)
    return 

def getCatagoryCompleteUrl(catagory_id):
    '''
    返回一个目录的完整url，比如一个二级目录：fz/ppzx
    一级目录：fz
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select url,parent_id from catagory where id = %s and delete_status=0" %catagory_id
    catagory_info = db.execQueryAssoc(sql)[0]
    if int(catagory_info['parent_id']):
        sql = "select url from catagory where id = %s and delete_status=0" %catagory_info['parent_id']
        parent_url = db.execQueryAssoc(sql)[0]['url']
        complete_url = parent_url + '/' + catagory_info['url']
    else:
        complete_url = catagory_info['url']
    return complete_url

def changeCatagory(catagory_id,name,parent_name,meta_title,meta_keyword,meta_description,hot_tag,hot_brand,author,cover_image):
    '''
    改变目录详情
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select name,parent_id from catagory where id=%s" %catagory_id
    old_info = db.execQueryAssoc(sql)[0]

    if name != old_info['name']:
        #if old_info['parent_id'] == 0:
            #raise MyDefineError("一级目录不允许改变")
        if name in r.hkeys("catagory_name_id"):
            raise MyDefineError("栏目已存在")

    if parent_name:
        parent_id = r.hget("catagory_name_id",parent_name)
        if not parent_id:
            raise MyDefineError("父目录不存在")
    else:
        parent_id = 0
    if hot_tag:
        updateHotTag(catagory_id,hot_tag)
    if hot_brand:
        updateHotBrand(catagory_id,hot_brand)
    sql = "update catagory set name='%s',parent_id='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',cover_image='%s' where id = %s" \
            %(name,parent_id,meta_title,meta_keyword,meta_description,cover_image,catagory_id)
    print sql
    recordFlow(author,"modify","catagory",sql)
    db.execUpdate(sql)

    if name != old_info['name']:
        r.hdel("catagory_name_id",old_info['name'])
        r.hset("catagory_name_id",name,catagory_id)
    return

def getCatagoryInfo(url='',name=''):
    '''
    获取目录页面详情
    '''
    db = DBAccess()
    db.dbName = "zixun"
    if url:
        sql = "select * from catagory where url = '%s' "%url
    if name:
        sql = "select * from catagory where name = '%s' "%name
    sql += " and delete_status=0 "
    try:
        cata_info = db.execQueryAssoc(sql)[0]
    except(IndexError):
        return []
    cata_info['parent_name'] = getCatagoryNameWithID(cata_info['parent_id'])
    cover_image = cata_info['cover_image']
    cata_info['cover_image'] = []
    if cover_image:
        for image in cover_image.split(','):
            image = image.split('&')
            if len(image) == 2:
                cata_info['cover_image'].append(image)
    return cata_info

def getCatagoryFirstLevelURL():
    '''
    获得一级目录的url
    '''
    db = DBAccess()
    db.dbName = "zixun"
    
    sql = "select url from catagory where delete_status=0 and parent_id=0"
    result = db.execQuery(sql)
    result = [ _[0] for _ in result]
    return result

def getArticlesByCatagory(url='',name='',page=-1):
    '''
    获取该目录下的所有文章列表和文章导读
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    pageNum = 10
    page = 1 if page < 1 else page
    start = pageNum * (page - 1)
    page_p = " limit %s,%s"%(start,pageNum)

    if url:
        query = " where catagory_id = (select id from catagory where url = '%s' and delete_status=0)"%url
    if name:
        query = " where catagory_id = (select id from catagory where name = '%s' and delete_status=0)"%name
    query += " and delete_status=0 and if_display = 1 "
    sql = "select id,title,cover_image,description,create_time from article %s order by update_time desc %s" %(query,page_p)
    articles = db.execQueryAssoc(sql)
    for article in articles:
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(article['id'])
        article['tag'] = db.execQueryAssoc(sql)

    recordNum = db.execQuery("select count(id) from article %s"%query)[0][0]
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,articles

def getArticleWithCatagory(url='',article_id='',page=-1):
    '''
    获取该目录下的指定文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    page = 1 if page < 1 else page
    sql = "select id from catagory where url = '%s' and delete_status=0"%url
    catagory_id = db.execQueryAssoc(sql)[0]['id']
    sql = "select * from article where id = %s and catagory_id = %s and delete_status=0 and if_display=1" %(article_id,catagory_id)
    try:
        article = db.execQueryAssoc(sql)[0]
    except(IndexError):
        return 0,{}
    article['content'], pageCount = articleContentHandle(article['content'],page)
    article['tag'] = getTagInfoByArticle(article_id)
    r.incr("click_time_article_%s"%article_id)
    return pageCount,article



def articleContentHandle(content,page):
    '''
    文章内容的处理，分页
    '''
    content = content.split("_ueditor_page_break_tag_")
    pageCount = len(content)
    page = pageCount if page > pageCount else page
    content = content[page-1]
    return content,pageCount

def collocationArticleContentHanlde(content):
    '''
    搭配栏目文章内容的处理
    '''
    result = []
    for image_info in content.split(','):
        temp = image_info.split('&')
        if len(temp) >= 2:
            result.append(temp)
    return result


def catagoryBelongTo(child_url, parent_url):
    '''
    判断子目录与父目录是否是从属关系
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    if child_url not in r.smembers("catagory_url_all") or parent_url not in r.smembers("catagory_url_all"):
        return False
    child_id = db.execQueryAssoc("select parent_id from catagory where url = '%s' and delete_status=0" %child_url)[0]['parent_id']
    parent_id = db.execQueryAssoc("select id from catagory where url = '%s' and delete_status=0 "%parent_url)[0]['id']
    print child_id,parent_id
    return child_id == parent_id

def getCatagoryNameWithID(catagory_id):

    db = DBAccess()
    db.dbName = "zixun"
    if catagory_id == 0:
        return
    sql = "select name from catagory where id = %s" %catagory_id
    return db.execQueryAssoc(sql)[0]['name']
    
def getCatagoryUrlWithID(catagory_id):

    db = DBAccess()
    db.dbName = "zixun"
    if catagory_id == 0:
        return
    sql = "select url from catagory where id = %s" %catagory_id
    return db.execQueryAssoc(sql)[0]['url']

def getLatestArticle(url='',catagory_id=0):
    '''
    6篇最新文章
    '''
    r = getRedisObj()
    if url:
        catagory_id = getCatagoryInfo(url=url)['id']
    article_info = r.lrange("latest_article_%s"%catagory_id,0,5)
    result = []
    for article in article_info:
        result.append(article.split('&'))
    return result

def getHotArticle(url='',catagory_id=0):
    '''
    最多会有20篇热门文章
    '''
    r = getRedisObj()
    if url:
        catagory_id = getCatagoryInfo(url=url)['id']
    article_info = r.lrange("hot_article_%s"%catagory_id,0,18)
    result = []
    for article in article_info:
        result.append(article.split('&'))
    return result

def getHotTags(url='',catagory_id=-1):
    '''
    最热标签
    '''
    r = getRedisObj()
    if catagory_id < 0:
        catagory_id = getCatagoryInfo(url=url)['id']
    tag_info = r.lrange("hot_tag_%s"%catagory_id,0,50)
    result = []
    for tag in tag_info:
        result.append(tag.split('&'))
    return result

def getHotBrands(url='',catagory_id=0):
    '''
    最热品牌
    '''
    r = getRedisObj()
    if catagory_id < 1:
        catagory_id = getCatagoryInfo(url=url)['id']
    brand_info = r.lrange("hot_brand_%s"%catagory_id,0,50)
    result = []
    for brand in brand_info:
        result.append(brand.split('&'))
    return result

def deleteCatagory(catagory_id,author):
    '''
    删除目录，目录下文章catagory_id设为0
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    son_catagory = db.execQueryAssoc("select id from catagory where parent_id=%s and delete_status=0"%catagory_id)
    if son_catagory:
        raise MyDefineError("有子栏目不能删除")

    complete_url = getCatagoryCompleteUrl(catagory_id)
    catagory_info = db.execQueryAssoc("select name,url from catagory where id = %s"%catagory_id)[0]
    sql = "update catagory set delete_status=1 where id = %s"%catagory_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","catagory",sql)
    db.execUpdate("update article set catagory_id=0 where catagory_id = %s"%catagory_id)

    r.srem("catagory_url_all",catagory_info['url'])
    r.hdel("catagory_name_id",catagory_info['name'])
    r.delete("latest_article_%s"%catagory_id)
    r.delete("hot_article_%s"%catagory_id)
    r.delete("hot_tag_%s"%catagory_id)
    r.delete("hot_brand_%s"%catagory_id)
    db.execNonQuery("delete from hot_tag where catagory_id=%s"%catagory_id)
    db.execNonQuery("delete from hot_brand where catagory_id=%s"%catagory_id)
    return

def addBrand(name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author):
    '''
    增加品牌
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()
    p = Pinyin()

    #if not (name and description and cover_image and description  and meta_title and meta_keyword and meta_description):
    #    raise MyDefineError('不能为空')
    if name in r.hkeys("brand_name_id"):
        raise MyDefineError("品牌已存在")

    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    while url in r.smembers("brand_url_all"):
        url += str(random.randint(0,30))

    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into brand (name,description,url,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author,create_time,update_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
            %(name,description,url,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author,create_time,create_time)
    brand_id = db.execNonQuery(sql)
    recordFlow(author,"add","brand",sql)

    r.sadd('brand_url_all',url)
    r.hset("brand_name_id",name,brand_id)
    r.set("click_time_brand_%s"%brand_id, 0)
    return brand_id

def getBrands(name='',start_time='',end_time='',description='',brand_classify='',company_name='',company_address='',author='',meta_title='',meta_keyword='',meta_description='',page=-1,sort=''):
    '''
    显示品牌列表
    '''
    db = DBAccess()
    db.dbName = "zixun"

    page = 1 if page < 0 else page
    pageNum = 30
    start = pageNum * (page - 1)
    page_p = " limit %s,%s"%(start, pageNum)

    sql = "select * from brand"
    query = " where delete_status=0 "
    if name:
        query += " and name regexp '%s'"%name
    if start_time:
        query += " and update_time > '%s'"%start_time
    if end_time:
        query += " and update_time < '%s'"%end_time
    if description:
        description = description.replace(' ','.*')
        query += " and description regexp '%s'"%description
    if brand_classify:
        query += " and brand_classify regexp '%s'"%brand_classify
    if company_name:
        query += " and company_name regexp '%s'"%company_name
    if company_address:
        company_address = company_address.replace(' ','.*')
        query += " and company_address regexp '%s'"%company_address
    if author:
        query += " and author = '%s'"%author
    if meta_title:
        query += " and meta_title regexp '%s'"%meta_title
    if meta_keyword:
        query += " and meta_keyword regexp '%s'"%meta_keyword
    if meta_description:
        query += " and meta_description regexp '%s'"%meta_description
    if sort == 'click':
        order = " order by click_time desc"
    else:
        order = " order by create_time desc "

    sql = "%s %s %s %s"%(sql,query,order,page_p)
    result = db.execQueryAssoc(sql)

    sql = "select count(id) from brand %s"%query
    recordNum = db.execQueryAssoc(sql)[0]['count(id)']
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,result

def deleteBrand(brand_id,author):
    '''
    删除品牌
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    brand_info = getBrandByID(brand_id)
    sql = "update article set brand_id = 0 where brand_id = %s"%brand_id
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update brand set delete_status=1,update_time='%s' where id=%s"%(update_time,brand_id)
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)
    recordFlow(author,"delete","brand",sql)

    r.hdel("brand_name_id",brand_info['name'])
    r.srem("brand_url_all",brand_info['url'])
    r.delete("click_time_brand_%s"%brand_id)
    db.execQueryAssoc("delete from hot_brand where brand_id=%s"%brand_id)
    return

def changeBrand(brand_id,name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author):
    '''
    编辑品牌
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    #if not  (name and description and company_name and cover_image and description  and meta_title and meta_keyword and meta_description):
    #    raise MyDefineError('必须填写所有字段')
    brand_info = getBrandByID(brand_id)
    if name != brand_info['name']:
        if name in r.hkeys("brand_name_id"):
            raise MyDefineError("品牌已存在")

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update brand set name='%s',description='%s',company_name='%s',company_website='%s',brand_classify='%s',company_address='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',cover_image='%s',update_time='%s' where id=%s"\
            %(name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,update_time,brand_id)
    db.execUpdate(sql)
    recordFlow(author,"modify","brand",sql)

    if name != brand_info['name']:
        r.hdel("brand_name_id",brand_info['name'])
        r.hset("brand_name_id",name,brand_id)
    return 

def getBrandByID(brand_id):
    '''
    通过id获取品牌信息，只是取一部分而已
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select name,url,cover_image from brand where id = %s and delete_status=0"%brand_id
    result = db.execQueryAssoc(sql)[0]
    return result

def getBrandInfoByID(brand_id):
    '''
    通过id获取品牌信息，只是取全部
    '''
    db = DBAccess()
    db.dbName = "zixun"

    sql = "select * from brand where id = %s and delete_status=0"%brand_id
    result = db.execQueryAssoc(sql)[0]
    return result

def getAllBrand():
    '''
    获取所有品牌名称
    '''
    db = DBAccess()
    db.dbName = "zixun"

    result = db.execQueryAssoc("select name from brand where delete_status=0")
    result = [ _['name'] for _ in result]
    return result

def getBrandInfo(url):
    '''
    获取品牌详情
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    result = db.execQueryAssoc("select * from brand where url = '%s' and delete_status=0"%url)[0]
    r.incr("click_time_brand_%s"%result['id'])
    return result

def getArticleByBrand(brand_url,page=-1):
    '''
    根据品牌返回文章列表和文章导读
    '''

    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    page =  1 if page < 1 else page
    pageNum = 10
    start = pageNum * (page - 1)
    page_p = "limit %s,%s"%(start,pageNum)
    query = " where delete_status=0 and if_display=1 and brand_id in (select id from brand where url='%s') and delete_status=0 and if_display=1 "%brand_url
    sql = "select id,title,cover_image,description,create_time,catagory_id from article %s order by update_time desc %s"%(query,page_p)
    articles = db.execQueryAssoc(sql)
    for article in articles:
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(article['id'])
        article['tag'] = db.execQueryAssoc(sql)
        article['complete_url'] = getCatagoryCompleteUrl(article['catagory_id'])
    recordNum = db.execQuery("select count(id) from article %s"%query)[0][0]
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,articles

def addCollocationArticle(title,tag,catagory,content,meta_title,meta_keyword,meta_description,cover_image,if_display,author):
    '''
    新增搭配栏目的文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    if not (title and tag and catagory and cover_image and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')

    collocation_ids = r.lrange("collocation_catagory_ids",0,100)
    catagory_id = r.hget("catagory_name_id",catagory)
    if catagory_id not in collocation_ids:
        raise MyDefineError("栏目不属于搭配")
    if not catagory_id:
        raise MyDefineError('没有这个栏目')
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into article (title,catagory_id,cover_image,content,author,create_time,meta_title,meta_keyword,meta_description,update_time,if_display) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)"\
            %(title,catagory_id,cover_image,content,author,create_time,meta_title,meta_keyword,meta_description,create_time,if_display)
    article_id = db.execNonQuery(sql)
    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = r.hget("tag_name_id",tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    r.set("click_time_article_%s"%article_id, 0)
    complete_url = getCatagoryCompleteUrl(catagory_id)
    recordFlow(author,"add","dapei_article",sql)
    return complete_url + '/' + str(article_id),article_id

def changeCollocationArticle(article_id,tag,title,catagory,cover_image,content,meta_title,meta_keyword,meta_description,author,if_display):
    '''
    修改搭配文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    if not (title and tag and catagory and cover_image  and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')

    collocation_ids = r.lrange("collocation_catagory_ids",0,100)
    catagory_id = r.hget("catagory_name_id",catagory)
    if catagory_id not in collocation_ids:
        raise MyDefineError("栏目不属于搭配")
    if not catagory_id:
        raise MyDefineError('没有这个目录')

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update article set title='%s',catagory_id='%s',cover_image='%s',content='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',if_display=%s where id=%s"\
                %(title,catagory_id,cover_image,content,meta_title,meta_keyword,meta_description,update_time,if_display,article_id)
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)
    recordFlow(author,"modify","article",sql)

    sql = "delete from article_tag where article_id=%s"%article_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)

    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = r.hget("tag_name_id",tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    complete_url = getCatagoryCompleteUrl(catagory_id)
    return complete_url + '/' + str(article_id)

def getCollocationArticleForBacker(article_id):
    '''
    后台查看搭配文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select * from article where  delete_status=0 and id = %s"%article_id

    try:
        article = db.execQueryAssoc(sql)[0]
    except(IndexError):
        return []
    article['tag'] = getTagInfoByArticle(article_id)
    article['catagory_name'] = getCatagoryNameWithID(article['catagory_id'])
    result = []
    for image_info in article['content'].split(','):
        temp = image_info.split('&')
        if len(temp) >= 2:
            result.append(temp)
    article['content'] = result
    return article


def updateHotTag(catagory_id,hot_tag):
    '''
    更新hot tag，存储方式为hot_tag_id:[tag_name&url,]
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    hot_tag = hot_tag.split(',')
    r.delete("hot_tag_%s"%catagory_id)
    db.execNonQuery("delete from hot_tag where catagory_id=%s"%catagory_id)
    for tag_name in hot_tag:
        tag_id = r.hget("tag_name_id",tag_name)
        if tag_id:
            tag_info = getTagByID(tag_id)
            r.lpush("hot_tag_%s"%catagory_id,tag_info['name'] + '&' + tag_info['url'])
            db.execNonQuery("insert into hot_tag (catagory_id, tag_id) values ('%s','%s')"%(catagory_id,tag_id))
    return

def updateHotBrand(catagory_id,hot_brand):
    '''
    更新hot tag，存储方式为hot_brand_id:[brand_name&url,]
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    hot_brand = hot_brand.split(',')
    r.delete("hot_brand_%s"%catagory_id)
    db.execNonQuery("delete from hot_brand where catagory_id=%s"%catagory_id)
    for brand_name in hot_brand:
        brand_id = r.hget("brand_name_id",brand_name)
        if brand_id:
            brand_info = getBrandByID(brand_id)
            r.lpush("hot_brand_%s"%catagory_id,brand_info['name'] + '&' + brand_info['url'] + '&' + brand_info['cover_image'])
            db.execNonQuery("insert into hot_brand (catagory_id, brand_id) values ('%s','%s')"%(catagory_id,brand_id))
    return

def changeIndex(hot_tag,hot_brand,meta_title,meta_keyword,meta_description,cover_image,shopping_goods,author):
    '''
    修改首页,首页在catagory中的id是1000
    '''
    db = DBAccess()
    db.dbName = "zixun"

    if not (hot_tag and hot_brand and cover_image and shopping_goods and meta_title and meta_keyword and meta_description):
        raise MyDefineError("必须全部填写")
    sql = "update index_page set meta_title='%s',meta_keyword='%s',meta_description='%s',cover_image='%s',shopping_goods='%s'"\
            %(meta_title,meta_keyword,meta_description,cover_image,shopping_goods)
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)
    updateHotTag(1000,hot_tag)
    updateHotBrand(1000,hot_brand)
    recordFlow(author,"modify","index",sql)
    return

def getIndexInfo():
    '''
    获得首页信息
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    index_info = db.execQueryAssoc("select * from index_page where id = 1")[0]
    cover_image = []
    for item in index_info['cover_image'].split(','):
        foo = item.split('&')
        if len(foo) == 2:
            cover_image.append(foo)
    shopping_goods = []
    for item in index_info['shopping_goods'].split(','):
        foo = item.split('&')
        if len(foo) == 2:
            shopping_goods.append(foo)
    return index_info,cover_image,shopping_goods


def getIndexArticleNotUse():
    '''
    获得首页文章列表
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    result = [0] * 7
    for idx in range(len(NAVIGATE)):
        catagory_id = r.hget("catagory_name_id",NAVIGATE[idx])
        articles = db.execQuery("select title,id,description,cover_image,catagory_id from article where catagory_id=%s order by create_time desc limit 8"%catagory_id)
        for article in articles:
            article = list(article)
            if idx < 2:
                article[0] = cutOffSentence(article[0],11)
                article[1] = cutOffSentence(article[2],20)
            if idx == 2:
                article[0] = cutOffSentence(article[0],8)
        result[idx] = articles
    return result

def getIndexArticle():
    '''
    获得首页文章列表
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    result = [0] * 7
    for idx in range(len(NAVIGATE)):
        catagory_id = r.hget("catagory_name_id",NAVIGATE[idx])
        if idx <= 3:
            articles  =getLatestArticle(catagory_id=catagory_id)
        else:
            articles = db.execQuery("select title,id,description,cover_image,catagory_id from article where catagory_id=%s and delete_status=0 and if_display=1 order by create_time desc limit 8"%catagory_id)
            for article in articles:
                article = list(article)
        result[idx] = articles
    return result


def recordFlow(operator,operate,object_name,sql):
    '''
    记录流水表
    '''
    db = DBAccess()
    db.dbName = "zixun"
    db.execNonQuery('''insert into record_flow (operator,operate,object,sql_content) values ("%s","%s","%s","%s")'''%(operator,operate,object_name,sql))
    return


def updateMySQLClickTime():
    '''
    把Redis中的click_time写入MySQL中
    每两个小时运行一次
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select id,click_time from article where delete_status=0"
    item_info = db.execQueryAssoc(sql)
    DEBUGLOG.debug("开始写入文章点击次数")
    for item in item_info:
        click_time = r.get("click_time_article_%s"%item['id'])
        if click_time:
            db.execUpdate("update article set click_time=%s where id = %s"%(click_time,item['id']))
        else:
            r.set("click_time_article_%s"%item['id'],item['click_time'])

    sql = "select id,click_time from tag "
    item_info = db.execQueryAssoc(sql)
    DEBUGLOG.debug("开始写入标签点击次数")
    for item in item_info:
        click_time = r.get("click_time_tag_%s"%item['id'])
        if click_time:
            db.execUpdate("update tag set click_time=%s where id = %s"%(click_time,item['id']))
        else:
            r.set("click_time_tag_%s"%item['id'],item['click_time'])

    sql = "select id,click_time from brand where delete_status=0"
    item_info = db.execQueryAssoc(sql)
    DEBUGLOG.debug("开始写入品牌点击次数")
    for item in item_info:
        click_time = r.get("click_time_brand_%s"%item['id'])
        if click_time:
            db.execUpdate("update brand set click_time=%s where id = %s"%(click_time,item['id']))
        else:
            r.set("click_time_brand_%s"%item['id'],item['click_time'])

def updateLatestAndHotArticle():
    '''
    从MySQL中取出最新和最热的10篇文章，存储格式为：latest_article_id: [title&id,], hot_article_id:[title&id,]
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select id,name from catagory where delete_status=0"
    catagory = db.execQueryAssoc(sql)
    collocation_ids = r.lrange("collocation_catagory_ids",0,100)
    collocation_ids = [ int(_) for _ in collocation_ids]
    DEBUGLOG.debug(u"开始导出最热和最新的文章")

    for cata in catagory:
        r.delete("latest_article_%s"%cata['id'])
        items = db.execQueryAssoc("select id,title,description,cover_image,meta_description,catagory_id from article where delete_status=0 and if_display=1 and catagory_id=%s order by create_time desc limit 6"%cata['id'])
        for item in items:
            item['title'] = cutOffSentence(item['title'],14)
            if item['catagory_id'] in collocation_ids:
                item['description'] = cutOffSentence(item['meta_description'],26)
            else:
                item['description'] = cutOffSentence(item['description'],26)
            r.rpush("latest_article_%s"%cata['id'],item['title'] + '&' + str(item['id']) + '&' + item['description'] + '&' + item['cover_image'])

        r.delete("hot_article_%s"%cata['id'])
        items = db.execQueryAssoc("select id,title from article where delete_status=0 and if_display=1 and catagory_id=%s order by click_time desc limit 6"%cata['id'])
        for item in items:
            item['title'] = cutOffSentence(item['title'],24)
            r.rpush("hot_article_%s"%cata['id'],item['title'] + '&' + str(item['id']))

    #首页
    r.delete("latest_article_1000")
    items = db.execQueryAssoc("select id,title,catagory_id,description,cover_image from article where delete_status=0 and if_display=1 and catagory_id !=0 and catagory_id not in %s order by create_time desc limit 5"%(tuple(collocation_ids),))
    for item in items:
        item['title'] = cutOffSentence(item['title'],14)
        item['description'] = cutOffSentence(item['description'],26)
        complete_url = getCatagoryCompleteUrl(item['catagory_id'])
        r.rpush("latest_article_1000",item['title'] + '&' + complete_url + '/' + str(item['id']) + '&' + item['description'] + '&' + item['cover_image'])

    r.delete("hot_article_1000")
    items = db.execQueryAssoc("select id,title,catagory_id,description from article where delete_status=0 and if_display=1 and catagory_id != 0 and catagory_id not in %s order by click_time desc limit 20"%(tuple(collocation_ids),))
    for item in items:
        item['title'] = cutOffSentence(item['title'],24)
        item['description'] = cutOffSentence(item['description'],48)
        complete_url = getCatagoryCompleteUrl(item['catagory_id'])
        r.rpush("hot_article_1000",item['title'] + '&' + complete_url + '/'  + str(item['id']) + '&' + item['description'])

def updateHotTagAndBrand():
    '''
    同步更新热门标签和热门品牌到redis，为了防止改名造成的不同步
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    sql = "select id,name from catagory where delete_status=0"
    catagory = list(db.execQueryAssoc(sql))
    catagory.append({"id":1000})
    DEBUGLOG.debug(u"开始导出热门标签和热门品牌")

    for cata in catagory:
        r.delete("hot_tag_%s"%cata['id'])
        items = db.execQueryAssoc("select url,name from tag where id in (select tag_id from hot_tag where catagory_id=%s)"%cata['id'])
        for item in items:
            r.rpush("hot_tag_%s"%cata['id'],item['name'] + '&' + item['url'])

        r.delete("hot_brand_%s"%cata['id'])
        items = db.execQueryAssoc("select name,url,cover_image from brand where id in (select brand_id from hot_brand where catagory_id=%s)"%cata['id'])
        for item in items:
            r.rpush("hot_brand_%s"%cata['id'],item['name'] + '&' + item['url'] + '&' + item['cover_image'])

def updateLatestGood():
    '''
    更新最新商品列表
    '''
    r = getRedisObj()
    db = getMongoDBConn().shop

    DEBUGLOG.debug(u"开始导出热门标签和热门品牌")
    r.delete("latest_goods_for_zixun")
    goods_ids = r.lrange("happy_shopping_goods_ids",0,20)
    for goods_id in goods_ids:
        goodsObj = db.activity_goods.find_one({"_id":int(goods_id)})
        if goodsObj:
            q_box_image = goodsObj['image'][0]
            url = '/detail/%s/%s'%(goodsObj['activity_id'],goodsObj['_id'])
            goodsObj['name'] = cutOffSentence(goodsObj['name'],10)
            r.rpush('latest_goods_for_zixun',goodsObj['name'] + '&' + url + '&' + q_box_image)
    return

def updateNiceGoods():
    '''
    更新优品驾到
    为了节省资源，先从中选出玩具，女衣与儿童服装根据category去取
    '''
    r = getRedisObj()
    db = getMongoDBConn().shop

    DEBUGLOG.debug("开始更新优品驾到")
    r.delete("awesome_goods_lady")
    r.delete("awesome_goods_children")
    r.delete("awesome_goods_toy")
    activity_ids = r.lrange("happy_shopping_activity_ids",0,300)
    lady_ids,children_ids,toy_ids = [],[],[]
    toy_leimu = db.leimu.find({"name":{"$regex":"玩具"}},{"_id":1})
    toy_leimu = [ int(float(_['_id'])) for _ in toy_leimu]
    print "toy_leimu",toy_leimu
    print "happy_shopping",activity_ids

    for activity_id in activity_ids:
        activityObj = db.activity.find_one({"_id":int(float(activity_id))})
        if not activityObj:
            continue
        #print activityObj.get('category'),activityObj.get("leimu_id")
        if len(toy_ids) < 20 and activityObj['leimu_id'] in toy_leimu:
            toy_ids.extend(random.sample(activityObj["goods_id"],5))
        elif len(lady_ids) < 20 and activityObj['category'] == "ladys":
            lady_ids.extend(random.sample(activityObj["goods_id"],5))
        elif len(children_ids) < 20 and activityObj['category'] == "children":
            children_ids.extend(random.sample(activityObj["goods_id"],5))
        if len(toy_ids) >= 20 and len(lady_ids) >= 20 and len(children_ids) >= 20:
            break

    r.delete("awesome_goods_lady")
    for goods_id in lady_ids:
        goodsObj = getGoodsInfo(goods_id)
        r.rpush("awesome_goods_lady",goodsObj['name'] + '&' + goodsObj['url'] + '&' + goodsObj['image'])

    r.delete("awesome_goods_children")
    for goods_id in children_ids:
        goodsObj = getGoodsInfo(goods_id)
        r.rpush("awesome_goods_children",goodsObj['name'] + '&' + goodsObj['url'] + '&' + goodsObj['image'])

    r.delete("awesome_goods_toy")
    for goods_id in toy_ids:
        goodsObj = getGoodsInfo(goods_id)
        r.rpush("awesome_goods_toy",goodsObj['name'] + '&' + goodsObj['url'] + '&' + goodsObj['image'])
    return

def updateFashionArticle():
    '''
    把时尚新鲜货存入redis
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    parent_id = r.hget("catagory_name_id","服装搭配")
    catagory_ids = db.execQueryAssoc("select id from catagory where parent_id=%s"%parent_id)
    catagory_ids = [ int(_['id']) for _ in catagory_ids] + [int(parent_id),]
    if len(catagory_ids) > 1:
        sql = "select id,catagory_id,cover_image from article where catagory_id in %s and delete_status=0 order by create_time desc limit 40"%(tuple(catagory_ids),)
    else:
        sql = "select id,catagory_id,cover_image from article where catagory_id = %s and delete_status=0 order by create_time desc limit 40"%catagory_ids[0]
    ERRORLOG.error(sql)
    articles = db.execQueryAssoc(sql)
    r.delete("fashion_article_for_zixun")
    for article in articles:
        complete_url = getCatagoryCompleteUrl(article['catagory_id'])
        r.rpush("fashion_article_for_zixun",article['cover_image'] + '&' + complete_url + '/' + str(article['id']))
    return

def updateCollocationCatagoryIds():
    '''
    更新搭配栏目的栏目id
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()
    parent_id = r.hget("catagory_name_id","服装搭配")
    collocation_ids = db.execQueryAssoc("select id from catagory where delete_status=0 and parent_id=%s"%parent_id)
    r.delete("collocation_catagory_ids")
    r.lpush("collocation_catagory_ids",parent_id)
    for item in collocation_ids:
        r.lpush("collocation_catagory_ids",item['id'])
    print r.lrange("collocation_catagory_ids",0,100),"collocation_catagory_ids"
    return

def getLatestGood():
    '''
    获得最新商品
    '''
    r = getRedisObj()

    goods_info = r.lrange("latest_goods_for_zixun",0,20)
    goods_info = random.sample(goods_info,4)
    result = []
    for goodsObj in goods_info:
        result.append(goodsObj.split('&'))
    return result

def getNiceGoods():
    '''
    获得优品驾到
    '''
    r = getRedisObj()

    result = {"lady":[],"children":[],"toy":[]}
    for item in result.keys():
        try:
            goodsObjs = random.sample(r.lrange("awesome_goods_%s"%item,0,20),6)
        except(ValueError):
            goodsObjs = r.lrange("awesome_goods_%s"%item,0,20)
        for goodsObj in goodsObjs:
            goodsObj = goodsObj.split('&')
            result[item].append(goodsObj)
    return result

def getDisplayStatus(status):
    '''
    返回状态显示的中文
    '''
    try:
        return "是" if int(status) else "否"
    except:
        return status

def cutOffSentence(sentence,length):
    '''
    截取指定长度的文字
    '''
    if len(sentence) > length:
        sentence = sentence[:length-2] + '...'
    return sentence

def timeFormatConvert(_time):
    '''
    截取时间
    '''
    try:
        return _time.strftime("%Y-%m-%d %H:%M")
    except:
        return _time

def getGoodsInfo(goods_id):
    '''
    根据一个商品ID，返回符合redis缓存的格式
    '''
    db = getMongoDBConn().shop

    goodsObj = db.activity_goods.find_one({"_id":int(goods_id)},{"activity_id":1,"image":1,"name":1})
    if goodsObj:
        goodsObj['image'] = goodsObj['image'][0]
        goodsObj['url'] = '/detail/%s/%s'%(goodsObj['activity_id'],goodsObj['_id'])
        goodsObj['name'] = cutOffSentence(goodsObj['name'],10)
    return goodsObj

def getNavigateHead():
    '''
    获得导航栏
    '''
    db = DBAccess()
    db.dbName = "zixun"
    #r = getRedisObj()

    cata_info = db.execQueryAssoc("select id,parent_id,name,url from catagory where delete_status=0")
    result = []
    for item in NAVIGATE:
        parent_id = r.hget("catagory_name_id",item)
        if parent_id:
            result.append([ _ for _ in cata_info if int(_['parent_id']) == int(parent_id)])
        else:
            result.append([])
    return result
#navigate = getNavigateHead()


def getFashionArticle():
    '''
    返回10篇时尚新鲜货
    '''
    r = getRedisObj()

    try:
        articles = random.sample(r.lrange("fashion_article_for_zixun",0,40),10)
    except(ValueError):
        articles = r.lrange("fashion_article_for_zixun",0,20)
    result = []
    for article in articles:
        result.append(article.split('&'))
    return result
#fashion_article = getFashionArticle()

def getArticlesWithSearch(search,page=-1):
    '''
    搜索获得文章列表
    '''
    import re
    db = DBAccess()
    db.dbName = "zixun"

    pageNum = 12
    page = 1 if page < 1 else page
    start = pageNum * (page - 1)
    page_p = " limit %s,%s"%(start,pageNum)

    search = re.sub("[?*.$@!&^]",' ',search)
    search = search.replace(" ",".*")
    sql = "select create_time,id,catagory_id,title,description,cover_image from article where delete_status=0 and if_display=1 and catagory_id != 0 and title regexp '%s' order by create_time desc %s"%(search,page_p)
    result = db.execQueryAssoc(sql)

    for r in result:
        r['complete_url'] = getCatagoryCompleteUrl(r['catagory_id'])
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(r['id'])
        r['tag'] = db.execQueryAssoc(sql)
    recordNum = db.execQuery("select count(id) from article where title regexp '%s'"%search)[0][0]
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,result

def getCollocationIds():
    '''
    获得所有搭配的id
    '''
    r = getRedisObj()
    return r.lrange("collocation_catagory_ids",0,100)

def getRandomArticle():
    '''
    获得随机的文章
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    collocation_ids = r.lrange("collocation_catagory_ids",0,100)
    collocation_ids = [ int(_) for _ in collocation_ids ]
    recordNum = db.execQuery("select max(id) from article where delete_status=0 and if_display=1")[0][0]
    result = []
    while len(result) < 10:
        article_ids = random.sample(range(recordNum),40)
        result = db.execQueryAssoc("select id,title,cover_image,description,catagory_id,create_time from article where delete_status=0 and if_display=1 and catagory_id>0 and id in %s and catagory_id not in %s "%(tuple(article_ids),tuple(collocation_ids)))
    for r in result:
        if int(r['catagory_id']) == 0:
            continue
        r['complete_url'] = getCatagoryCompleteUrl(r['catagory_id'])
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(r['id'])
        r['tag'] = db.execQueryAssoc(sql)
    return result

def getCollocationArticlesByCatagory(url,page=-1):
    '''
    获取搭配文章列表
    '''
    db = DBAccess()
    db.dbName = "zixun"

    pageNum = 10
    page = 1 if page < 1 else page
    start = pageNum * (page - 1)
    page_p = " limit %s,%s"%(start,pageNum)

    query = " where catagory_id in (select id from catagory where url = '%s')"%url
    query += " and delete_status=0 and if_display = 1 "
    sql = "select id,title,cover_image,description,create_time,meta_description from article %s order by update_time desc %s" %(query,page_p)
    articles = db.execQueryAssoc(sql)
    for article in articles:
        sql = "select name,url from tag where id in (select tag_id from article_tag where article_id = %s)" %(article['id'])
        article['tag'] = db.execQueryAssoc(sql)
        try:
            article['description'] = article['meta_description']
        except:
            ERRORLOG.error(article)
            article['description'] = ''

    recordNum = db.execQuery("select count(id) from article %s"%query)[0][0]
    pageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,pageCount,articles
