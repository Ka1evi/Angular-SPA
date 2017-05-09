#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
from main_index import alarm_schedule

class Csetting(cgibase):
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

    # 设置定时执行时间，所需参数:opr,timing
    def setting(self):
        self.log.debug("setting in.")
        req = self.input["input"]
        # 执行时间
        timing = req["timing"]
        # 调用方法更新执行时间
        istrue = Timing().setting(timing=timing)
        # 返回true（更新成功）/false（更新失败）
        if istrue:
            # 启动定时任务
            alarm_schedule().input_one_time()
            self.out = {"status": 0}
        else:
            self.out = {"status": 1}

    # 查询所有用户及邮箱，所需参数:opr
    def user_email(self):
        self.log.debug("user_email in.")
        req = self.input["input"]
        # 用户、邮箱列表
        list1 = User().find_name_email()
        self.out = {"data":list1}

    # 设置收件人，所需参数:opr,user,to_email
    def to_email_address(self):
        self.log.debug("to_email_address in.")
        req = self.input["input"]
        # 当前用户
        user = req["user"]
        # 收件人列表
        to_email = req["to_email"]
        num = To_email().add_email(user=user, to_email=to_email)
        if num:
            self.out = {"status": 0}
        else:
            self.out = {"status": 1}



if __name__ == "__main__":
    pass