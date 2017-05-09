#!/usr/bin/python
# -*- coding: utf-8 -*-

from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
from upload import Cupload
import xlrd
import os
import yaml


class Cread(cgibase):
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
        eval("self.%s()" % opr)

    def caseadd(self, d):
        num = Case().readoneadd(d)
        count = Case().readcount()
        if num:
            self.out = {"status": 0, "msg": "suss", "add": len(d), 'count': count}
        else:
            self.out = {"status": 1}

    def modeladd(self, d):
        num = Case_model().modeladd(d)
        count = Case_model().readcount()
        if num:
            self.out = {"status": 0, "msg": "suss", "add": len(d), 'count': count}
        else:
            self.out = {"status": 1}

    def caread(self):
        self.log.debug("cread in.")
        req = self.input["input"]
        file = req["filename"]
        type1 = req["type"]
        a, b = os.path.splitext(file)
        if b.__eq__(".yaml"):
            fn = open(Cupload().get_tmp_path() + file)
            d = yaml.load(fn)
            print len(d)
            fn.close()
            if type1 == 1:
                self.caseadd(d)
            else:
                self.modeladd(d)

        elif b.__eq__(".xls") or b.__eq__(".xlsx"):
            book = xlrd.open_workbook(Cupload().get_tmp_path() + file)
            for s in book.sheets():
                firstline = []
                print s.nrows
                for r in range(s.nrows):
                    if r == 0:
                        firstline = s.row(r)
                        if len(firstline) != 4:
                            print 0
                    else:
                        d = {}
                        # 输出指定行
                        line = s.row(r)
                        for i in range(len(firstline)):
                            d[firstline[i].value] = line[i].value
                        if type1 == 1:
                            self.caseadd(d)
                        else:
                            self.modeladd(d)



if __name__ == "__main__":
    pass
