#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
import time,json
from main_index import alarm_schedule

global alarm  # 设置定时闹钟
alarm = 0

class Ccase(cgibase):
    def __init__(self):
        return cgibase.__init__(self)

    def onInit(self):
        cgibase.SetNoCheckCookie(self)
        opr = cgibase.onInit(self)
        if opr is None:
            return
        if not hasattr(self, opr):
            self.out = g_err["input_err"]
            return
        eval("self.%s()"%opr)

    # 通过id去查询用例,所需参数opr,id
    def casequery_by_id(self):
        self.log.debug("casequery_by_id in.")
        req = self.input["input"]
        # 用例id
        id = req["id"]
        case = Case().casequery_by_id(id=id)
        if case:
            self.out = {"status": 0, "data": case}
        else:
            self.out = {"status": 1}

    # 新增用例，所需参数opr,cmid,name,pid,pmodel,ip,url,method,type,data,check,desc,timing,rank,encrypt,user
    def caseadd(self):
        self.log.debug("caseadd in.")
        req = self.input["input"]
        # 用例是否套用模版
        cmid = req["cmid"]
        # 若cmid存在，则套用模版，获取用例相关信息
        if cmid:
            # 通过cmid查询模版
            cm = Case_model().cmqueryone(cmid)
            # 主机ip
            ip = cm["ip"]
            # 请求url
            url = cm["url"]
            # 请求方法
            method = cm["method"]
            # 请求类型
            type = cm["type"]
        else:
            # 主机ip
            ip = req["ip"]
            # 请求url
            url = req["url"]
            # 请求方法
            method = req["method"]
            # 请求类型
            type = req["type"]
        # 项目id
        pid = req["pid"]
        # 用例名称
        name = req["name"]
        # 用例所属模块
        pmodel = req["pmodel"]
        # 请求参数
        data = req["data"]
        if not isinstance(data,dict):
            self.out = {"status": 1, "msg": "data not dict"}
        else:
            # 检查点
            check = req["check"]
            # if not isinstance(check,dict):
            #     self.out = {"status": 1, "msg": "check not dict"}
            # elif not check.values()[0] and check.values()[0] != 0:
            #     self.out = {"status": 1, "msg": "check value none"}
            # else:
            # 用例说明
            desc = req["desc"]
            # 是否定时
            timing = req["timing"].upper()
            if "YES" == timing:  # 该语句用于定时调度做准备
                global alarm
                if alarm == 0:
                    alarm = 1  # 设置全局变量改变并且启动定时任务，这样以后有就不用判断了，也不会重复启动定时
                    alarm_schedule().input_one_time()  # 启动定时任务
            # 用例级别
            rank = req["rank"]
            # 是否加密
            encrypt = req["encrypt"].upper()
            # 最后编辑人员
            user = req["user"]
            # 最后编辑时间
            tim = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            # 新增成功则返回用例ID，失败返回空
            num = Case().caseadd(name=name,pid=pid,pmodel=pmodel,ip=ip,url=url,method=method,
                                 type=type,data=data,check=check,desc=desc,timing=timing,
                                 rank=rank,encrypt=encrypt,user=user,time=tim)
            if num:
                # 重新查询
                total = Case().casequery_total(pid=pid, pmodel=pmodel)
                list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                self.out = {"status":0, "total": total, "data": list0}
            else:
                self.out = {"status":1}

    # 查询指定项目指定模块下的用例列表，所需参数opr,pid,pmodel,page
    def casequery(self):
        self.log.debug("casequery in.")
        req = self.input["input"]
        # 项目id
        pid = req["pid"]
        # 模块名称
        pmodel = req["pmodel"]
        # 当前页码数,第一次查询是默认为0
        page = req["page"]
        # 每页显示条数
        limitnum = 8
        if page:
            # 数据库查询时跳过的条数
            skipnum = (int(page)-1) * limitnum
            list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=skipnum, limit_num=limitnum)
            self.out = {"data": list0}
        else:
            # 第一次查询，页码为0，查询总条数，用于前台分页
            total = Case().casequery_total(pid=pid, pmodel=pmodel)
            list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=limitnum)
            self.out = {"total": total, "data": list0}

        # # 用例列表
        # list = Case().casequery(pid=pid,pmodel=pmodel)
        # self.out = {"data": list}

    # 通过用例名称模糊查询指定项目指定模块下的用例列表，所需参数opr,pid,pmodel，name
    def casequery_by_name(self):
        self.log.debug("casequery_by_name in.")
        req = self.input["input"]
        # 项目id
        pid = req["pid"]
        # 模块名称
        pmodel = req["pmodel"]
        # 用例名称
        name = req["name"]
        # 每页显示条数
        limitnum = 8
        total = Case().casequery_total_by_name(pid=pid, pmodel=pmodel, name=name)
        list0 = Case().casequery_page_by_name(pid=pid, pmodel=pmodel, skip_num=0, limit_num=limitnum, name=name)
        self.out = {"total": total, "data": list0}

    # 编辑用例，所需参数opr,id,name,pid,pmodel,ip,url,pmethod,type,data,check,desc,timing,rank,encrypt,user,time
    def caseupdate(self):
        self.log.debug("caseupdate in.")
        req = self.input["input"]
        # 用例id
        id = req["id"]
        # 用例名称
        name = req["name"]
        # 项目id
        pid = req["pid"]
        # 主机ip
        ip = req["ip"]
        # 请求url
        url = req["url"]
        # 请求方法
        method = req["method"]
        # 请求类型
        type = req["type"]
        # 用例所属模块
        pmodel = req["pmodel"]
        # 请求参数
        data = req["data"]
        if not isinstance(data,dict):
            self.out = {"status": 1, "msg": "data not dict"}
        else:
            # 检查点
            check = req["check"]
            # if not isinstance(check,dict):
            #     self.out = {"status": 1, "msg": "check not dict"}
            # elif not check.values()[0]:
            #     self.out = {"status": 1, "msg": "check value none"}
            # else:
            # 用例说明
            desc = req["desc"]
            # 是否定时
            timing = req["timing"]
            # 用例级别
            rank = req["rank"]
            # 是否加密
            encrypt = req["encrypt"]
            # 最后编辑人员
            user = req["user"]
            # 最后编辑时间
            tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 返回true（更新成功）/false（更新失败）
            istrue = Case().caseupdate(id=id,name=name,pid=pid,pmodel=pmodel,ip=ip,url=url,
                                       method=method,type=type,data=data,check=check,desc=desc,
                                       timing=timing,rank=rank,encrypt=encrypt,user=user,time=tim)
            if istrue:
                # 重新查询
                total = Case().casequery_total(pid=pid, pmodel=pmodel)
                list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                self.out = {"status": 0, "total": total, "data": list0}
            else:
                self.out = {"status":1}

    # 删除用例,所需参数opr,id，pid,pmodel
    def casedelete(self):
        self.log.debug("casedelete in.")
        req = self.input["input"]
        # 用例id
        id = req["id"]
        # 项目id
        pid = req["pid"]
        # 模块名称
        pmodel = req["pmodel"]
        # 批量删除
        if isinstance(id, list):
            # 成功删除的个数
            total = 0
            # 循环删除
            for i in id:
                num = Case().casedelete(i)
                if num:
                    total += 1
            if total == len(id):
                # 重新查询
                total = Case().casequery_total(pid=pid, pmodel=pmodel)
                list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                self.out = {"status": 0, "total": total, "data": list0}
            else:
                self.out = {"status": 1}
        # 删除单个
        else:
            # 返回1（删除成功）/0（删除失败）
            num = Case().casedelete(id)
            if num:
                # 重新查询
                total = Case().casequery_total(pid=pid, pmodel=pmodel)
                list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                self.out = {"status": 0, "total": total, "data": list0}
            else:
                self.out = {"status": 1}

if __name__ == "__main__":
    pass