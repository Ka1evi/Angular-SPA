#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
import json
import requests

class Ccase_model(cgibase):
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

    # 新增模版，所需参数opr,name, pid, ip, url, method, type
    def cmadd(self):
        self.log.debug("cmadd in.")
        req = self.input["input"]
        # 模版名
        name = req["name"]
        # 模版所属项目id
        pid = req["pid"]
        # API主机
        ip = req["ip"]
        # 请求url
        url = req["url"]
        # 请求方法
        method = req["method"]
        # 请求类型
        type = req["type"]
        # 新增成功则返回模版ID，失败返回空
        num = Case_model().cmadd(name=name, pid=pid, ip=ip, url=url,
                                 method=method, type=type)
        if num:
            # 重新查询
            total = Case_model().cmquery_total(pid=pid)
            list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
            self.out = {"status": 0, "total": total, "data": list0}
        else:
            self.out = {"status":1}


    # 查询指定项目模版列表，所需参数opr,pid,page
    def cmquery(self):
        self.log.debug("cmquery in.")
        req = self.input["input"]
        # 指定项目id
        pid = req["pid"]
        # 当前页码数,第一次查询是默认为0
        page = req["page"]
        # 每页显示条数
        limitnum = 8
        if page:
            # 数据库查询时跳过的条数
            skipnum = (int(page)-1) * limitnum
            list0 = Case_model().cmquery_page(pid=pid, skip_num=skipnum, limit_num=limitnum)
            self.out = {"data": list0}
        else:
            # 第一次查询，页码为0，查询总条数，用于前台分页
            total = Case_model().cmquery_total(pid=pid)
            list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=limitnum)
            self.out = {"total": total, "data": list0}

    # 查询指定项目模版的id和名称，用于新增用例，所需参数opr,pid
    def cmquery_id_name(self):
        self.log.debug("cmquery_id_name in.")
        req = self.input["input"]
        # 指定的项目id
        pid = req["pid"]
        list0 = Case_model().cmquery_id_name(pid=pid)
        self.out = {"data": list0}

    # 通过模块名称模糊查询指定项目模版列表，所需参数opr,pid,name,page
    def cmquery_by_name(self):
        self.log.debug("cmquery_by_name in.")
        req = self.input["input"]
        # 指定项目id
        pid = req["pid"]
        # 模版名称
        name = req["name"]
        # 当前页码数,第一次查询是默认为0
        page = req["page"]
        # 每页显示条数
        limitnum = 8
        if page:
            # 数据库查询时跳过的条数
            skipnum = (int(page) - 1) * limitnum
            list0 = Case_model().cmquery_page_by_name(pid=pid, skip_num=skipnum, limit_num=limitnum, name=name)
            self.out = {"data": list0}
        else:
            # 第一次查询，页码为0，查询总条数，用于前台分页
            total = Case_model().cmquery_total_by_name(pid=pid, name=name)
            list0 = Case_model().cmquery_page_by_name(pid=pid, skip_num=0, limit_num=limitnum, name=name)
            self.out = {"total": total, "data": list0}

    # 通过id去查询用例模版,所需参数opr,id
    def cmquery_by_id(self):
        self.log.debug("cmquery_by_id in.")
        req = self.input["input"]
        # 模版id
        id = req["id"]
        case_model = Case_model().cmqueryone(id=id)
        if case_model:
            self.out = {"status": 0, "data": case_model}
        else:
            self.out = {"status": 1}

    # 编辑模版，所需参数opr, id, name, pid, ip, url, method, type
    def cmupdate(self):
        self.log.debug("cmupdate in.")
        req = self.input["input"]
        # 模版id
        id = req["id"]
        # 模版名
        name = req["name"]
        # 项目名
        pid = req["pid"]
        # API主机
        ip = req["ip"]
        # 请求url
        url = req["url"]
        # 请求方法
        method = req["method"]
        # 请求类型
        type = req["type"]
        # 返回true（更新成功）/false（更新失败）
        istrue = Case_model().cmupdate(id=id, name=name, pid=pid,
                                       ip=ip, url=url, method=method, type=type)
        if istrue:
            # 重新查询
            total = Case_model().cmquery_total(pid=pid)
            list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
            self.out = {"status": 0, "total": total, "data": list0}
        else:
            self.out = {"status":1}


    # 删除模版,所需参数opr,id,pid
    def cmdelete(self):
        self.log.debug("cmdelete in.")
        req = self.input["input"]
        # 模版id
        id = req["id"]
        # 项目id
        pid = req["pid"]
        # 批量删除
        if isinstance(id, list):
            # 成功删除的个数
            total = 0
            # 循环删除
            for i in id:
                num = Case_model().cmdelete(i)
                if num:
                    total += 1
            if total == len(id):
                # 重新查询
                total = Case_model().cmquery_total(pid=pid)
                list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
                self.out = {"status": 0, "total": total, "data": list0}
            else:
                self.out = {"status": 1}
        # 删除单个
        else:
            # 返回1（删除成功）/0（删除失败）
            num = Case_model().cmdelete(id)
            if num:
                # 重新查询
                total = Case_model().cmquery_total(pid=pid)
                list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
                self.out = {"status": 0, "total": total, "data": list0}
            else:
                self.out = {"status": 1}

if __name__ == "__main__":

    pass