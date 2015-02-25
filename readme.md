###在资讯项目中有两个错误：
1. category被我写成了catagory，在数据库、网页、脚本中都是
2. redis的介入过早，因此MySQL和Redis有很高的耦合性，因此修改和删除尽可能使用models中的函数
3. 不知道有json如此神器，存入redis中的内容都是用&分隔开的

###Redis中存储的数据：
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


运行前：

* 依照zixun.sql的结构新建数据库
* 在根目录下新建一个settings.py
  
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-

        # coding: utf-8

        import os
        from tornado.options import define,options

        from unchange_settings import *
* 在setting或者unchange_settings中修改七牛和数据库、redis的信息