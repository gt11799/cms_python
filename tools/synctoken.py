# coding:utf-8

import os
import sys
import json

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from utility.utils import getRedisObj

dump_json = "/root/dump.json"

with open(dump_json) as f:
    j = f.read()

j = json.loads(j)

r = getRedisObj(rdb=1)

for key,value in j[1].items():
    r.set(key,value)
    print "%s %s"%(key,value)