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
    
    from settings import setClient,getClient
    
    setClient("web")

    dirs = os.listdir(".")
    urls = []
    for d in dirs:
        if os.path.exists("%s/urls.py" % d):
            try:
                exec("from %s.urls import urls as temp_urls" % d)
                urls.extend(temp_urls)
                logging.info("import %s urls ok..........." % d)
            except:
                logging.error(traceback.format_exc())
                logging.error("import %s urls fail!!!!!!!!!!" % d)

    from utility.utils import BasicTemplateHandler

    class NotFoundHandler(BasicTemplateHandler):
        def get(self):
            self.render("error/404.html")

    urls.extend([(r".*",NotFoundHandler)])# append 404
    
    from settings import settings
    application = tornado.web.Application(urls, **settings)
    global server
    server = tornado.httpserver.HTTPServer(application,xheaders=True)
    server.listen(port,address="0.0.0.0")

    tornado.ioloop.IOLoop.instance().start()
 
    logging.info("Exit...")


if __name__ == "__main__":
    main(int(sys.argv[1]))
