#coding:utf-8

# 添加用户，测试用
def insertUser(db,table,nrows):
    for i in range(1, nrows):
        Id = table.row_values(i)[1]
        user_name =  table.row_values(i)[2]
        obj = {"company_id":Id, "name":user_name}
        db.company.insert(obj)
    print "用户添加完毕"

# 用户添加组
def addGroup(db,table,nrows):
    collection = db.groups
    group_id=-1
    for i in range(1, nrows):
        group_name = table.row_values(i)[0]
        if group_name == "":
            group_name = "无"
        Id = table.row_values(i)[1]
        
        index = collection.find_one({"group_name":group_name})
        if index == None:
            group_id += 1
            collection.save({"group_id":group_id, "group_name": group_name})                         
        db.company.update({"company_id":Id},{"$set":{"group_id":group_id}}); 
    print "OK"

# 用户组添加权限，从指定用户copy权限
def addPermission(db,table,nrows):
    for i in range(nrows):
        group_name = table.row_values(i)[0]
        result1 = db.groups.find_one({"group_name":group_name},{"group_id":1})
        user_name = table.row_values(i)[1]
        result2 = db.company.find_one({"name":user_name},{"company_id":1})
        if result2==None:
            print "用户不存在", user_name
        else:
            company_id = result2["company_id"]
            permission = db.user_permission.find({"company_id":company_id})
            
            for per in permission:
                group_permission = {}
                group_permission["group_id"] = result1["group_id"]
                group_permission["url"] = per["url"]
                group_permission["get"] = per["get"]
                group_permission["post"] = per["post"]
                db.group_permission.save(group_permission)
        
    print "权限添加完毕"
    
if __name__ == "__main__":
    import xlrd 
    import pymongo
    import os
    import sys
    path = os.path.dirname(__file__)
    sys.path.append(os.path.join(path, ".."))
    from utility.utils import BasicTemplateHandler,getMongoDBConn
    
    data = xlrd.open_workbook('./1111.xls')
    table1 = data.sheet_by_name(u'个人')   
    nrows1 = table1.nrows #行数
    ncols1 = table1.ncols #列数
    print "个人：", nrows1,"行", ncols1,"列"
    
    table2 = data.sheet_by_name(u'组别')
    nrows2 = table2.nrows #行数
    ncols2 = table2.ncols #列数
    print "组别：", nrows2,"行", ncols2,"列"
   
    # connection = pymongo.Connection('localhost', 27017)
    db = getMongoDBConn().shop
    # insertUser(db,table1,nrows1);
    addGroup(db, table1, nrows1)
    addPermission(db,table2,nrows2)
