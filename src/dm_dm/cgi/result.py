#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
import tp_smtp,json
from main_index import Interface_Tasking


class Cresult(cgibase):
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

    # 用例测试，所需参数opr,id,pid,user
    def execute(self):
        self.log.debug("execute in.")
        req = self.input["input"]
        # 用例（测试结果）名称
        # name = req["name"]
        # 项目id
        pid = req["pid"]
        # 用例id
        cid = req["id"]
        # 测试人员，即当前登录人员
        user = req["user"]

        # 此处调用测试工具，并传递参数cid
        exeresult = Interface_Tasking().give_one_objectid(id=ObjectId(cid))
        # 测试名称
        name = exeresult["c_name"]
        # 测试成功与否
        result0 = exeresult["r_result"]
        # 测试结果说明
        desc = exeresult["r_desc"]
        # 测试时间
        tim = exeresult['r_time']

        # 对返回值进行判断
        if exeresult:
            # 在数据库添加测试结果
            Result().execute(name=name,
                             pid=pid,
                             cid=cid,
                             user=user,
                             time=tim,
                             result=result0,
                             desc=desc)
            # 测试结果相关信息
            result = {"name": name,
                      "case_id": str(cid),
                      "result": result0,
                      "desc": desc,
                      "user": user,
                      "time": tim}
            # # 通过用户名得到用户邮箱
            # user = User().findemail(name=user)
            # email = user["u_email"]
            # # 此处发送邮件
            # num1 = tp_smtp.send(email=email, result=json.dumps(result).decode("unicode-escape"))

            # 通过用户名得到邮件发送地址
            from_email = User().findemail(name=user)
            # 邮件接收地址
            to_email = []
            # 项目创建人
            p_user = Project().proquery_user(id=pid)
            # 项目创建人邮箱地址
            pro_email = User().findemail(name=p_user)
            to_email.append(pro_email)
            # 当前用户添加的收件人
            u_email = To_email().find_email(user=user)
            if u_email:
                to_email.extend(u_email)
            num1 = tp_smtp.send(from_email=from_email, to_email=to_email, result=json.dumps(result).decode("unicode-escape"))

            if num1:

                #websocket发送推送pass

                self.out = {"status": 0, "data": result}
            # 邮件发送失败
            else:
                self.out = {"status": 2, "data": result}
        # 执行失败
        else:
            self.out = {"status": 1}


    # 用例批量测试，所需参数:opr,pid,model,user
    def executeall(self):
        self.log.debug("executeall in.")
        req = self.input["input"]
        # 用例（测试结果）名称
        # name = req["name"]
        # 项目id
        pid = req["pid"]
        # 需批量执行的用例所属模块名称
        model = req["model"]
        # 测试人员，即当前登录人员
        user = req["user"]
        # 此处调用测试工具，并传递参数
        result_list = Interface_Tasking().pid_and_model(pid=ObjectId(pid), model=model)
        # 测试成功的次数
        success_num = 0
        # 测试失败的次数
        fail_num = 0
        # 测试成功的结果列表
        success_list = []
        # 测试失败的结果列表
        fail_list = []
        # 此模块拥有的用例数
        total = Case().casequery_total(pid=pid, pmodel=model)
        if len(result_list) == total:
            for re in result_list:
                # 用例id
                cid = re["c_id"]
                # 测试名称
                name = re["c_name"]
                # 测试成功与否
                result0 = re["r_result"]
                # 测试结果说明
                desc = re["r_desc"]
                # 测试时间
                tim =re['r_time']
                # 在数据库添加测试结果
                Result().execute(name=name,
                                 pid=pid,
                                 cid=cid,
                                 user=user,
                                 time=tim,
                                 result=result0,
                                 desc=desc)
                # 测试结果相关信息
                result = {"name": name,
                          "case_id": str(cid),
                          "result": result0,
                          "desc": desc,
                          "user": user,
                          "time": tim}
                # 测试成功
                if result0 == 100:
                    success_num += 1
                    success_list.append(result)
                #　测试失败
                else:
                    fail_num += 1
                    fail_list.append(result)
            # # 通过用户名得到用户邮箱
            # user = User().findemail(name=user)
            # email = user["u_email"]
            # 通过用户名得到邮件发送地址
            from_email = User().findemail(name=user)
            # 邮件接收地址
            to_email = []
            # 项目创建人
            p_user = Project().proquery_user(id=pid)
            # 项目创建人邮箱地址
            pro_email = User().findemail(name=p_user)
            to_email.append(pro_email)
            # 当前用户添加的收件人
            u_email = To_email().find_email(user=user)
            if u_email:
                to_email.extend(u_email)
            # 测试结果
            dict0 = {"success_num": success_num,
                     "fail_num": fail_num,
                     "success_list": success_list,
                     "fail_list":fail_list}
            # 此处发送邮件
            # num1 = tp_smtp.send(email=email, result=json.dumps(dict0).decode("unicode-escape"))
            num1 = tp_smtp.send(from_email=from_email, to_email=to_email,
                                result=json.dumps(dict0).decode("unicode-escape"))
            if num1:

                # websocket发送推送pass

                self.out = {"status": 0, "data": dict0}
            # 邮件发送失败
            else:
                self.out = {"status": 2, "data": dict0}
        else:
            # 有用例执行失败
            self.out = {"status": 1}

    # # 查询项目用例整体执行情况，所需参数opr,id
    # def proresult(self):
    #     self.log.debug("proresult in.")
    #     req = self.input["input"]
    #     # 项目id
    #     pid = req["id"]
    #     # 查询数据库
    #     proresult = Result().proresult(pid=pid)
    #     # 返回查询结果
    #     self.out = proresult

    # 查询用例历史执行情况，所需参数opr,id
    def caseresult(self):
        self.log.debug("proresult in.")
        req = self.input["input"]
        # 用例id
        cid = req["id"]
        # 查询数据库
        list = Result().caseresult(cid=cid)
        # 返回查询结果
        self.out = {"data":list}

if __name__ == "__main__":
    pass