#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request
from tp_global import *
from cgibase import cgibase
import time

class Cupload(cgibase):
    def __init__(self):
        return cgibase.__init__(self)

    def onInit(self):
        cgibase.SetNoCheckCookie(self)

        opr = cgibase.onInit(self)
        print opr
        if opr is None:
            return
        if not hasattr(self, opr):
            self.out = g_err["input_err"]
            return
        eval("self.%s()" % opr)

    def allow_ext(self):
        return ["yaml", "xlsx"]

    def get_tmp_path(self):
        return "../../g_nginx/www/upload/"

    def upload(self):
        self.log.debug("upload in.")
        self.out = {"status": 0, "allow": self.allow_ext(), "path": self.get_tmp_path()}
        self.log.debug("out is %s..." % self.out)


if __name__ == "__main__":
    upload = Cupload()
    upload.onInit()
