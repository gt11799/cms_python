#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from utility.utils import *
from utility.error_code import *
from models import *
from qiniu.models import cow,uploadImage
from utility.checkfile import isImageFileType
import uuid
from random import random

class IndexHandler(BasicTemplateHandler):
    '''
    显示首页
    '''
    def get(self):

        hot_tag = getHotTags(catagory_id=1000)
        hot_brand = getHotBrands(catagory_id=1000)
        latest_articles = getLatestArticle(catagory_id=1000)
        hot_articles = getHotArticle(catagory_id=1000)
        search = self.get_argument("search",'')

        index_info,cover_image,shopping_goods = getIndexInfo()
        if search:
            page = self.get_argument("page",0)
            recordNum,pageCount,articles = getArticlesWithSearch(search,page)
            collocation_ids = getCollocationIds()
            return self.render("news/search_article_list.html",index_info=index_info,hot_tag=hot_tag,hot_brand=hot_brand,cutOffSentence=cutOffSentence,fashion_article=fashion_article,
                    latest_articles=latest_articles,hot_articles=hot_articles,random=random,navigate=navigate,articles=articles,recordNum=recordNum,pageCount=pageCount,
                    timeFormatConvert=timeFormatConvert,collocation_ids=collocation_ids)
        articles = getIndexArticle()
        return self.render("news/index.html",index_info=index_info,cover_image=cover_image,shopping_goods=shopping_goods,hot_tag=hot_tag,hot_brand=hot_brand,
                    latest_articles=latest_articles,hot_articles=hot_articles,random=random,navigate=navigate,articles=articles,cutOffSentence=cutOffSentence)

class AddArticleHandler(BasicTemplateHandler):

    '''运营:增加文章'''

    #@staff_member()
    def get(self):
        catagory_all = getAllCatagory()
        tag_all = getAllTags()
        brand_all = getAllBrand()
        return self.render("zixun/add_article.html",catagory_all=catagory_all,tag_all=tag_all,brand_all=brand_all)

    def getArgument(self):
        Argu = {}
        Argu["title"] = self.get_argument("title")
        Argu['tag'] = self.get_argument("tag",'')
        Argu['catagory'] = self.get_argument("catagory")
        Argu['content'] = self.get_argument("content",'')
        Argu['description'] = self.get_argument("description",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['if_display'] = int(self.get_argument('if_display'))
        Argu['brand'] = self.get_argument("brand")
        return Argu

    def DBAction(self, Arguments):
        article_url,article_id = addArticle(**Arguments)
        self.write({"status": RET_OK,"url":article_url,"id":article_id})

    #@staff_member()
    def post(self):
        return self._post()

class EditArticleHandler(BasicTemplateHandler):

    '''运营:修改文章页面'''

    #@staff_member()
    def get(self):
        try:
            article_id = int(self.get_argument("id"))
        except(TypeError,ValueError):
            self.redirect("/zixun/admin/article_list")
        article = getArticleByIDForBacker(article_id)
        catagory_all = getAllCatagory()
        tags = getTagByArticle(article_id)
        if tags:
            tags = [ _['name'] for _ in tags ]
            parent_tag = getFirstLevelTag(tags[0])
        else:
            parent_tag = ''
        tag_all = getAllTags()
        brand_all = getAllBrand()
        return self.render("zixun/edit_article.html",catagory_all=catagory_all,article=article,tag_all=tag_all,brand_all=brand_all,tags=tags,parent_tag=parent_tag)

    def getArgument(self):
        Argu = {}
        Argu['article_id'] = self.get_argument("id")
        Argu["title"] = self.get_argument("title")
        Argu['tag'] = self.get_argument("tag",'')
        Argu['catagory'] = self.get_argument("catagory")
        Argu['content'] = self.get_argument("content",'')
        Argu['description'] = self.get_argument("description",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['if_display'] = int(self.get_argument('if_display'))
        Argu['brand'] = self.get_argument("brand")
        return Argu

    def DBAction(self, Arguments):
        article_url = changeArticle(**Arguments)
        self.write({"status": RET_OK,"url":article_url})

    #@staff_member()
    def post(self):
        return self._post()

class ArticleListHandler(BasicTemplateHandler):
    '''
    运营:显示文章列表
    '''
    #@staff_member()
    def get(self):
        
        catagory_name = self.get_argument("catagory_name",'')
        start_time = self.get_argument("start_time",'')
        end_time = self.get_argument("end_time",'')
        title = self.get_argument("title",'')
        description = self.get_argument("description",'')
        author = self.get_argument("author",'')
        meta_title = self.get_argument("meta_title",'')
        meta_keyword = self.get_argument("meta_keyword",'')
        meta_description = self.get_argument("meta_description",'')
        if_display = self.get_argument("if_display",'')
        page = int(self.get_argument("page",-1))
        sort = self.get_argument("sort",'')
        recordNum,pageCount,result = getArticles(catagory_name=catagory_name,start_time=start_time,end_time=end_time,title=title,description=description,author=author,
                            meta_title=meta_title,meta_keyword=meta_keyword,meta_description=meta_description,if_display=if_display,page=page,sort=sort)

        catagory_all = getAllCatagory()
        collocation_ids = getCollocationIds()
        return self.render("zixun/article_list.html",result=result,recordNum=recordNum,pageCount=pageCount,catagory_all=catagory_all,getDisplayStatus=getDisplayStatus,collocation_ids=collocation_ids)



class TagHandler(BasicTemplateHandler):
    '''显示该标签下的所有文章'''

    def get(self,tag_url):
        page = int(self.get_argument("page",-1))
        recordNum,pageCount,articles = getArticleByTag(tag_url,page=page)
        tag_info = getTagInfo(tag_url)
        hot_tags = getHotTags(catagory_id=1000)
        hot_brands = getHotBrands(catagory_id=1000)
        latest_articles = getLatestArticle(catagory_id=1000)
        hot_articles = getHotArticle(catagory_id=1000)
        nice_goods = getNiceGoods()
        collocation_ids = getCollocationIds()
        return self.render("news/tag_list.html",articles=articles,recordNum=recordNum,pageCount=pageCount,tag_info=tag_info,hot_tags=hot_tags,
                hot_brands=hot_brands,latest_articles=latest_articles,hot_articles=hot_articles,url=tag_url,timeFormatConvert=timeFormatConvert,
                cutOffSentence=cutOffSentence,random=random,navigate=navigate,fashion_article=fashion_article,nice_goods=nice_goods,collocation_ids=collocation_ids)

class TagListHandler(BasicTemplateHandler):
    '''
    运营:显示标签列表
    '''
    #@staff_member()
    def get(self):
        name = self.get_argument("name",'')
        start_time = self.get_argument("start_time",'')
        end_time = self.get_argument("end_time",'')
        meta_title = self.get_argument("meta_title",'')
        meta_keyword = self.get_argument("meta_keyword",'')
        meta_description = self.get_argument("meta_description",'')
        parent_tag = self.get_argument("parent_tag",'')
        page = int(self.get_argument("page",-1))
        sort = self.get_argument("sort",'')
        recordNum,pageCount,result = getTags(name=name,meta_title=meta_title,meta_keyword=meta_keyword,meta_description=meta_description,
                    start_time=start_time,end_time=end_time,sort=sort,page=page,parent_tag=parent_tag)
        first_level = getFirstLevelTags()
        tag_all = getAllTags()
        return self.render("zixun/tag_list.html",recordNum=recordNum,pageCount=pageCount,result=result,first_level=first_level,tag_all=tag_all)


class CatagoryHandler(BasicTemplateHandler):
    '''通过目录索取文章'''

    def get(self,first_level,second_level,article_id):
        page = int(self.get_argument("page",-1))

        if article_id:
            article_id = int(article_id[1:])
            cata_level = []
            cata_level.append(getCatagoryInfo(url=first_level))
            if second_level:
                url = second_level[1:]
                complete_url = first_level + second_level
                if not catagoryBelongTo(child_url=url,parent_url=first_level):
                    return self.render("error/404.html")
                cata_level.append(getCatagoryInfo(url=url))
                cata_level[1]['url'] = complete_url
            else:
                first_level_urls = getCatagoryFirstLevelURL()
                if first_level not in first_level_urls:
                    return self.render("error/404.html")
                url = first_level
                complete_url = first_level
            pageCount,article = getArticleWithCatagory(url,article_id,page=page)
            if not article:
                return self.render("error/404.html")
            hot_tags = getHotTags(url)
            hot_brands = getHotBrands(url)
            latest_articles = getLatestArticle(url)
            hot_articles = getHotArticle(url)
            random_articles = getRandomArticle()
            return self.render("news/article_detail.html",article=article,pageCount=pageCount,hot_tags=hot_tags,url=complete_url, hot_brands=hot_brands,random_articles=random_articles,
                    hot_articles=hot_articles,timeFormatConvert=timeFormatConvert,random=random,navigate=navigate,fashion_article=fashion_article,cutOffSentence=cutOffSentence,cata_level=cata_level)

        if second_level:
            url = second_level[1:]
            if not catagoryBelongTo(child_url=url,parent_url=first_level):
                return self.render("error/404.html")
            complete_url = first_level + second_level
        else:
            first_level_urls = getCatagoryFirstLevelURL()
            if first_level not in first_level_urls:
                return self.render("error/404.html")
            url = first_level
            complete_url = first_level
        cata_info = getCatagoryInfo(url=url)
        if not cata_info:
            return self.render("error/404.html")

        recordNum,pageCount,articles = getArticlesByCatagory(url=url,page=page)
        hot_tags = getHotTags(url)
        hot_brands = getHotBrands(url)
        latest_articles = getLatestArticle(url)
        hot_articles = getHotArticle(url)
        return self.render("news/article_list.html",recordNum=recordNum,pageCount=pageCount,articles=articles,cata_info=cata_info,latest_articles=latest_articles,hot_tags=hot_tags,url=complete_url,hot_brands=hot_brands,
                hot_articles=hot_articles,random=random,cutOffSentence=cutOffSentence,timeFormatConvert=timeFormatConvert,navigate=navigate,fashion_article=fashion_article)

class CatagoryListHandler(BasicTemplateHandler):
    '''
    运营:显示目录列表，后台管理
    '''
    #@staff_member()
    def get(self):
        catagory_all = getAllCatagory()
        catagories = getCatagories()
        tag_all = getAllTags()
        brand_all = getAllBrand()
        return self.render("zixun/catagory_list.html",catagory_all=catagory_all,catagories=catagories,tag_all=tag_all,brand_all=brand_all)

class AddCatagoryHandler(BasicTemplateHandler):
    '''
    运营:增加目录
    '''
    #@staff_member()
    def get(self):
        parent_name = self.get_argument("parent_name",'')
        tag_all = getAllTags()
        brand_all = getAllBrand()
        return self.render("zixun/add_catagory.html",parent_name=parent_name,tag_all=tag_all,brand_all=brand_all)

    def getArgument(self):
        Argu = {}
        Argu['parent_name'] = self.get_argument("parent_name")
        Argu['name'] = self.get_argument("name")
        Argu['meta_title'] = self.get_argument("meta_title")
        Argu['meta_keyword'] = self.get_argument("meta_keyword")
        Argu['meta_description'] = self.get_argument("meta_description")
        Argu['hot_tag'] = self.get_argument("hot_tag")
        Argu['hot_brand'] = self.get_argument("hot_brand")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['cover_image'] = self.get_argument("cover_image")
        return Argu

    def DBAction(self, Arguments):
        addCatagory(**Arguments)
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        return self._post()

class EditCatagoryHandler(BasicTemplateHandler):
    '''
    运营:编辑目录页面
    '''
    #@staff_member()
    def get(self):
        name = self.get_argument("name")
        if not name:
            return
        result = getCatagoryInfo(name=name)
        catagory_all = getAllCatagory()
        hot_tag = getHotTags(catagory_id=result['id'])
        hot_tag = [ _[0] for _ in hot_tag]
        if hot_tag:
            parent_tag = getFirstLevelTag(hot_tag[0])
        else:
            parent_tag = ''
        hot_brand = getHotBrands(catagory_id=result['id'])
        hot_brand = [ _[0] for _ in hot_brand]
        tag_all = getAllTags()
        brand_all = getAllBrand()
        return self.render("zixun/edit_catagory.html",result=result,catagory_all=catagory_all,hot_brand=hot_brand,hot_tag=hot_tag,parent_tag=parent_tag,tag_all=tag_all,brand_all=brand_all)


    def getArgument(self):
        Argu = {}
        Argu['catagory_id'] = self.get_argument("id")
        Argu['parent_name'] = self.get_argument("parent_name")
        Argu['name'] = self.get_argument("name")
        Argu['meta_title'] = self.get_argument("meta_title")
        Argu['meta_keyword'] = self.get_argument("meta_keyword")
        Argu['meta_description'] = self.get_argument("meta_description")
        Argu['hot_tag'] = self.get_argument("hot_tag")
        Argu['hot_brand'] = self.get_argument("hot_brand")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['cover_image'] = self.get_argument("cover_image")
        return Argu

    def DBAction(self, Arguments):
        changeCatagory(**Arguments)
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        return self._post()


class EditTagHandler(BasicTemplateHandler):
    '''
    运营:更改标签
    '''
    #@staff_member()
    def get(self):
        try:
            tag_id = int(self.get_argument("id"))
        except(TypeError):
            return self.redirect("/zixun/admin/tag_list")
        tag_info = getTagByID(tag_id)
        return self.render("zixun/edit_tag.html",tag_info=tag_info)

    def getArgument(self):
        Argu = {}
        Argu['tag_id'] = self.get_argument("id")
        Argu['name'] = self.get_argument("name")
        Argu['parent_name'] = self.get_argument("parent_name")
        Argu['meta_title'] = self.get_argument("meta_title")
        Argu['meta_keyword'] = self.get_argument("meta_keyword")
        Argu['meta_description'] = self.get_argument("meta_description")
        Argu['author'] = self.get_secure_cookie("cuser")
        return Argu

    def DBAction(self, Arguments):
        changeTag(**Arguments)
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        return self._post()

class AddTagHandler(BasicTemplateHandler):
    '''
    运营:添加标签
    '''
    def getArgument(self):
        Argu = {}
        Argu['parent_name'] = self.get_argument("parent_name")
        Argu['name'] = self.get_argument("name")
        Argu['meta_title'] = self.get_argument("meta_title")
        Argu['meta_keyword'] = self.get_argument("meta_keyword")
        Argu['meta_description'] = self.get_argument("meta_description")
        Argu['author'] = self.get_secure_cookie("cuser")
        return Argu

    def DBAction(self, Arguments):
        addTag(**Arguments)
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        return self._post()

class DeleteHandler(BasicTemplateHandler):
    '''
    运营:删除文章、标签、目录、品牌
    '''
    def getArgument(self):
        Argu = {}
        Argu['object_id'] = self.get_argument("id")
        Argu['object'] = self.get_argument("object")
        Argu['author'] = self.get_secure_cookie("cuser")
        return Argu

    def DBAction(self, Arguments):
        if Arguments['object'] == 'tag':
            deleteTag(Arguments['object_id'],Arguments['author'])
        elif Arguments['object'] == 'catagory':
            deleteCatagory(Arguments['object_id'],Arguments['author'])
        elif Arguments['object'] == 'article':
            deleteArticle(Arguments['object_id'],Arguments['author'])
        elif Arguments['object'] == 'brand':
            deleteBrand(Arguments['object_id'],Arguments['author'])
        else:
            raise MyDefineError("参数不对")
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        return self._post()


class AdminHandler(BasicTemplateHandler):
    '''
    运营:主目录重定向
    '''
    def get(self):
        return self.redirect("/zixun/admin/catagory_list/")

class AddBrandHandler(BasicTemplateHandler):
    '''
    运营:增加品牌
    '''

    def getArgument(self):
        Argu = {}
        Argu["name"] = self.get_argument("name")
        Argu['description'] = self.get_argument("description",'')
        Argu['company_name'] = self.get_argument("company_name",'')
        Argu['company_website'] = self.get_argument("company_website",'')
        Argu['brand_classify'] = self.get_argument("brand_classify",'')
        Argu['company_address'] = self.get_argument("company_address",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        return Argu

    def DBAction(self, Arguments):
        brand_id = addBrand(**Arguments)
        self.write({"status": RET_OK,"id":brand_id})

    #@staff_member()
    def post(self):
        self._post()

class BrandListHandler(BasicTemplateHandler):
    '''
    运营:显示品牌列表
    '''
    #@staff_member()
    def get(self):
        name = self.get_argument("name",'')
        start_time = self.get_argument("start_time",'')
        end_time = self.get_argument("end_time",'')
        description = self.get_argument("description",'')
        brand_classify = self.get_argument("brand_classify",'')
        author = self.get_argument("author",'')
        meta_title = self.get_argument("meta_title",'')
        meta_keyword = self.get_argument("meta_keyword",'')
        meta_description = self.get_argument("meta_description",'')
        company_address = self.get_argument("company_address",'')
        company_name = self.get_argument("company_name",'')
        page = int(self.get_argument("page",-1))
        sort = self.get_argument("sort",'')
        recordNum,pageCount,result = getBrands(name=name,start_time=start_time,end_time=end_time,description=description,brand_classify=brand_classify,company_name=company_name,
                                        company_address=company_address,author=author,meta_title=meta_title,meta_keyword=meta_keyword,meta_description=meta_description,page=page,sort=sort)
        return self.render("zixun/brand_list.html",recordNum=recordNum,pageCount=pageCount,result=result)

class EditBrandHandler(BasicTemplateHandler):
    '''
    运营:编辑品牌
    '''
    #@staff_member()
    def get(self):
        try:
            tag_id = int(self.get_argument("id"))
        except(TypeError):
            return self.redirect("/zixun/admin/brand_list/")
        brand_info = getBrandInfoByID(tag_id)
        return self.render("zixun/edit_brand.html",brand_info=brand_info)

    def getArgument(self):
        Argu = {}
        Argu['brand_id'] = self.get_argument("id")
        Argu["name"] = self.get_argument("name")
        Argu['description'] = self.get_argument("description",'')
        Argu['company_name'] = self.get_argument("company_name",'')
        Argu['company_website'] = self.get_argument("company_website",'')
        Argu['brand_classify'] = self.get_argument("brand_classify",'')
        Argu['company_address'] = self.get_argument("company_address",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        return Argu

    def DBAction(self, Arguments):
        changeBrand(**Arguments)
        self.write({"status": RET_OK})

    #@staff_member()
    def post(self):
        self._post()

class BrandHandler(BasicTemplateHandler):
    '''显示该标签下的所有文章'''

    def get(self,brand_url):
        page = int(self.get_argument("page",0))
        recordNum,pageCount,articles = getArticleByBrand(brand_url)
        brand_info = getBrandInfo(brand_url)
        hot_tags = getHotTags(catagory_id=1000)
        hot_brands = getHotBrands(catagory_id=1000)
        latest_articles = getLatestArticle(catagory_id=1000)
        hot_articles = getHotArticle(catagory_id=1000)
        latest_goods = getLatestGood()
        print [brand_info['description'],1]
        return self.render("news/brand_detail.html",recordNum=recordNum,pageCount=pageCount,articles=articles,brand_info=brand_info,
                hot_brands=hot_brands,latest_articles=latest_articles,hot_articles=hot_articles,timeFormatConvert=timeFormatConvert,hot_tags=hot_tags,
                cutOffSentence=cutOffSentence,random=random,latest_goods=latest_goods,navigate=navigate)

class GetTagJsonHandler(BasicTemplateHandler):
    '''
    运营:根据一级标签，返回二级标签名
    '''

    #@staff_member()
    def get(self):
        self._post()

    #@staff_member()
    def post(self):
        self._post()

    def getArgument(self):
        Argu = {}
        Argu['tag_name'] = self.get_argument("name")
        return Argu

    def DBAction(self, Arguments):
        names = getSecondLevelTagByName(Arguments['tag_name'])
        self.write({"status": RET_OK, "tags":names})

class EditIndexHandler(BasicTemplateHandler):
    '''
    运营:修改首页信息
    '''
    #@staff_member()
    def get(self):
        index_info,cover_image,shopping_goods = getIndexInfo()
        hot_tag = getHotTags(catagory_id=1000)
        hot_tag = [ _[0] for _ in hot_tag]
        hot_brand = getHotBrands(catagory_id=1000)
        hot_brand = [ _[0] for _ in hot_brand]
        tag_all = getAllTags()
        brand_all = getAllBrand()
        self.render("zixun/edit_index.html",tag_all=tag_all,brand_all=brand_all,index_info=index_info,cover_image=cover_image,shopping_goods=shopping_goods,hot_tag=hot_tag,
                                    hot_brand=hot_brand)

    #@staff_member()
    def post(self):
        self._post()

    def getArgument(self):
        Argu = {}
        Argu['hot_tag'] = self.get_argument("hot_tag")
        Argu['hot_brand'] = self.get_argument("hot_brand")
        Argu['meta_title'] = self.get_argument("meta_title")
        Argu['meta_keyword'] = self.get_argument("meta_keyword")
        Argu['meta_description'] = self.get_argument("meta_description")
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['shopping_goods'] = self.get_argument("shopping_goods")
        Argu['author'] = self.get_argument("cuser")
        return Argu

    def DBAction(self, Arguments):
        changeIndex(**Arguments)
        self.write({"status": RET_OK})

class UploadImageHandler(BasicTemplateHandler):
    '''
    百度编辑器的API
    '''

    #@staff_member()
    @tornado.gen.coroutine
    def get(self):
        self._post()

    #@staff_member()
    @tornado.gen.coroutine
    def post(self):
        self._post()


    def DBAction(self,Arguments):
        config = self.get_argument("action",'')
        if config == 'config':
            call_back = {
                "imageActionName": "uploadimage",
                "imageFieldName": "upfile",
                "imageMaxSize": 2048000, 
                "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                "imageCompressEnable": "true",
                "imageCompressBorder": 1600, 
                "imageInsertAlign": "none", 
                "imageUrlPrefix": "", 
                "imagePathFormat": "/zixun/upload_image/"
                }
        elif config == 'uploadimage':
            f = self.request.files.get("upfile")
            f = f[0]
            original_name = f.get("filename")
            image_type = f.get("content_type")
            fn = f["filename"].encode("utf-8")
            timestamp = int(time.time())
            filename = "image/zixun/%s.jpg"%str(uuid.uuid1())
            url = uploadImage(filename, f["body"])
            if RET_OK == 0:
                state = "SUCCESS"
            else:
                state = "FAIL"
            call_back = {
                "state" :state,
                "url" :url,
                "title" :"小荷资讯",
                "original" :original_name,
                "type":image_type,
            }
        else:
            raise MyDefineError("服务器未配置")
        print call_back
        self.write(call_back)

    
class AddCollocationArticleHandler(BrandListHandler):
    '''
    运营:增加搭配的文章
    '''  

    #@staff_member()
    def get(self):
        catagory_all = getCollocationCatagory()
        tag_all = getAllTags()
        return self.render("zixun/add_dapei_article.html",catagory_all=catagory_all,tag_all=tag_all)

    def getArgument(self):
        Argu = {}
        Argu["title"] = self.get_argument("title")
        Argu['tag'] = self.get_argument("tag",'')
        Argu['catagory'] = self.get_argument("catagory")
        Argu['content'] = self.get_argument("content",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['if_display'] = int(self.get_argument('if_display'))
        return Argu

    def DBAction(self, Arguments):
        article_url,article_id = addCollocationArticle(**Arguments)
        self.write({"status": RET_OK,"url":article_url,"id":article_id})

    #@staff_member()
    def post(self):
        return self._post()

class EditCollocationArticleHandler(BasicTemplateHandler):
    '''
    运营:编辑搭配文章
    '''
    #@staff_member()
    def get(self):
        try:
            article_id = int(self.get_argument("id"))
        except(TypeError,ValueError):
            self.redirect("/zixun/admin/article_list")
        article = getCollocationArticleForBacker(article_id)
        catagory_all = getCollocationCatagory()
        tags = getTagByArticle(article_id)
        if tags:
            tags = [ _['name'] for _ in tags ]
            parent_tag = getFirstLevelTag(tags[0])
        else:
            parent_tag = ''
        tag_all = getAllTags()
        return self.render("zixun/edit_dapei.html",catagory_all=catagory_all,article=article,tag_all=tag_all,tags=tags,parent_tag=parent_tag)

    def getArgument(self):
        Argu = {}
        Argu['article_id'] = self.get_argument("id")
        Argu["title"] = self.get_argument("title")
        Argu['tag'] = self.get_argument("tag",'')
        Argu['catagory'] = self.get_argument("catagory")
        Argu['content'] = self.get_argument("content",'')
        Argu['meta_title'] = self.get_argument("meta_title",'')
        Argu['meta_keyword'] = self.get_argument("meta_keyword",'')
        Argu['meta_description'] = self.get_argument("meta_description",'')
        Argu['cover_image'] = self.get_argument("cover_image")
        Argu['author'] = self.get_secure_cookie("cuser")
        Argu['if_display'] = int(self.get_argument('if_display'))
        return Argu

    def DBAction(self, Arguments):
        article_url = changeCollocationArticle(**Arguments)
        self.write({"status": RET_OK,"url":article_url})

    #@staff_member()
    def post(self):
        return self._post()

class CollocationCatagoryHandler(BasicTemplateHandler):
    '''通过目录索取搭配文章'''

    def get(self,second_level,article_id):
        page = int(self.get_argument("page",-1))

        if article_id:
            article_id = int(article_id[1:])
            cata_level = []
            cata_level.append(getCatagoryInfo(url=COLLOCATION_URL))
            if second_level:
                url = second_level[1:]
                complete_url = COLLOCATION_URL + second_level
                cata_level.append(getCatagoryInfo(url=url))
                cata_level[1]['url'] = complete_url
            else:
                url = COLLOCATION_URL
                complete_url = COLLOCATION_URL
            _,article = getArticleWithCatagory(url,article_id)
            article['content'] = collocationArticleContentHanlde(article['content'])
            if not article:
                return self.render("error/404.html")
            hot_tags = getHotTags(url)
            hot_brands = getHotBrands(url)
            latest_articles = getLatestArticle(url)
            hot_articles = getHotArticle(url)
            random_articles = getRandomArticle()
            return self.render("news/match_detail.html",article=article,hot_tags=hot_tags,url=complete_url, hot_brands=hot_brands,latest_articles=latest_articles,random_articles=random_articles,cata_level=cata_level,
                    hot_articles=hot_articles,timeFormatConvert=timeFormatConvert,random=random,navigate=navigate,fashion_article=fashion_article,cutOffSentence=cutOffSentence)

        if second_level:
            url = second_level[1:]
            complete_url = COLLOCATION_URL + second_level
        else:
            url = COLLOCATION_URL
            complete_url = COLLOCATION_URL
        cata_info = getCatagoryInfo(url=url)
        if not cata_info:
            return self.render("error/404.html")

        recordNum,pageCount,articles = getCollocationArticlesByCatagory(url=url,page=page)
        hot_tags = getHotTags(url)
        hot_brands = getHotBrands(url)
        latest_articles = getLatestArticle(url)
        hot_articles = getHotArticle(url)
        return self.render("news/match_list.html",recordNum=recordNum,pageCount=pageCount,articles=articles,cata_info=cata_info,latest_articles=latest_articles,hot_tags=hot_tags,url=complete_url,hot_brands=hot_brands,
                hot_articles=hot_articles,random=random,cutOffSentence=cutOffSentence,timeFormatConvert=timeFormatConvert,navigate=navigate,fashion_article=fashion_article)
