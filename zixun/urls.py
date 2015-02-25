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
            (r"/?",IndexHandler),
            (r"/([a-zA-Z0-9]+)(/[a-zA-Z]+[0-9]*){0,1}(/[0-9]+){0,1}/?",CatagoryHandler),

        ]

