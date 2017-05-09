#!/usr/bin/env python
# coding=utf-8
import sys, json, os
import logging
import logging.handlers
import commands
import urllib
import urlparse
from tp_global import *
from tp_redis import g_redis
from tasks import mytask


class cgibase:
    def __init__(self):
        self.myinit()

    def __del__(self):
        self.mydel()

    def myinit(self):
        self.out = {}
        self.input = {}
        self.out_ssid = None
        self.redirect_url = None
        self.log_handler = None
        self.__cookieFlag = True
        self.name = None
        self.log = None
        self.isdebug = False

    def mydel(self):
        if self.log_handler is not None:
            self.log.removeHandler(self.log_handler)
            self.log_handler = None
        if self.isdebug is True:
            print self.output()

    def setenv(self, req_dict):
        self.input = req_dict

    def output(self):
        if type(self.out) is dict:
            self.out = json.dumps(self.out, ensure_ascii=False)
        self.log.debug("cgibase out is %s..."%self.out)
        return self.out

    def onInit(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if self.input == {}:
            self.isdebug = True
            self.SetNoCheckCookie()

            if len(sys.argv) != 3:
                self.out = g_err["input_err"]
                return None
            self.input["tp_self"] = {}
            self.input["tp_self"]["fun"] = sys.argv[1]
            self.input["tp_self"]["ip"] = "127.0.0.1"
            self.input["tp_self"]["ssid"] = None
            self.input["tp_self"]["m"] = "GET"
            arg = sys.argv[2]
            isjson = False
            data_in = ""
            if arg.find("file://") == 0:
                self.input["tp_self"]["m"] = "POST"
                try:
                    file = open(arg[len("file://"):])
                except:
                    self.out = g_err["input_err"]
                    return None
                else:
                    data_in = file.read()
                    file.close()
                    try:
                        json.loads(data_in)
                    except:
                        isjson = False
                    else:
                        isjson = True
            else:
                data_in = arg
            jsondata = {}
            if isjson is False:
                data_in = urllib.unquote(data_in)
                data_in = urlparse.parse_qsl(data_in)
                for dat in data_in:
                    jsondata[dat[0]] = dat[1]
            else:
                jsondata = json.loads(data_in)
            self.input["input"] = jsondata

        cginame = self.input["tp_self"]["fun"]
        cgi_debug_file = CGI_LOG_PATH + cginame + ".log"
        handler = logging.handlers.RotatingFileHandler(cgi_debug_file, maxBytes = MAX_CGI_LOG_SIZE, backupCount = 1)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.log = logging.getLogger(cginame)
        self.log_handler = handler
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)

        self.log.debug('\n\n### start debug log ###\n')
        self.log.debug(json.dumps(self.input, ensure_ascii=False))

        if self.__cookieFlag:
            if not self.checkCookie():
                return None

        opr = None
        if not self.input["input"].has_key("opr"):
            self.out = g_err["input_err"]
            return opr
        if self.input["input"]["opr"] not in g_opr_list:
            self.out = g_err["input_err"]
            return opr
        opr = self.input["input"]["opr"]
        return opr

    def SetNoCheckCookie(self):
        self.__cookieFlag = False
        return

    def exec_shell(self, shell):
        (status, out) = commands.getstatusoutput(shell)
        if (status != 0):
            self.log.debug("exec [%s] fail. out=%s"%(shell, out))
        else:
            self.log.debug("exec [%s] success. out=%s"%(shell, out))
        return (status, out)

    def exec_task(self, fun, arg={}, delay=1):
        a = {"delay":delay, "fun":fun, "arg":arg}
        mytask.apply_async([a])

    def checkCookie(self):
        sid = self.input["tp_self"]["ssid"]

        if (sid == '' or sid is None):
            self.out = g_err["relogin"]
            return False #cookie error
        # r = g_redis.get(g_redis_pix + sid)
        # if r is None or r == "":
        #     self.out = g_err["relogin"]
        #     return False #cookie error
        # self.name = r
        # g_redis.expire(g_redis_pix + sid, g_ssid_timeout)
        return True


if __name__ == "__main__":
    pass
