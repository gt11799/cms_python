#coding:utf-8

import os
import sys

def countWeb(logpath="/root/log/shop_web.log",tail_num=20000):

    CMD = "tail -n " + str(tail_num) + " " + logpath + "| grep ^INFO | awk '{print $5,$3}' "

    print CMD
    f = os.popen(CMD)

    request_count  = {}
    request_time = {}
    avg_time = {}

    for line in f:
        try:
            t,url = line.split()
            t = t.replace('ms','')
            url = url.split('?')[0]
            #print url
            #if url.endswith('/'): 
            #    url = url.rstrip('/')
            t = float(t)
        except:
            continue
        
        if url.startswith("/admin") or url.startswith("/company"):
            continue 
    
        if url == "/" or url.startswith("/?") or url.startswith("/yaoqing") or url.startswith("/#"):
            url = "/"
    
        elif url.startswith("/show"):
            url = "/show"
    
        elif url.startswith("/detail"):
            url = "/detail"
    
        elif url.startswith("/qudao"):
            url = "/qudao"
    
        elif url.startswith("/alipay_pc_callback"):
            url = "/alipay_pc_callback"

        elif url.startswith("/brand"):
            url = "/brand"
    
        else:
            pass
        
        
        count = request_count.get(url,0)
        count += 1
        spend = request_time.get(url,0)
        spend += t
    
        request_count[url] = count
        request_time[url] = spend
        avg_time[url] = spend/count
    
    return request_count,request_time,avg_time
    

def getCountLog(count_dict,time_dict,avg_dict,top=30):
    # count_dict,time_dict,avg_dict
    t1 =  sorted(count_dict.iteritems(), key=lambda d:d[1], reverse = True)
    t2 =  sorted(time_dict.iteritems(), key=lambda d:d[1], reverse = True)
    t3 =  sorted(avg_dict.iteritems(), key=lambda d:d[1], reverse = True)
    count_list = []
    time_list = []
    avg_list = []
    print "#################url######count########spend######avg 请求量"
    for i in t1:
        url = i[0]
        print url,i[1],count_dict[url],time_dict[url],avg_dict[url] 
        count_list.append((url,i[1],count_dict[url],time_dict[url],avg_dict[url]))
        if len(count_list) >= top:
            break 
    
    print "#################url######count########spend######avg 总时间"
    for i in t2:
        url = i[0]
        print url,i[1],count_dict[url],time_dict[url],avg_dict[url] 
        time_list.append((url,i[1],count_dict[url],time_dict[url],avg_dict[url]))
        if len(time_list) >= top:
            break 

    print "#################url######count########spend######avg 平均时间"
    for i in t3:
        url = i[0]
        print url,i[1],count_dict[url],time_dict[url],avg_dict[url] 
        avg_list.append((url,i[1],count_dict[url],time_dict[url],avg_dict[url]))
        if len(avg_list) >= top:
            break

    return count_list,time_list,avg_list 

if __name__ == "__main__":
    getCountLog(*countWeb(logpath="/home/lovedboy/you1hui/tools/shop.log"))
