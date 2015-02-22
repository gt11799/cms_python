#!/usr/bin/env python
#coding:utf-8

import os
import sys
import urllib2
import urllib
import traceback

# brand_name = os.path.split(os.path.abspath(os.path.pardir))[-1]

# brand_name = os.path.split(os.getcwd())[-1]


# query = urllib.urlencode({"name":brand_name})

# query_url = "http://localhost:8000/upload/query/brand/?%s"%query


# try:
#     res = urllib2.urlopen(query_url).read()
#     brand_id = int(res)
#     if brand_id < 0:
#         open("error.txt",'wb').write('brand name not found')
#         sys.exit()
# except Exception:
#     print traceback.format_exc()
#     open("error.txt",'wb').write('query error')
#     sys.exit()


currentPath = os.getcwd()

files = os.listdir(currentPath)


allPath = os.path.join(currentPath,"all_image")

if not  os.path.exists(allPath):
    os.mkdir(allPath)

for i in files:
    if i == "all_image":
        continue
    filePath = os.path.join(currentPath,i)
    if os.path.isdir(os.path.join(currentPath,i)):
        print i
        for j in os.listdir(filePath):
            if j.startswith("."):
                continue
            imagePath = os.path.join(filePath,j)
            if os.path.isfile(imagePath):
                if "_" in j:
                    j = j.replace("_",'')
                # with open(os.path.join(allPath,"%s_%s_%s"%(brand_id,i,j)),"wb") as f1:
                with open(os.path.join(allPath,"%s_%s"%(i,j)),"wb") as f1:
                    with open(imagePath,'rb') as f2:
                        f1.write(f2.read())

