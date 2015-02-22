#! /usr/bin/env python
# -*- coding=utf8 -*-
'''
gongting@xiaoher.com
查看退厂相关的log
'''
import os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.mail import send_mail
import datetime,re

END_TIME = datetime.datetime.today().strftime("%Y-%m-%d")
START_TIME = (datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d")

def analyseLog():
    '''
    筛选匹配相关的日志，发送邮件
    '''
    try:
        f = open('/root/log/debug_web.log','r')
    except:
        send_mail("open_wrong","open error log wrong",["gongting@xiaoher.com",])
    #f = open('../demo/test_log.txt','r')
    error_log = ''
    for line in f.readlines():
        items = line.split(' - ')
        if items[0] < END_TIME and items[0] > START_TIME and re.search(u'return_to_supplier_out',items[2]):
            error_log += (line)

    subject = u"return_to_supplier_out: error_log"
    body = error_log.encode('utf8')
    send_mail(subject,body,['gongting@xiaoher.com',])

    f = open('/root/log/debug_web.log','r')
    debug_log = ''
    for line in f.readlines():
        items = line.split(' - ')
        if items[0] < END_TIME and items[0] > START_TIME and re.search(u'return_to_supplier_out',items[2]):
            error_log += (line)

    subject = u"return_to_supplier_out: debug_log"
    body = debug_log.encode('utf8')
    send_mail(subject,body,['gongting@xiaoher.com',])

if __name__ == "__main__":
    analyseLog()