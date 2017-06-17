### 在资讯项目中有个错误：

`category`被我写成了`catagory`，在数据库、网页、脚本中都是



#### 运行前：

* 依照zixun.sql的结构新建数据库
* 在根目录下新建一个settings.py
  
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-

        # coding: utf-8

        import os
        from tornado.options import define,options

        from unchange_settings import *
        
* 在setting或者unchange_settings中修改七牛和数据库的信息
