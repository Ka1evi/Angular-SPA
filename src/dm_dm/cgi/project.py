#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *


class Cproject(cgibase):
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

    #新增项目，所需参数opr,name,desc
    def proadd(self):
        self.log.debug("proadd in.")
        req = self.input["input"]
        # 项目名
        name = req["name"]
        # # 项目模块
        # model = req["model"]
        # if not isinstance(model, list):
        #     self.out = {"status": 1, "msg": "model not list"}
        # 项目说明
        desc = req["desc"]
        # 用户
        user = req["user"]
        # 新增成功则返回项目ID，失败返回空
        # num = Project().proadd(name=name, model=model, desc=desc, user=user)
        num = Project().proadd(name=name, desc=desc, user=user)
        if num:
            # 重新查询项目列表
            list0 = Project().proquery_id_name()
            self.out = {"status": 0, "data": list0}
        else:
            self.out = {"status": 1}

    # 查询某一项目信息，所需参数opr,id
    def proquery(self):
        self.log.debug("proquery in.")
        req = self.input["input"]
        # 项目id
        id = req["id"]
        # 查询得到项目说明
        dict1 = Project().proquery_desc(id=id)
        # 查询项目成功、失败次数
        dict2 = Result().proresult(pid=id)
        dict0 = dict(dict1,**dict2)
        # 查询项目模块
        modellist = Model().modelquery(pid=id)
        dict3 = {"model":modellist}
        dict4 = dict(dict3,**dict0)
        self.out = dict4

    # 编辑项目，所需参数opr,id,name,desc
    def proupdate(self):
        self.log.debug("proupdate in.")
        req = self.input["input"]
        # 项目id
        id = req["id"]
        # 项目名
        name = req["name"]
        # 用户
        user = req["user"]
        # # 项目模块
        # model = req["model"]
        # if not isinstance(model, list):
        #     self.out = {"status": 1}
        # 项目说明
        desc = req["desc"]
        # 返回true（更新成功）/false（更新失败）
        # istrue = Project().proupdate(id=id,name=name,model=model,desc=desc)
        istrue = Project().proupdate(id=id,name=name,desc=desc,user=user)
        if istrue:
            # 重新查询项目列表
            list0 = Project().proquery_id_name()
            self.out = {"status": 0, "data": list0}
        else:
            self.out = {"status": 1}

    # 删除项目,所需参数opr,id
    def prodelete(self):
        self.log.debug("prodelete in.")
        req = self.input["input"]
        # 项目id
        id = req["id"]
        # 返回1（删除成功）/0（删除失败）
        num = Project().prodelete(id)
        # 项目删除成功后需将项目所属的模版和用例删除
        if num:
            # 删除项目所有的模版
            cm_id_list = Case_model().cmquery_id(pid=id)
            for cm_id in cm_id_list:
                Case_model().cmdelete(id=cm_id)
            # 删除项目所有模块
            Model().deletemodel_all(pid=id)
            # 删除项目所有用例
            case_id_list = Case().casequery_pro_id(pid=id)
            for case_id in case_id_list:
                Case().casedelete(id=case_id)

            # 重新查询项目列表
            list = Project().proquery_id_name()
            self.out = {"status": 0, "data": list}
        else:
            self.out = {"status": 1}

    # # 新建项目模块，所需参数opr,id,addmodel
    # def proaddmodel(self):
    #     self.log.debug("proaddmodel in.")
    #     req = self.input["input"]
    #     # 当前项目id
    #     id = req["id"]
    #     # 新增项目模块名
    #     addmodel = req["addmodel"]
    #     # 返回true（新增成功）/false（新增失败）
    #     istrue = Project().proaddmodel(id=id, addmodel=addmodel)
    #     if istrue:
    #         # 查询得到项目模块、项目说明
    #         dict1 = Project().proquery_model_desc(id=id)
    #         # 查询项目成功、失败次数
    #         dict2 = Result().proresult(pid=id)
    #         dict0 = dict(dict1, **dict2)
    #         self.out = {"status": 0, "data": dict0}
    #     else:
    #         self.out = {"status": 1}
    #
    # # 删除项目模块，所需参数opr,id,deletemodel
    # def prodeletemodel(self):
    #     self.log.debug("prodeletemodel in.")
    #     req = self.input["input"]
    #     # 当前项目id
    #     id = req["id"]
    #     # 删除项目模块名
    #     deletemodel = req["deletemodel"]
    #     istrue = Project().prodeletemodel(id=id, deletemodel=deletemodel)
    #     # 返回ture（删除成功）/false（删除失败）
    #     if istrue:
    #         # 删除模块后须将模块下的所有用例删除
    #         case_id_list = Case().casequery_model_id(pid=id, pmodel=deletemodel)
    #         for case_id in case_id_list:
    #             Case().casedelete(id=case_id)
    #         # 查询得到项目模块、项目说明
    #         dict1 = Project().proquery_model_desc(id=id)
    #         # 查询项目成功、失败次数
    #         dict2 = Result().proresult(pid=id)
    #         dict0 = dict(dict1, **dict2)
    #         self.out = {"status": 0, "data": dict0}
    #     else:
    #         self.out = {"status":1}



if __name__ == "__main__":
    pass
