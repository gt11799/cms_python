# coding:utf-8
import os
import sys
print "hello,window"
import datetime
import time
path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))

# from orders.models import insertOrdersGoods
# from orders.models import getAddressInfo,getHumanAddress
import simplejson

from utility.utils import DBAccess,getMongoDBConn,getNowUTCtime,getRedisObj
'''
====================================================================
TESTING CODE
====================================================================
'''
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

users1 = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Blues Traveler": 3.5, "Broken Bells": 2.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }



def getXHRating():
    f = open("colla_output")
    line = f.readline()
    rating = {}
    while line:
        parts = line.split("_")

        if len(parts)<=1:
            line = f.readline()
            continue
        uid = parts[0]
        dna = {}
        for i in xrange(1,len(parts)):
            item = parts[i]
            subParts = item.split(":")
            if subParts[0] == "":
                continue
            dna[unicode(subParts[0].strip())]= float(subParts[1])
        rating[uid] = dna
        line = f.readline()
    return rating
    pass


def manhattan(rate1,rate2):
    distance = 0 
    commonRating = 0
    for key in rate1:
        if key in rate2:
            distance+= abs(rate1[key] - rate2[key])
            commonRating = True
    if commonRating:
        return distance
    else:
        return -1


def computeNearestNeighbor(username,users):
    distances = []
    for key in users:
        if len(users[key]) <= 1:
            continue
        if key<>username:
            distance = pearson(users[username],users[key])
            distances.append((distance,key))
    distances.sort(reverse = True)
    return distances


from math import sqrt

def pearson(rate1,rate2):
    sum_xy = 0
    sum_x=0
    sum_y=0
    sum_x2=0
    sum_y2=0
    n=0
    for key in rate1:
        if key in rate2:
            n+=1
            x=rate1[key]
            y=rate2[key]
            sum_xy += x*y
            sum_x +=x
            sum_y +=y
            sum_x2 +=x*x
            sum_y2 +=y*y
    #计算距离
    if n==0:
        return 0
    else:
        sx=sqrt(sum_x2-(pow(sum_x,2)/n))
        sy=sqrt(sum_y2-(pow(sum_y,2)/n))
        if sx<>0 and sy<>0:
            denominator=(sum_xy-sum_x*sum_y/n)/sx/sy
        else:
            denominator=0
    return denominator


def minkowski(rate1,rate2,r):
    distance = 0
    commonRating = False
    for key in rate1:
        if key in rate2:
            distance += pow(abs(rate1[key] - rate2[key]),r)
            commonRating = True
    if commonRating:
        return pow(distance,1/r)
    else:
        return -1
    pass


'''
推荐最相似用户中，本用户没用过的评分最高的商品
'''
def recommend(username,users):
    nearest = computeNearestNeighbor(username,users)[0][1]
    recommendations = []
    neighborRatings = users[nearest]

    for key in neighborRatings:
        if not key in users[username]:
            recommendations.append((key,neighborRatings[key]))

    recommendations.sort(key = lambda rat:rat[1],reverse = True)
    return recommendations


def batchQueryGoodsType(goodsIds):
    conn = getMongoDBConn()
    db = conn.shop
    result = {}
    for item in goodsIds:
        print item
        if item == "":
            continue 
        goods = db.activity_goods.find_one({"_id" : int(item)})
        if goods is None:
            continue
        goodsDNA = {}
        goodsDNA["species"] = goods["species"]
        goodsDNA["goods_type"] = goods["goods_type"]
        goodsDNA["sell_point"] = goods["sell_point"]
        result[item] = goodsDNA
    return result


def getAllUserRating():
    sql = "select uid,product_ids from orders"
    db = DBAccess()
    db.dbName = "billing_record_db"
    result = db.execQueryAssoc(sql)

    unmegredResult = []
    for item in result:
        if "product_ids" not in item or item["product_ids"] is None:
            continue
        goodsIds = item['product_ids'].split("_")
        unmegredResult.append((item['uid'],batchQueryGoodsType(goodsIds)))


    mergedResult = {}
    for item in unmegredResult:
        uid = item[0]
        uidDNAs = item[1]
        if uid not in mergedResult:
            uidRating = {}
        else:
            uidRating = mergedResult[uid]

        for goodsId in uidDNAs:
            goodsDNA = uidDNAs[goodsId]
            goodType = goodsDNA["goods_type"]

            if goodType.strip() == "":
                continue

            if goodType in uidRating:
                uidRating[goodType] = uidRating[goodType] + 1
            else:
                uidRating[goodType] = 1

        if len(uidRating) >= 1:
            mergedResult[str(uid)] = uidRating

    '''
    f = open("colla_output","a+")
    for uid in mergedResult:
        f.write(str(uid))
        for key in mergedResult[uid]:
            
            f.write("_%s:%s" % (key,str(mergedResult[uid][key])))
        f.write("\r\n")
    f.close()
    '''

    r = getRedisObj()
    r.set("user_goods_rating",simplejson.dumps(mergedResult))
    print mergedResult

def cosine(rate1,rate2):
    sum_xy = 0
    sum_x=0
    sum_y=0
    n=0 
    for key in rate1:
        if key in rate2:
            n+=1
            x=rate1[key]
            y=rate2[key]
            sum_xy += x*y
            sum_x +=x*x
            sum_y +=y*y
    #计算距离
    if n==0:
        return 0
    else:
        sx=pow(sum_x,1/2)
        sy=pow(sum_y,1/2)
        if sum_xy<>0:
            denominator=sx*sy/sum_xy
        else:
            denominator=0
    return denominator

if __name__ == "__main__":
    
    print manhattan(users['Hailey'],users['Veronica'])
    print computeNearestNeighbor("Hailey",users)
    
    import sys
    reload(sys)
    '''
    sys.setdefaultencoding('utf-8')
    #getAllUserRating()
    rating = getXHRating()
    r = getRedisObj()
    r.set("user_goods_rating",simplejson.dumps(rating))
  
    print computeNearestNeighbor("393351",rating)
    print rating["394165"]
    print rating["130533"]
    print manhattan(rating["394165"],rating["130533"])
    #print computeNearestNeighbor("394165",rating)
    print rating["393351"]
    print rating["262369"]
    print pearson(rating["393351"],rating["262369"])
    print cosine(rating["393351"],rating["262369"])

    print cosine(users1['Angelica'],users1['Jordyn'])
    print recommend("393351",rating)
    '''
    getAllUserRating()

