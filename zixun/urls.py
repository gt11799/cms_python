#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import *

urls = [
            (r"/zixun/admin/?",AdminHandler),
            (r"/zixun/admin/catagory_list/?", CatagoryListHandler),
            (r"/zixun/admin/add_catagory/?",AddCatagoryHandler),
            (r"/zixun/admin/edit_catagory/?",EditCatagoryHandler),

            (r"/zixun/admin/edit_article/?", EditArticleHandler),
            (r"/zixun/admin/add_article/?", AddArticleHandler),
            (r"/zixun/admin/article_list/?",ArticleListHandler),

            (r"/zixun/admin/edit_tag/?", EditTagHandler),
            (r"/zixun/admin/add_tag/?", AddTagHandler),
            (r"/zixun/admin/tag_list/?",TagListHandler),
            (r"/zixun/admin/tags/?",GetTagJsonHandler),

            (r"/zixun/admin/add_dapei/?",AddCollocationArticleHandler),
            (r"/zixun/admin/edit_dapei/?",EditCollocationArticleHandler),

            (r"/zixun/admin/edit_brand/?", EditBrandHandler),
            (r"/zixun/admin/add_brand/?", AddBrandHandler),
            (r"/zixun/admin/brand_list/?",BrandListHandler),

            (r"/zixun/admin/edit_index/?",EditIndexHandler),

            (r"/zixun/admin/delete/?",DeleteHandler),

            (r"/zixun/upload_image/?",UploadImageHandler),

            (r"/zixun/?",IndexHandler),
            (r"/zixun/fzdp(/[a-zA-Z]+[0-9]*){0,1}(/[0-9]+){0,1}/?",CollocationCatagoryHandler),
            (r"/pinpai/([a-zA-Z0-9]+)/?",BrandHandler),
            (r"/label/([a-zA-Z0-9]+)/?",TagHandler),
            (r"/zixun/([a-zA-Z0-9]+)(/[a-zA-Z]+[0-9]*){0,1}(/[0-9]+){0,1}/?",CatagoryHandler),


        ]

'''
        在资讯项目中有两个错误：
        1.category被我写成了catagory，在数据库、网页、脚本中都是
        2.redis的介入过早，因此MySQL和Redis有很高的耦合性，因此修改和删除尽可能使用models中的函数

        Redis中存储的数据：
        1. catagory_url_all:{url1,url2}, 用来存放目录生成的所有url
        2. tag_url_all:{url1,url2}, 用来存放所有的标签的url
        3. brand_url_all:{url1,url2}, 用来存放所有的品牌的url
        4. caragory_name_id: {name1:id1,name2:id2}, 是使用目录名得到目录ID的速查表
        5. tag_name_id: {name1:id1, name2:id2}, 是使用标签名得到ID的速查表
        6. brand_name_id: {name1:id1, name2:id2}, 是使用品牌名得到ID的速查表
        7. hot_tag_%catagory_id: [tag_name&tag_url, tag_name], 热门标签的缓存
        8. hot_brand_%catagory_id: [brand_name&brand_url, brand_name&brand_url], 热门品牌的缓存
        9. hot_article_%catagory_id: [article_title&article_id, article_title&article_id], 最热文章的缓存
        10. latest_article_%catagory_id: [article_title&article_id, article_title&article_id], 最新文章的缓存
        11. click_time_article_%id: 1234, 文章的点击次数
        12. click_time_tag_%id: 1234, 标签的点击次数
        13. click_time_brand_%id: 1234, 品牌的点击次数
'''