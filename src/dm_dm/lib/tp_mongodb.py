#!/usr/bin/env python
# -*- coding:utf-8 -*-

##
#连接数据库，以及与数据库的相关操作

import pymongo,json,time,hashlib,tablib,yaml
from bson.objectid import ObjectId

#连接数据库
def get_conn():
    client = pymongo.MongoClient('10.10.62.10', 27017)
    db = client.test
    return db

#与user表相关操作
class User(object):
    def __init__(self):
        self.db = get_conn().user    #user表操作游标

    #查询用户
    def find(self, name, pwd):
        user = self.db.find({"u_name":name,
                             "u_password":hashlib.md5(name+pwd).hexdigest()})
        for u in user:
            return u

    # 通过用户名得到邮箱地址
    def findemail(self, name):
        user = self.db.find({"u_name":name}, {"u_email":1})
        for u in user:
            # return u
            return u["u_email"]

    # 查询所有用户以及邮箱地址
    def find_name_email(self):
        # 查询所有用户以及邮箱地址
        name_email = self.db.find({},{"u_name":1,"u_email":1})
        # 返回的列表
        lsit = []
        for n in name_email:
            dict1 = {}
            # 用户名
            dict1["name"] = n["u_name"]
            # 邮箱
            dict1["email"] = n["u_email"]
            lsit.append(dict1)
        return lsit

    # 注册用户
    def useradd(self, name, pwd, email):
        # 验证此用户名是否存在
        num = User().check_name(name)
        # 存在返回空
        if num:
            return
        # 不存在则注册，并返回用户ID
        return self.db.insert({"u_name": name,
                               "u_password": hashlib.md5(name + pwd).hexdigest(),
                               "u_email": email})

    def check_name(self, name):
        # 验证此用户名是否存在
        user = self.db.find({"u_name": name})
        # 存在返回1
        for u in user:
            return 1

#与项目表相关操作
class Project(object):
    def __init__(self):
        self.db = get_conn().project

    # 新增项目
    def proadd(self, name, desc, user):
        # 验证此项目是否存在
        project = self.db.find({"p_name": name})
        # 存在返回空
        for p in project:
            return
        # 不存在则新增，并返回项目ID
        return self.db.insert({"p_name": name,
                               "p_desc": desc,
                               "p_user": user})

    # 查询项目id,名称
    def proquery_id_name(self):
        prolist = self.db.find({},{"_id": 1, "p_name": 1})
        # 返回的项目列表
        list = []
        # 遍历游标
        for pro in prolist:
            # 每个项目作为一个字典（列表元素）
            dict = {"id": str(pro["_id"]),
                    "name": pro["p_name"]}
            list.append(dict)
        return list

    # 查询单个项目说明
    def proquery_desc(self, id):
        id = ObjectId(id)
        prolist = self.db.find({"_id": id},{"p_desc": 1})
        # 遍历游标
        for pro in prolist:
            # 项目作为一个字典
            dict = {"desc": pro["p_desc"]}
            return dict

    # 查询项目创建人
    def proquery_user(self, id):
        id = ObjectId(id)
        prolist = self.db.find({"_id": id}, {"p_user": 1})
        # 遍历游标
        for pro in prolist:
            return pro["p_user"]

    # 编辑项目
    def proupdate(self, id, name, desc, user):
        id = ObjectId(id)
        # 得到更新操作的相关信息
        dict = self.db.update({"_id":id},
                              {"p_name":name,
                               "p_user":user,
                               "p_desc":desc})
        # 返回true（更新成功）/false（更新失败）
        return dict['updatedExisting']

    # 删除项目
    def prodelete(self, id):
        id = ObjectId(id)
        # 得到删除操作的相关信息
        dict = self.db.remove({"_id":id})
        # 返回1（删除成功）/0（删除失败）
        return dict['n']

    # 查询单个项目
    def proqueryone(self, id):
        # 得到项目Cursor
        project = self.db.find({"_id": id})
        # 返回查询得到的项目，没有则返回None
        for pro in project:
            return pro

# 与模块表相关操作
class Model(object):
    def __init__(self):
        self.db = get_conn().model

    # 查询单个项目的模块
    def modelquery(self, pid):
        pid = ObjectId(pid)
        modellist = self.db.find({"p_id": pid})
        lsit =[]
        # 遍历游标
        for model in modellist:
            # 项目作为一个字典
            dict = {"id":str(model["_id"]),
                    "name": model["name"]}
            lsit.append(dict)
        return lsit

    # 新增项目模块
    def addmodel(self, id, addmodel):
        id = ObjectId(id)
        model = self.db.find({"p_id": id, "name": addmodel})
        # 若模块已经存在，则直接空
        for m in model:
            return
        # 在数据库中新增,成功则返回id
        num = self.db.insert({"p_id": id, "name": addmodel})
        return num

    # 删除项目模块
    def deletemodel(self, id, deletemodel):
        id = ObjectId(id)
        # 得到删除操作的相关信息
        dict = self.db.remove({"p_id": id, "name": deletemodel})
        # 返回1（删除成功）/0（删除失败）
        return dict['n']

    # 删除项目所有模块
    def deletemodel_all(self, pid):
        pid = ObjectId(pid)
        # 得到删除操作的相关信息
        dict = self.db.remove({"p_id": pid})
        # 返回1（删除成功）/0（删除失败）
        return dict['n']



#与用例模版表相关操作
class Case_model(object):
    def __init__(self):
        self.db = get_conn().case_model

    # 查询某一项目的所有用例模版
    def cmquery(self, pid):
        pid = ObjectId(pid)
        cmlist = self.db.find({"cm_pid":pid})
        list = []
        # 遍历游标
        for cm in cmlist:
            # 每个模版作为一个字典（列表元素）
            dict = {"id": str(cm["_id"]),
                    "name": cm["cm_name"],
                    "ip": cm["cm_ip"],
                    "url": cm["cm_url"],
                    "method": cm["cm_method"],
                    "type": cm["cm_type"]
                    }
            list.append(dict)
        return list

        # 用例~导出

    def modelout(self, id):
        pid = ObjectId(id)
        modelist = self.db.find({"_id": pid})
        print modelist
        # 表格第一行
        # headers = ["模版编号", "模版名称", "主机IP", "请求URL", "请求方法", "请求类型"]
        # list = []
        for data in modelist:
            a = (str(data["_id"]), data["cm_name"], data["cm_ip"], data["cm_url"], data["cm_method"],
                 data["cm_type"])
            return a
            # list.append(a)
        # data = tablib.Dataset(*list, headers=headers)
        # print data
        # return data

    def modeloneout(self, id):
        pid = ObjectId(id)
        modelist = self.db.find({"_id": pid})
        print modelist
        # 表格第一行
        headers = ["模版编号", "模版名称", "主机IP", "请求URL", "请求方法", "请求类型"]
        list = []
        for data in modelist:
            a = (str(data["_id"]), data["cm_name"], data["cm_ip"], data["cm_url"], data["cm_method"],
                 data["cm_type"])
            list.append(a)
        data = tablib.Dataset(*list, headers=headers)
        return data

    def readcount(self):
        count = self.db.count()
        return count

    def modeladd(self, d):
        model = d
        num = self.db.insert(model)
        return num


    # 查询某一项目的所有用例模版的id和名称
    def cmquery_id_name(self, pid):
        pid = ObjectId(pid)
        cmlist = self.db.find({"cm_pid": pid}, {"_id": 1, "cm_name": 1})
        list = []
        # 遍历游标
        for cm in cmlist:
            # 每个模版作为一个字典（列表元素）
            dict = {"id": str(cm["_id"]),
                    "name": cm["cm_name"]
                    }
            list.append(dict)
        return list

    # 查询某一项目的用例模版总数
    def cmquery_total(self, pid):
        pid = ObjectId(pid)
        total = self.db.count({"cm_pid":pid})
        return total

    # 分页查询
    def cmquery_page(self, pid, skip_num, limit_num):
        pid = ObjectId(pid)
        cmlist = self.db.find({"cm_pid": pid}).skip(skip_num).limit(limit_num)
        list = []
        # 遍历游标
        for cm in cmlist:
            # 每个模版作为一个字典（列表元素）
            dict = {"id": str(cm["_id"]),
                    "name": cm["cm_name"],
                    "ip": cm["cm_ip"],
                    "url": cm["cm_url"],
                    "method": cm["cm_method"],
                    "type": cm["cm_type"]
                    }
            list.append(dict)
        return list

    # 模糊查询某一项目的用例模版总数
    def cmquery_total_by_name(self, pid, name):
        pid = ObjectId(pid)
        total = self.db.count({"cm_pid": pid, "cm_name": {"$regex": name, "$options": 'i'}})
        return total

    # 模糊查询
    def cmquery_page_by_name(self, pid, skip_num, limit_num, name):
        pid = ObjectId(pid)
        cmlist = self.db.find({"cm_pid": pid, "cm_name": {"$regex": name, "$options": 'i'}}).skip(skip_num).limit(limit_num)
        list = []
        # 遍历游标
        for cm in cmlist:
            # 每个模版作为一个字典（列表元素）
            dict = {"id": str(cm["_id"]),
                    "name": cm["cm_name"],
                    "ip": cm["cm_ip"],
                    "url": cm["cm_url"],
                    "method": cm["cm_method"],
                    "type": cm["cm_type"]
                    }
            list.append(dict)
        return list


    # 查询单个项目的所有模版id
    def cmquery_id(self, pid):
        pid = ObjectId(pid)
        cmlist = self.db.find({"cm_pid": pid}, {"_id": 1})
        list = []
        # 遍历游标
        for cm in cmlist:
            list.append(str(cm["_id"]))
        return list

    # 查询单个用例模版
    def cmqueryone(self, id):
        id = ObjectId(id)
        # 得到Cursor
        casemodel = self.db.find({"_id": id})
        # 返回查询得到的用例模版，没有则返回None
        for cm in casemodel:
            dict = {"id": str(cm["_id"]),
                    "name": cm["cm_name"],
                    "ip": cm["cm_ip"],
                    "url": cm["cm_url"],
                    "method": cm["cm_method"],
                    "type": cm["cm_type"]
                    }
            return dict

    # 新增用例模版
    def cmadd(self, name, pid, ip, url, method, type):
        pid = ObjectId(pid)
        # 验证此项目是否存在
        pro = Project().proqueryone(pid)
        # 项目存在
        if pro:
            # 验证此模版是否存在
            cm = self.db.find({"cm_name": name,"cm_pid":pid})
            # 存在返回空
            for c in cm:
                return
            # 不存在则新增，并返回模版ID
            return self.db.insert({"cm_name":name,
                                   "cm_pid":pid,
                                   "cm_ip":ip,
                                   "cm_url":url,
                                   "cm_method":method,
                                   "cm_type":type})
        else:
            return

    # 编辑用例模版
    def cmupdate(self, id, name, pid, ip, url, method, type):
        id = ObjectId(id)
        pid = ObjectId(pid)
        # 数据库更新模版，并返回更新信息
        dict = self.db.update({"_id":id},
                              {"cm_name":name,
                               "cm_pid":pid,
                               "cm_ip":ip,
                               "cm_url":url,
                               "cm_method":method,
                               "cm_type":type})
        # 返回true（更新成功）/false（更新失败）
        return dict['updatedExisting']

    # 删除用例模版
    def cmdelete(self, id):
        id = ObjectId(id)
        # 得到删除操作的相关信息
        dict = self.db.remove({"_id": id})
        # 返回1（删除成功）/0（删除失败）
        return dict['n']

#与用例表相关操作
class Case(object):
    def __init__(self):
        self.db = get_conn().case

    # 通过id去查询单个用例
    def casequery_by_id(self, id):
        id = ObjectId(id)
        # 得到Cursor
        case = self.db.find({"_id": id})
        for c in case:
            # 用例作为一个字典
            dict = {"id": str(c["_id"]),
                    "name": c["c_name"],
                    "pid": str(c["c_pid"]),
                    "pmodel": c["c_pmodel"],
                    "ip": c["c_ip"],
                    "url": c["c_url"],
                    "method": c["c_method"],
                    "type": c["c_type"],
                    "data": c["c_data"],
                    "check": c["c_check"],
                    "desc": c["c_desc"],
                    "timing": c["c_timing"],
                    "rank": c["c_rank"],
                    "encrypt": c["c_encrypt"]}
            return dict

    # 查询指定项目指定模块下的用例列表
    def casequery(self, pid, pmodel):
        pid = ObjectId(pid)
        caselist = self.db.find({"c_pid":pid, "c_pmodel":pmodel})
        # 需要返回的用例列表
        list = []
        # 遍历游标
        for case in caselist:
            # 每个用例作为一个字典（列表元素）
            dict = {"id": str(case["_id"]),
                    "name": case["c_name"],
                    "pid": str(case["c_pid"]),
                    "pmodel": case["c_pmodel"],
                    "ip":case["c_ip"],
                    "url":case["c_url"],
                    "method":case["c_method"],
                    "type":case["c_type"],
                    "data":case["c_data"],
                    "check":case["c_check"],
                    "desc":case["c_desc"],
                    "timing":case["c_timing"],
                    "rank":case["c_rank"],
                    "encrypt":case["c_encrypt"],
                    "user":case["c_user"],
                    "time":case["c_time"]}
            list.append(dict)
        return list

    # 查询项目某一模块的用例模版总数
    def casequery_total(self, pid, pmodel):
        pid = ObjectId(pid)
        total = self.db.count({"c_pid": pid, "c_pmodel": pmodel})
        return total

    # 分页查询
    def casequery_page(self, pid, pmodel, skip_num, limit_num):
        pid = ObjectId(pid)
        caselist = self.db.find({"c_pid": pid, "c_pmodel": pmodel}).skip(skip_num).limit(limit_num)
        list = []
        # 遍历游标
        for case in caselist:
            # 每个用例作为一个字典（列表元素）
            dict = {"id": str(case["_id"]),
                    "name": case["c_name"],
                    "pid": str(case["c_pid"]),
                    "pmodel": case["c_pmodel"],
                    "ip": case["c_ip"],
                    "url": case["c_url"],
                    "method": case["c_method"],
                    "type": case["c_type"],
                    "data": case["c_data"],
                    "check": case["c_check"],
                    "desc": case["c_desc"],
                    "timing": case["c_timing"],
                    "rank": case["c_rank"],
                    "encrypt": case["c_encrypt"],
                    "user": case["c_user"],
                    "time": case["c_time"]}
            list.append(dict)
        return list

    # 模糊查询项目某一模块的用例模版总数
    def casequery_total_by_name(self, pid, pmodel, name):
        pid = ObjectId(pid)
        total = self.db.count({"c_pid": pid, "c_pmodel": pmodel, "c_name": {"$regex": name, "$options": 'i'}})
        return total

    # 模糊查询
    def casequery_page_by_name(self, pid, pmodel, skip_num, limit_num, name):
        pid = ObjectId(pid)
        caselist = self.db.find({"c_pid": pid, "c_pmodel": pmodel, "c_name": {"$regex": name, "$options": 'i'}}).skip(skip_num).limit(limit_num)
        list = []
        # 遍历游标
        for case in caselist:
            # 每个用例作为一个字典（列表元素）
            dict = {"id": str(case["_id"]),
                    "name": case["c_name"],
                    "pid": str(case["c_pid"]),
                    "pmodel": case["c_pmodel"],
                    "ip": case["c_ip"],
                    "url": case["c_url"],
                    "method": case["c_method"],
                    "type": case["c_type"],
                    "data": case["c_data"],
                    "check": case["c_check"],
                    "desc": case["c_desc"],
                    "timing": case["c_timing"],
                    "rank": case["c_rank"],
                    "encrypt": case["c_encrypt"],
                    "user": case["c_user"],
                    "time": case["c_time"]}
            list.append(dict)
        return list

    # 查询单个项目的所有用例id
    def casequery_pro_id(self, pid):
        pid = ObjectId(pid)
        caselist = self.db.find({"c_pid": pid}, {"_id": 1})
        list = []
        # 遍历游标
        for cm in caselist:
            list.append(str(cm["_id"]))
        return list

    # 查询单个项目的下某一模块的所有用例id
    def casequery_model_id(self, pid, pmodel):
        pid = ObjectId(pid)
        caselist = self.db.find({"c_pid": pid, "c_pmodel": pmodel}, {"_id": 1})
        list = []
        # 遍历游标
        for cm in caselist:
            list.append(str(cm["_id"]))
        return list

    # 在指定项目指定模块下新增用例
    def caseadd(self, name, pid, pmodel, ip, url, method, type,
                data, check, desc, timing, rank, encrypt, user, time):
        pid = ObjectId(pid)
        # 查询指定项目指定模块是否存在相同的用例名称
        case = self.db.find({"c_name":name,"c_pid":pid,"c_pmodel":pmodel})
        # 若存在则返回空
        for c in case:
            return
        # 不存在新增用例，并返回用例ID
        num = self.db.insert({"c_name":name,
                    "c_pid":pid,
                    "c_pmodel":pmodel,
                    "c_ip":ip,
                    "c_url":url,
                    "c_method":method,
                    "c_type":type,
                    "c_data":data,
                    "c_check":check,
                    "c_desc":desc,
                    "c_timing":timing,
                    "c_rank":rank,
                    "c_encrypt":encrypt,
                    "c_user":user,
                    "c_time":time})
        return num

    # 编辑用例
    def caseupdate(self, id, name, pid, pmodel, ip, url, method, type,
                   data, check, desc, timing, rank, encrypt, user, time):
        id = ObjectId(id)
        pid = ObjectId(pid)
        dict = self.db.update({"_id":id},
                       {"c_name": name,
                        "c_pid": pid,
                        "c_pmodel": pmodel,
                        "c_ip": ip,
                        "c_url": url,
                        "c_method": method,
                        "c_type": type,
                        "c_data": data,
                        "c_check": check,
                        "c_desc": desc,
                        "c_timing": timing,
                        "c_rank": rank,
                        "c_encrypt": encrypt,
                        "c_user": user,
                        "c_time": time}
                       )
        # 返回true（更新成功）/false（更新失败）
        return dict['updatedExisting']

    # 删除用例
    def casedelete(self, id):
        id= ObjectId(id)
        # 得到删除操作的相关信息
        dict = self.db.remove({"_id": id})
        # 返回1（删除成功）/0（删除失败）
        return dict['n']

    # 用例~导出
    def caseoneout(self, id):
        id = ObjectId(id)
        caselist = self.db.find({"_id": id})
        # 表格第一行
        headers = ["用例编号", "请求参数", "用例名称", "检查点", "请求URL", "是否开始定时任务",
                   "主机IP", "用例所属模块", "请求类型", "用例最后编辑人员", "用例说明", "用例编辑时间",
                   "请求方法", "用例是否加密", "用例级别", "用例所属项目编号"]

        list = []
        for data in caselist:
            a = (str(data["_id"]), data["c_data"], data["c_name"], data["c_check"], data["c_url"],
                 data["c_timing"], data["c_ip"], data["c_pmodel"], data["c_type"], data["c_user"],
                 data["c_desc"], data["c_time"], data["c_method"], data["c_encrypt"], data["c_rank"],
                 str(data["c_pid"]))
            list.append(a)
        data = tablib.Dataset(*list, headers=headers)
        return data

    def caseout(self, id):
        pid = ObjectId(id)
        caselist = self.db.find({"_id": pid})
        for data in caselist:
            a = (str(data["_id"]), data["c_data"], data["c_name"], data["c_check"], data["c_url"],
                 data["c_timing"], data["c_ip"], data["c_pmodel"], data["c_type"], data["c_user"],
                 data["c_desc"], data["c_time"], data["c_method"], data["c_encrypt"], data["c_rank"],
                 str(data["c_pid"]))
            return a



    def readcount(self):
        count = self.db.count()
        return count


    def readoneadd(self, d):
        case = d
        num = self.db.insert(case)
        return num

# 与结果表相关操作
class Result(object):
    def __init__(self):
        self.db = get_conn().result

    # 添加测试结果
    def execute(self,name,pid,cid,user,time,result,desc):
        pid = ObjectId(pid)
        cid = ObjectId(cid)
        # 添加测试结果，并返回id
        num = self.db.insert({"r_name": name,
                              "r_pid": pid,
                              "r_cid": cid,
                              "r_user": user,
                              "r_time": time,
                              "r_result": result,
                              "r_desc": desc})
        return num

    # 查询指定项目用例整体执行情况
    def proresult(self,pid):
        pid = ObjectId(pid)
        # 通过项目id查询项目所有的用例
        list = get_conn().case.find({"c_pid": pid}, {"_id": 1})
        # 测试成功的用例数
        suc_num = 0
        # 测试失败的用例数
        fail_num = 0
        # 对用例列表进行遍历
        for case in list:
            # 得到某一用例最新一次的测试结果
            resultone = self.db.find({"r_cid": case["_id"]},{"r_result": 1}).limit(1).sort([("_id",-1)])
            for r in resultone:
                # 测试结果成功
                if r["r_result"] == 100:
                    suc_num += 1
                # 失败
                else:
                    fail_num += 1
        # 返回项目用例整体执行情况
        return {"suc_num": suc_num, "fail_num": fail_num}

    # 查询某个用例历史执行情况
    def caseresult(self,cid):
        cid = ObjectId(cid)
        # 查询最后测试的5条记录
        result_list = self.db.find({"r_cid": cid}).limit(5).sort([("_id", -1)])
        # 返回的记录列表
        list = []
        for r in result_list:
            # 取值并添加到列表中
            dict = {"name": r["r_name"],
                    "result": r["r_result"],
                    "desc": r["r_desc"],
                    "user": r["r_user"],
                    "time": r["r_time"]}
            list.append(dict)
        return list

# 设置定时执行的时间
class Timing(object):
    def __init__(self):
        self.db = get_conn().timing

    # 设置定时执行的时间
    def setting(self, timing):
        dict = self.db.update({"_id": ObjectId("58fab871cf75c6f671464991")},
                              {"time": timing})
        # 返回true（更新成功）/false（更新失败）
        return dict['updatedExisting']

# 收件人邮箱表
class To_email(object):
    def __init__(self):
        self.db = get_conn().to_email

    # 设置收件人
    def add_email(self,user,to_email):
        dict = self.db.update({"user": user}, {"user": user, "to_email": to_email}, True)
        # 返回操作的条数1（成功）/0（失败）
        return dict['n']

    # 查询收件人邮箱地址
    def find_email(self,user):
        email = self.db.find({"user": user}, {"to_email": 1})
        for e in email:
            return e["to_email"]


if __name__ == '__main__':
    a = To_email().find_email("liujl")
    if a:
        print 1
    else:
        print 0