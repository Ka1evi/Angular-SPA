#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *


class Cmodel(cgibase):
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

    # 新建项目模块，所需参数opr,id,addmodel
    def addmodel(self):
        self.log.debug("addmodel in.")
        req = self.input["input"]
        opr = req["addmodel"]
        # 项目id，将模块与项目关联
        id = req["id"]
        # 模块名称
        name = req["addmodel"]
        # 将模块加入数据库，返回1（新增成功）
        num = Model().addmodel(id=id, addmodel=name)
        if num:
            # 查询此项目下的所有模块
            modellist = Model().modelquery(pid=id)
            self.out = {"status": 0, "model": modellist, "pid": id}
        else:
            self.out = {"status": 1}


    # 删除项目模块，所需参数opr,id,deletemodel
    def deletemodel(self):
        self.log.debug("deletemodel in.")
        req = self.input["input"]
        # 项目id
        id = req["id"]
        # 模块名称
        name = req["deletemodel"]
        # 将模块从数据库删除
        num = Model().deletemodel(id=id, deletemodel=name)
        if num:
            # 删除模块后须将模块下的所有用例删除
            case_id_list = Case().casequery_model_id(pid=id, pmodel=name)
            for case_id in case_id_list:
                Case().casedelete(id=case_id)
            # 查询此项目下的所有模块
            modellist = Model().modelquery(pid=id)
            self.out = {"status": 0, "model": modellist, "pid": id}
        else:
            self.out = {"status": 1}


if __name__ == "__main__":
    pass
