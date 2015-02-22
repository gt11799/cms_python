#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# coding: utf-8

import tornado.ioloop
import tornado.template
import tornado.httpserver
# from settings import *
import tornado.wsgi
# 添加一个app中函数必须步骤 ,such as images_app
import images_app
from images_app.views import *
import sys
import os
import traceback
import logging
import signal
import time

from settings import MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)
 
def shutdown():
    logging.info('Stopping http server')
    server.stop()
 
    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
 
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
 
    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()

def main(port):
    
    from settings import setClient,setMessageChannel,getClient
    
    if port >= 8880:
        setClient("web")
    elif port <=6000:
        setClient("3g")
    else:
        setClient("wap")

    dirs = os.listdir(".")
    urls = []
    for d in dirs:
        if os.path.exists("%s/urls.py" % d):
            try:
                if port <= 6000 and os.path.exists("%s/jisu_urls.py" %d ):
                    exec("from %s.jisu_urls import urls as temp_urls" % d)
                    urls.extend(temp_urls)
                    logging.info("import %s jisu urls ok..........." % d)
                else:
                    exec("from %s.urls import urls as temp_urls" % d)
                    urls.extend(temp_urls)
                    logging.info("import %s urls ok..........." % d)
            except:
                logging.error(traceback.format_exc())
                logging.error("import %s urls fail!!!!!!!!!!" % d)

    from utility.utils import BasicTemplateHandler,getMongoDBConn
    db = getMongoDBConn().shop

    class NotFoundHandler(BasicTemplateHandler):
        def get(self):
            self.render("error/404.html")

    urls.extend([(r".*",NotFoundHandler)])# append 404

    for t in urls:
        url = t[0].rstrip("/?")
        if url.startswith("/admin/"):
            doc = t[1].__doc__ and t[1].__doc__.strip() or ""
            # print url,doc
            # add "tag" column by cyf 2015-01-16
            tag = ""
            if doc.find(':') >= 0:
                tag = doc.split(':')[0]
            elif doc.find('：') >= 0:
                tag = doc.split('：')[0]
            elif (len(doc)>0 and len(doc)<=21):
                tag = doc
            else:
                tag = "未分类"
            db.permission.update({"url":url},{"$set":{"doc":doc,"tag":tag}},upsert=True)
            #db.permission.update({"url":url},{"$set":{"doc":doc}},upsert=True)
    
    print "Client:",getClient()
    from settings import settings
    application = tornado.web.Application(urls, **settings)
    global server
    server = tornado.httpserver.HTTPServer(application,xheaders=True)
    server.listen(port,address="0.0.0.0")

    # signal.signal(signal.SIGTERM, sig_handler)
    # signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().start()
 
    logging.info("Exit...")


if __name__ == "__main__":
    main(int(sys.argv[1]))
