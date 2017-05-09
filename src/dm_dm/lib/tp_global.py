#!/usr/bin/env python
# coding=utf-8

##
# @file    tp_global.py
# @brief   基础文件
# @author  zhanglong
# @date    2016-08-23
# @version 1.0
import os
g_opr_list = ["add", "del", "modify", "list", "login", "logout", "useradd",
              "proadd", "proquery", "proupdate", "prodelete", "proaddmodel", "prodeletemodel",
              "cmadd", "cmquery", "cmquery_by_name", "cmupdate", "cmdelete",
              "caseadd", "casequery", "casequery_by_name", "caseupdate", "casedelete",
              "execute", "proresult", "caseresult", "casequery_by_id", "cmquery_by_id",
              "setting", "cmquery_id_name", "executeall","caseout","caread","upload", "addmodel", "deletemodel",
              "user_email", "to_email_address", "check_name"]
g_err = {
    "refused": '{"status":1, "msg":"url is refused."}',
    "input_err": '{"status":2, "msg":"input error."}',
    "relogin": '{"status":3, "msg":"need login.", "need_login":1}'
}

CGI_LOG_PATH = '/data/log/cgi/'
MAX_CGI_LOG_SIZE = 70*1024*1024
g_redis_pix = "s_"
g_ssid_timeout = 3600*2
RANDON_CHAR = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


def randomStr(randomlength=128):
    str = ''
    chars = RANDON_CHAR
    length = len(chars) - 1
    for i in range(randomlength):
        # 用urandom生成一个随机数，符合CheckList
        str += chars[ord(os.urandom(1)) % length]
    return str
