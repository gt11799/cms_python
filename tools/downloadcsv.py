#! /usr/bin/env python
# -*- coding=utf8 -*-
'''
每天生成固定的数据，保存到static/csv文件夹下
'''

import time
from io import BytesIO
import csv,os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from utility.mail import send_mail
from shop_admin.models import unicode2gbk
from shop_admin.models import getDeliveringGoodsCsv,getDeliveringGoodsCsvAddCancled



GOODS_CSV_MAIL_LIST = ['shafei@xiaoher.com','zuowan@xiaoher.com','xiaojun@xiaoher.com','dongxue@xiaoher.com','gongting@xiaoher.com','haifang@xiaoher.com',
                    'zhuting@xiaoher.com','yuqin@xiaoher.com']
PACKAGE_CSV_MAIL_LSIT = ['xiaochang@xiaoher.com','gongting@xiaoher.com','haifang@xiaoher.com']

END_TIME = datetime.datetime.today().strftime("%Y-%m-%d")
START_TIME = (datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d")
#END_TIME = "2014-11-27"
#START_TIME = "2014-11-25"

def downloadGoodsCSV():
    '''
    下载商品审核页面的CSV
    '''
    sql = """select og.deliver_no,og.package_id,og.deliver_time,og.deliver,og.sign_time,og.product_status,o.human_address as address,o.phone,o.receiver_name 
                    from order_goods as og, orders as o  where og.order_id = o.order_id and deliver_time > '%s' and deliver_time < '%s' 
                    """ %(START_TIME, END_TIME)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)

    exportCSV = getDeliveringGoodsCsv(result)
    exportPerDayCSV = getDeliveringGoodsCsvAddCancled(result)
    csv_path = generatePath(START_TIME + '_csv')
    perdaycsv_path = generatePath(START_TIME + '_perdaycsv')
    writeFile(csv_path,exportCSV)
    writeFile(perdaycsv_path,exportPerDayCSV)
    return

def generatePath(filename):
    return os.path.join(os.path.dirname(__file__), '../static/csv/%s.csv'%str(filename))

def generateDownloadURL():
    '''
    生成附件下载链接。目前是高耦合的，以后多了可以改
    '''
    url = "http://erp.xiaoher.com/static/csv/"
    url_dict = {}
    url_dict['csv'] = url + START_TIME + '_csv.csv'
    url_dict['perdaycsv'] = url + START_TIME + '_perdaycsv.csv'
    url_dict['packages'] = url + START_TIME + '_packages.csv'
    return url_dict

def perDaySendPackage():
    '''
    每个发货人每天发了几个包裹，生成CSV
    '''
    sql = "select packed_by,count(id) from package_flow where deliver_time > '%s' and deliver_time < '%s' group by packed_by" %(START_TIME,END_TIME)
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)

    output = BytesIO()
    writer = csv.writer(output)
    head_data = ["发货人","包裹数"]
    head_data = unicode2gbk(head_data)
    writer.writerow(head_data)
    for r in result:
        data = [r["packed_by"], r["count(id)"]]
        data = unicode2gbk(data)
        writer.writerow(data)
    file_path = generatePath(START_TIME + '_packages')
    writeFile(file_path,output.getvalue())
    return

def writeFile(file_path,output):
    with open(file_path,'wb') as f:
        f.write(output)
    return 
        

def generateRemarks():
    '''
    生成备注
    '''
    remarks = u'''
            备注：
            1.点击链接即可下载
            2.文件名称的日期是数据所在的日期，也就是说12-10收到邮件，文件是12-09的数据，文件名也是12-09_*.csv
            3.如果要下载历史文档，复制链接到浏览器，把日期改掉即可
            4.如果有其他每天都要下载的CSV，请知会开发组
            '''
    return remarks

def sendMail():
    '''
    发邮件，上班前执行
    '''
    subject = u"CSV下载".encode('utf8')
    url_dict = generateDownloadURL()
    remarks = generateRemarks()
    body = u'商品审核页面下载CSV： ' + url_dict['csv'] + u'\n'
    body += u'商品审核页面下载CSV（每日发单）：  ' + url_dict['perdaycsv'] + u'\n'
    body += u'\n\n\n' + remarks
    body = body.encode('utf8')
    send_mail(subject, body, GOODS_CSV_MAIL_LIST)
    #send_mail(subject,body,['gongting@xiaoher.com',])

    body = u'发货人发送包裹数统计CSV： ' + url_dict['packages'] + u'\n'
    body += u'\n\n\n' + remarks
    body = body.encode("utf8")
    send_mail(subject, body, PACKAGE_CSV_MAIL_LSIT)
    #send_mail(subject,body,['gongting@xiaoher.com',])


if __name__ == '__main__':
    downloadGoodsCSV()
    perDaySendPackage()
    sendMail()

    