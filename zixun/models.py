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

    if not (title and tag and catagory and cover_image and description and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')

    catagory_id = getObjectIdWithName('catagory',catagory)
    if not catagory_id:
        raise MyDefineError('没有这个栏目')
    brand_id = getObjectIdWithName('brand',brand)
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into article (title,catagory_id,cover_image,description,content,author,create_time,meta_title,meta_keyword,meta_description,update_time,if_display,brand_id) values ('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s)"\
    		%(title,catagory_id,cover_image,description,content,author,create_time,meta_title,meta_keyword,meta_description,create_time,if_display,brand_id)
    article_id = db.execNonQuery(sql)
    print article_id
    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = getObjectIdWithName('tag',tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    complete_url = getCatagoryCompleteUrl(catagory_id)
    recordFlow(author,"add","article",sql)
    return complete_url + '/' + str(article_id),article_id

def changeArticle(article_id,tag,title,catagory,cover_image,description,content,meta_title,meta_keyword,meta_description,author,if_display,brand):
    '''
    修改文章
    '''
    db = DBAccess()
    db.dbName = "zixun"

    if not (title and tag and catagory and cover_image and description and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')
    catagory_id = getObjectIdWithName('catagory',catagory)
    if not catagory_id:
        raise MyDefineError('没有这个目录')
    brand_id = getObjectIdWithName('brand',brand)
    if not brand_id:
        brand_id = 0

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update article set title='%s',catagory_id='%s',cover_image='%s',description='%s',content='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',if_display=%s,brand_id=%s where id=%s"\
                %(title,catagory_id,cover_image,description,content,meta_title,meta_keyword,meta_description,update_time,if_display,brand_id,article_id)
    db.execUpdate(sql)
    recordFlow(author,"modify","article",sql)

    sql = "delete from article_tag where article_id=%s"%article_id
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)

    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = getObjectIdWithName('tag',tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

    complete_url = getCatagoryCompleteUrl(catagory_id)
    return complete_url + '/' + str(article_id)

def addTag(parent_name,name,meta_title,meta_keyword,meta_description,author):
    '''
    增加标签
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()
    p = Pinyin()

    if parent_name:
        parent_id = getObjectIdWithName('tag',parent_name)
        if not parent_id:
            raise MyDefineError("一级标签不存在")
    else:
        parent_id = 0

    names_all = getAllObjectUrlsOrNames("tag",'name')
    if name in names_all:
        raise MyDefineError("标签已存在")

    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    urls_all = getAllObjectUrlsOrNames('tag','url')
    while url in urls_all:
        url += str(random.randint(0,30))

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into tag (name,url,update_time,parent_id,meta_title,meta_keyword,meta_description) values ('%s','%s','%s',%s,'%s','%s','%s')"\
            %(name,url,update_time,parent_id,meta_title,meta_keyword,meta_description)
    tag_id = db.execNonQuery(sql)
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

    tag_names_exists = getAllObjectUrlsOrNames("tag","name")
    tag_ids = []
    for tag_name in tag_names:
        if tag_name not in tag_names_exists:
            tag_ids.append(addTag(tag_name))
        else:
            tag_ids.append(getObjectIdWithName('tag',tag_name))
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


def getArticleByIDForBacker(article_id):
    '''
    根据文章id取出文章
    '''
    db = DBAccess()
    db.dbName = "zixun"

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

    page = 1 if page < 1 else page
    pageNum = 30
    start = pageNum * (page - 1)
    page_p = " limit %s,%s "%(start,pageNum)

    sql = "select id,catagory_id,title,description,cover_image,author,create_time,meta_title,meta_keyword,meta_description,if_display,update_time,click_time,brand_id from article"

    query = " where delete_status=0 "
    if catagory_name:
        catagory_id = getObjectIdWithName('catagory',catagory_name)
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
    PageCount = recordNum / pageNum + (1 if recordNum % pageNum else 0)
    return recordNum,PageCount,result

def deleteArticle(article_id,author):
    '''
    删除文章
    '''
    db = DBAccess()
    db.dbName = "zixun"

    article_info = db.execQueryAssoc("select catagory_id,title from article where id = %s"%article_id)[0]
    sql = "delete from article_tag where article_id = %s"%article_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "delete from article where id = %s"%article_id
    db.execNonQuery(sql)

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

    sql = "select * from tag where url = '%s' "%url
    tag_info = db.execQueryAssoc(sql)[0]
    incrClickTime('tag',tag_info['id'])
    return tag_info

def deleteTag(tag_id,author):
    '''
    删除标签，tag表，article_tag表，以及Redis都要删除
    '''
    db = DBAccess()
    db.dbName = "zixun"

    son_tag = db.execQueryAssoc("select id from tag where parent_id=%s"%tag_id)
    if son_tag:
        raise MyDefineError("有子标签不能删除")
    tag_info = db.execQueryAssoc('select url,name from tag where id = %s'%tag_id)[0]
    sql = "delete from article_tag where tag_id = %s" %tag_id
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)
    sql = "delete from tag where id = %s" %tag_id
    db.execNonQuery(sql)
    recordFlow(author,"delete","tag",sql)

    db.execNonQuery("delete from hot_tag where tag_id = %s"%tag_id)
    return

def getTags(name='',meta_title='',meta_keyword='',meta_description='',start_time='',end_time='',sort='',page=-1,parent_tag=''):
    '''
    编辑：获得所有标签列表
    '''
    db = DBAccess()
    db.dbName = "zixun"

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
        parent_id = getObjectIdWithName('tag',parent_tag)
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

    sql = "select name,url from tag where id=%s" %tag_id
    tag_info = db.execQueryAssoc(sql)[0]
    if name != tag_info['name']:
        names_all = getAllObjectUrlsOrNames("tag","name")
        if name in names_all:
            raise MyDefineError("标签已存在")

    if parent_name:
        parent_id = getObjectIdWithName('tag',parent_name)
        if not parent_id:
            raise MyDefineError("一级标签不存在")
    else:
        parent_id = 0

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update tag set name='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',parent_id=%s where id=%s"\
        %(name,meta_title,meta_keyword,meta_description,update_time,parent_id,tag_id)
    db.execNonQuery(sql)
    recordFlow(author,"modify","tag",sql)

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

    result = []
    parent_id = getObjectIdWithName('catagory',"服装搭配")
    result.append("服装搭配")
    sql = "select name from catagory where parent_id = %s and delete_status=0" %parent_id
    second_level = db.execQueryAssoc(sql)
    result.append([_['name'] for _ in second_level])
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
        item['hot_tag'] = [ _['name'] for _ in hot_tag]
        hot_brand = getHotBrands(catagory_id=item['id'])
        item['hot_brand'] = [ _['name'] for _ in hot_brand]
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
    p = Pinyin()

    if not name:
        raise MyDefineError("名称不能为空")
    names_all = getAllObjectUrlsOrNames('catagory','name')
    if name in names_all:
        raise MyDefineError("栏目已存在")
    if parent_name:
        parent_id = getObjectIdWithName('catagory',parent_name)
        if not parent_id:
            raise MyDefineError("父栏目不存在")
    else:
        parent_id = 0
    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    urls_all = getAllObjectUrlsOrNames('catagory','url')
    while url in urls_all:
        url += str(random.randint(0,30))

    sql = "insert into catagory (name, parent_id,url, meta_title,meta_keyword,meta_description,cover_image) values ('%s','%s','%s','%s','%s','%s','%s')" \
            %(name,parent_id,url,meta_title,meta_keyword,meta_description,cover_image)
    catagory_id = db.execNonQuery(sql)
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

    sql = "select name,parent_id from catagory where id=%s" %catagory_id
    old_info = db.execQueryAssoc(sql)[0]

    if name != old_info['name']:
        if old_info['parent_id'] == 0:
            raise MyDefineError("一级目录不允许改变")
        names_all = getAllObjectUrlsOrNames('catagory','name')
        if name in names_all:
            raise MyDefineError("栏目已存在")

    if parent_name:
        parent_id = getObjectIdWithName('catagory',parent_name)
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
    recordFlow(author,"modify","catagory",sql)
    db.execUpdate(sql)
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
    incrClickTime('article',article['id'])
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

    urls_all = getAllObjectUrlsOrNames('catagory','url')
    if child_url not in urls_all or parent_url not in urls_all:
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
    try:
        return db.execQueryAssoc(sql)[0]['name']
    except(IndexError,ValueError):
        return ''

def getObjectIdWithName(tableName, name):
    db = DBAccess()
    db.dbName = 'zixun'

    try:
        return db.execQueryAssoc("select id from %s where name = '%s'"%(tableName,name))[0]["id"]
    except(IndexError):
        return 0

def getAllObjectUrlsOrNames(tableName, item):
    db = DBAccess()
    db.dbName = 'zixun'

    items = db.execQuery("select %s from %s"%(item,tableName))
    items = [ _[0] for _ in items]
    return items


def incrClickTime(tableName,Object_id):
    db = DBAccess()
    db.dbName = 'zixun'

    db.execUpdate("update %s set click_time = click_time + 1 where id = %s"%(tableName, Object_id))
    return
    
def getCollocationAllIds():
    db = DBAccess()
    db.dbName = 'zixun'

    parent_id = db.execQuery("select id from catagory where name='服装搭配'")[0][0]
    all_ids = db.execQuery("select id from catagory where parent_id=%s"%parent_id)
    all_ids = [ int(_[0]) for _ in all_ids]
    all_ids.append(int(parent_id))
    return all_ids

def getLatestArticle(url='',catagory_id=0):
    '''
    6篇最新文章
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    if url:
        catagory_id = db.execQuery("select id from catagory where url= '%s' "%url)[0][0]

    if catagory_id == 1000:
        collocation_ids = getCollocationAllIds()
        query = " where catagory_id not in %s "%(tuple(collocation_ids),)
    elif catagory_id:
        query = " where catagory_id = %s"%catagory_id

    articles = db.execQueryAssoc("select id,title,catagory_id,description,cover_image,meta_description from article %s order by id desc limit 6"\
                %query)
    for article in articles:
        article['complete_url'] = getCatagoryCompleteUrl(article['catagory_id']) + '/' + str(article['id'])
        article['title'] = cutOffSentence(article['title'],15)
        article['description'] = cutOffSentence(article['description'],30)
        article['meta_description'] = cutOffSentence(article['meta_description'],30)
    return articles

def getHotArticle(url='',catagory_id=0):
    '''
    最多会有20篇热门文章
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    if url:
        catagory_id = db.execQuery("select id from catagory where url= '%s' "%url)[0][0]

    if catagory_id == 1000:
        collocation_ids = getCollocationAllIds()
        query = " where catagory_id not in %s "%(tuple(collocation_ids),)
    elif catagory_id:
        query = " where catagory_id = %s"%catagory_id

    articles = db.execQueryAssoc("select id,title,catagory_id,description,cover_image,meta_description from article %s order by click_time desc limit 6"\
                %query)
    for article in articles:
        article['complete_url'] = getCatagoryCompleteUrl(article['catagory_id']) + '/' + str(article['id'])
        article['title'] = cutOffSentence(article['title'],25)
        article['description'] = cutOffSentence(article['description'],70)
    return articles

def getHotTags(url='',catagory_id=-1):
    '''
    最热标签
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    if catagory_id < 0:
        catagory_id = getCatagoryInfo(url=url)['id']
    tag_ids = db.execQuery("select tag_id from hot_tag where catagory_id = %s"%catagory_id)
    tag_ids = [ _[0] for _ in tag_ids]
    result = []
    for tag_id in tag_ids:
        tag_info = getTagByID(tag_id=tag_id)
        result.append(tag_info)
    return result

def getHotBrands(url='',catagory_id=-1):
    '''
    最热品牌
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    if catagory_id < 0:
        catagory_id = getCatagoryInfo(url=url)['id']
    brand_ids = db.execQuery("select brand_id from hot_brand where catagory_id = %s"%catagory_id)
    brand_ids = [ _[0] for _ in brand_ids]
    result = []
    for brand_id in brand_ids:
        brand_info = getBrandByID(brand_id=brand_id)
        result.append(brand_info)
    return result

def deleteCatagory(catagory_id,author):
    '''
    删除目录，目录下文章catagory_id设为0
    '''
    db = DBAccess()
    db.dbName = "zixun"

    son_catagory = db.execQueryAssoc("select id from catagory where parent_id=%s and delete_status=0"%catagory_id)
    if son_catagory:
        raise MyDefineError("有子栏目不能删除")

    complete_url = getCatagoryCompleteUrl(catagory_id)
    catagory_info = db.execQueryAssoc("select name,url from catagory where id = %s"%catagory_id)[0]
    sql = "delete from catagory where id = %s"%catagory_id
    DEBUGLOG.debug(sql)
    db.execNonQuery(sql)
    recordFlow(author,"delete","catagory",sql)
    db.execUpdate("update article set catagory_id=0 where catagory_id = %s"%catagory_id)

    db.execNonQuery("delete from hot_tag where catagory_id=%s"%catagory_id)
    db.execNonQuery("delete from hot_brand where catagory_id=%s"%catagory_id)
    return

def addBrand(name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author):
    '''
    增加品牌
    '''
    db = DBAccess()
    db.dbName = "zixun"
    p = Pinyin()

    names_all = getAllObjectUrlsOrNames("brand",'name')
    if name in names_all:
        raise MyDefineError("品牌已存在")

    url = str(p.get_initials(name.decode('utf-8'),'')).lower()
    urls_all = getAllObjectUrlsOrNames("brand",'url')
    while url in urls_all:
        url += str(random.randint(0,30))

    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into brand (name,description,url,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author,create_time,update_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
            %(name,description,url,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author,create_time,create_time)
    brand_id = db.execNonQuery(sql)
    recordFlow(author,"add","brand",sql)

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

    brand_info = getBrandByID(brand_id)
    sql = "update article set brand_id = 0 where brand_id = %s"%brand_id
    DEBUGLOG.debug(sql)
    db.execUpdate(sql)

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "delete from brand where id=%s"%brand_id
    db.execUpdate(sql)
    recordFlow(author,"delete","brand",sql)

    db.execQueryAssoc("delete from hot_brand where brand_id=%s"%brand_id)
    return

def changeBrand(brand_id,name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,author):
    '''
    编辑品牌
    '''
    db = DBAccess()
    db.dbName = "zixun"

    if not  (name and description and company_name and cover_image and description  and meta_title and meta_keyword and meta_description):
        raise MyDefineError('必须填写所有字段')
    brand_info = getBrandByID(brand_id)
    if name != brand_info['name']:
        names_all = getAllObjectUrlsOrNames("brand",'name')
        if name in names_all:
            raise MyDefineError("品牌已存在")

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update brand set name='%s',description='%s',company_name='%s',company_website='%s',brand_classify='%s',company_address='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',cover_image='%s',update_time='%s' where id=%s"\
            %(name,description,company_name,company_website,brand_classify,company_address,meta_title,meta_keyword,meta_description,cover_image,update_time,brand_id)
    db.execUpdate(sql)
    recordFlow(author,"modify","brand",sql)

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
    通过id获取品牌信息，取全部
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

    result = db.execQueryAssoc("select * from brand where url = '%s' and delete_status=0"%url)[0]
    incrClickTime("brand",result['id'])
    return result

def getArticleByBrand(brand_url,page=-1):
    '''
    根据品牌返回文章列表和文章导读
    '''

    db = DBAccess()
    db.dbName = "zixun"

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

    if not (title and tag and catagory and cover_image and content and meta_title and meta_keyword and meta_description ):
        raise MyDefineError('必须全部填写')

    collocation_ids = getCollocationAllIds()
    catagory_id = getObjectIdWithName('catagory',catagory)
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
        tag_id = getObjectIdWithName('tag',tag_name)
        if tag_id:
            addTagAndArticle(article_id=article_id, tag_id=tag_id)

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

    collocation_ids = getCollocationAllIds()
    catagory_id = getObjectIdWithName('catagory',catagory)
    if catagory_id not in collocation_ids:
        raise MyDefineError("栏目不属于搭配")
    if not catagory_id:
        raise MyDefineError('没有这个目录')

    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "update article set title='%s',catagory_id='%s',cover_image='%s',content='%s',meta_title='%s',meta_keyword='%s',meta_description='%s',update_time='%s',if_display=%s where id=%s"\
                %(title,catagory_id,cover_image,content,meta_title,meta_keyword,meta_description,update_time,if_display,article_id)
    db.execUpdate(sql)
    recordFlow(author,"modify","article",sql)

    sql = "delete from article_tag where article_id=%s"%article_id
    db.execNonQuery(sql)
    recordFlow(author,"delete","article_tag",sql)

    tag_names = tag.split(",")
    tag_names = set(tag_names)
    for tag_name in tag_names:
        tag_id = getObjectIdWithName('tag',tag_name)
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

    hot_tag = hot_tag.split(',')
    db.execNonQuery("delete from hot_tag where catagory_id=%s"%catagory_id)
    for tag_name in hot_tag:
        tag_id = getObjectIdWithName('tag',tag_name)
        if tag_id:
            tag_info = getTagByID(tag_id)
            db.execNonQuery("insert into hot_tag (catagory_id, tag_id) values ('%s','%s')"%(catagory_id,tag_id))
    return

def updateHotBrand(catagory_id,hot_brand):
    '''
    更新hot tag
    '''
    db = DBAccess()
    db.dbName = "zixun"

    hot_brand = hot_brand.split(',')
    db.execNonQuery("delete from hot_brand where catagory_id=%s"%catagory_id)
    for brand_name in hot_brand:
        brand_id = getObjectIdWithName("brand",brand_name)
        if brand_id:
            brand_info = getBrandByID(brand_id)
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

def getIndexArticle():
    '''
    获得首页文章列表
    '''
    db = DBAccess()
    db.dbName = "zixun"

    result = [0] * 7
    for idx in range(len(NAVIGATE)):
        catagory_id = getObjectIdWithName('catagory',NAVIGATE[idx])
        articles  =getLatestArticle(catagory_id=catagory_id)
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


def updateFashionArticle():
    '''
    把时尚新鲜货存入redis
    '''
    db = DBAccess()
    db.dbName = "zixun"
    r = getRedisObj()

    parent_id = getObjectIdWithName('catagory',"服装搭配")
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

def getNavigateHead():
    '''
    获得导航栏
    '''
    db = DBAccess()
    db.dbName = "zixun"

    cata_info = db.execQueryAssoc("select id,parent_id,name,url from catagory where delete_status=0")
    result = []
    for item in NAVIGATE:
        parent_id = getObjectIdWithName('catagory',item)
        if parent_id:
            result.append([ _ for _ in cata_info if int(_['parent_id']) == int(parent_id)])
        else:
            result.append([])
    return result
navigate = getNavigateHead()


def getFashionArticle():
    '''
    返回10篇时尚新鲜货
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    collocation_ids = getCollocationAllIds()
    articles = db.execQueryAssoc("select catagory_id,id,cover_image from article where catagory_id in %s order by id desc limit 10"%(tuple(collocation_ids),))
    for article in articles:
        article['complete_url'] = getCatagoryCompleteUrl(article['catagory_id']) + '/' + str(article['id'])
    return articles

fashion_article = getFashionArticle()

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
