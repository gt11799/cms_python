#! /usr/bin/env python
#! -*- coding=utf8 -*-
'''
移除redis时的脚本
'''
import os,sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import *
from zixun.models import *



def deleteStatus():
    '''
    之前设置过delete status,现在移除
    '''
    db = DBAccess()
    db.dbName = 'zixun'

    for table in ['article','brand','catagory']:
        print db.execUpdateQuery("delete from %s where delete_status = 1"%table)


if __name__ == '__main__':
    deleteStatus()
