#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import *

urls = [
            (r"/admin/?",AdminHandler),
            (r"/admin/catagory_list/?", CatagoryListHandler),
            (r"/admin/add_catagory/?",AddCatagoryHandler),
            (r"/admin/edit_catagory/?",EditCatagoryHandler),

            (r"/admin/edit_article/?", EditArticleHandler),
            (r"/admin/add_article/?", AddArticleHandler),
            (r"/admin/article_list/?",ArticleListHandler),

            (r"/admin/edit_tag/?", EditTagHandler),
            (r"/admin/add_tag/?", AddTagHandler),
            (r"/admin/tag_list/?",TagListHandler),
            (r"/admin/tags/?",GetTagJsonHandler),

            (r"/admin/add_dapei/?",AddCollocationArticleHandler),
            (r"/admin/edit_dapei/?",EditCollocationArticleHandler),

            (r"/admin/edit_brand/?", EditBrandHandler),
            (r"/admin/add_brand/?", AddBrandHandler),
            (r"/admin/brand_list/?",BrandListHandler),

            (r"/admin/edit_index/?",EditIndexHandler),

            (r"/admin/delete/?",DeleteHandler),

            (r"/upload_image/?",UploadImageHandler),

            (r"/fzdp(/[a-zA-Z]+[0-9]*){0,1}(/[0-9]+){0,1}/?",CollocationCatagoryHandler),
            (r"/pinpai/([a-zA-Z0-9]+)/?",BrandHandler),
            (r"/label/([a-zA-Z0-9]+)/?",TagHandler),
            (r"/?",IndexHandler),
            (r"/([a-zA-Z0-9]+)(/[a-zA-Z]+[0-9]*){0,1}(/[0-9]+){0,1}/?",CatagoryHandler),

        ]

