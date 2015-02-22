# coding:utf-8
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

from utility.utils import getMongoDBConn


#with open("cloth_type.txt", "r") as f:
#    h = f.readlines()

conn = getMongoDBConn()
db = conn.shop

'''
for t in h:
    if t.lstrip() == t:
        current_type = t.strip()
        db.cloth_type.insert({"type": current_type})
    elif t.strip() == "":
        pass
    else:
        db.cloth_type.update(
            {"type": current_type}, {"$addToSet": {"species": t.strip()}})
'''

s = '''
宝宝纪念品/个性产品
彩泥/手工制作/仿真/过家家玩具
电动/遥控/惯性/发条玩具
电子/发光/充气/整蛊玩具
儿童包/背包/箱包
高达/BJD/手办/机器人
户外运动/休闲/传统玩具
静态模型
聚会/魔术/cosplay用具
解锁/迷宫/魔方/悠悠球
积木/拆装/串珠/拼图/配对玩具
卡通/动漫/游戏周边
毛绒布艺类玩具
母婴线下服务
棋牌/桌面游戏
其它玩具
童车/儿童轮滑
娃娃/配件
玩具模型零件/工具/耗材/辅件
网游周边(实物)
学习/实验/绘画文具
游泳池/戏水玩具
游乐/教学设备/大型设施
幼儿响铃/布书手偶/爬行健身
油动电动模型
早教/音乐/智能玩具
'''

s = [ i.strip() for i  in s.splitlines() if i.strip() ]

for i in s:
    print i

# db.cloth_type.insert({"type":"包袋","species":['单肩包','斜挎包','手提包','手拿包','腰包','胸包','双肩包','化妆包']})

db.cloth_type.insert({"type":"玩具/模型/动漫/早教/益智","species":s})



