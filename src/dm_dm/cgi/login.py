#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, request
import json
from tp_global import *
from tp_redis import g_redis
from cgibase import cgibase
from tp_mongodb import *


class Clogin(cgibase):
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

    # 登录，所需参数opr,name,pwd
    def login(self):
        self.log.debug("login in.")
        req = self.input["input"]
        # 用户名
        name = req["name"]
        # 密码
        pwd = req["pwd"]

        user = User().find(name = name, pwd = pwd)
        if user:
            self.out_ssid = randomStr()
            # 登录成功后去查询项目id、项目名称
            list = Project().proquery_id_name()
            self.out = {"status": 0,"data":list}
        # if name == "zl" and pwd == "123":
        #     self.out_ssid = randomStr()
        #     g_redis.set(g_redis_pix + self.out_ssid, name)
        #     g_redis.expire(g_redis_pix + self.out_ssid, g_ssid_timeout)
        #     self.out = '{"status":0}'
        else:
            self.out = {"status": 1, "msg": "passwd or name error."}

    # 新增用户，所需参数opr,name,pwd,email
    def useradd(self):
        self.log.debug("useradd in.")
        req = self.input["input"]
        # 用户名
        name = req["name"]
        # 密码
        pwd = req["pwd"]
        # 邮箱
        email = req["email"]
        # 注册成功则返回用户ID，失败返回空
        num = User().useradd(name=name, pwd=pwd, email=email)
        if num:
            self.out = {"status": 0}
        else:
            self.out = {"status": 1}

    def check_name(self):
        self.log.debug("check_name in.")
        req = self.input["input"]
        # 用户名
        name = req["name"]
        # 若用户已经存在返回1
        num = User().check_name(name=name)
        # 存在返回1，并提示
        if num:
            self.out = {"status": 1, "msg": "name already sign in"}
        else:
            self.out = {"status": 0}


    def add(self):
        self.log.debug("add in.")
        if not cgibase.checkCookie(self):
            return
        self.out = '{"status":0}'

    def logout(self):
        self.log.debug("logout in.")
        sid = self.input["tp_self"]["ssid"]
        if (sid == '' or sid is None):
            self.out = {"status": 0}
            return
        g_redis.delete(g_redis_pix + sid)
        self.out = {"status": 0}

if __name__ == "__main__":
    pass
