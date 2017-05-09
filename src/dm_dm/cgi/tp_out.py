# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
# import pymongo
import tablib
# import random
# import json

# conn = pymongo.MongoClient('10.10.62.10', 27017)
# db = conn.test
# collection = db.case
class Cout(cgibase):
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


    def caseout(self):
        self.log.debug("caseout in.")
        req = self.input["input"]
        # 项目id
        typ=req["typ"]
        id = req["id"]
        type1 = req["type"]
        print typ,id
        # 用例列表
        if type1 == 1:
            if isinstance(id, list):
                for i in id:
                    data = Case().caseout(i)
                    f = open('case~batch~out.%s' % typ, "ab+")
                    f.write(data.yaml)
                    f.close
                    self.out = {"type": '%s' % typ}

            else:
                data = Case().caseout(id=id)
                # data =Case_model().modelout(id=id)
                print data
                f = open('mme~~out.%s'%typ, "wb")
                if "yaml"==(typ):
                    f.write(data.yaml)
                    self.out = {"type": '%s' % typ}
                else:
                    f.write(data.xlsx)
                    self.out = {"type": '%s' % typ}
                f.close
        else:
            data = Case_model().modelout(id=id)
            print data
            f = open('mme~~out.%s' % typ, "wb")
            if "yaml" == (typ):
                f.write(data.yaml)
                self.out = {"type": '%s' % typ}
            else:
                f.write(data.xlsx)
                self.out = {"type": '%s' % typ}
            f.close

if __name__ == "__main__":
    pass