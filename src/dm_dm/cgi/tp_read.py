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

    def caseadd(self, pid, pmodel):
        # d.keys()[0] = "c_name"
        count = Case().casequery_total(pid, pmodel)
        list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
        # lists = {'count': count, "list": list0}
        return {'count': count, "list": list0}

    def modeladd(self, pid):
        count = Case_model().cmquery_total(pid)
        list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
        # lists = {'count': count, "list": list0}
        return {'count': count, "list": list0}

    def caread(self, pid, typ, f, pmodel, user):
        # self.log.debug("cread in.")
        # req = self.input["input"]
        file = f
        pid = pid
        typ=int(typ)
        print typ
        print typ==0
        if typ == 0:
            a, b = os.path.splitext(file)
            if b.__eq__(".yaml"):
                fn = open(Cupload().get_tmp_path() + file)
                data = yaml.load(fn)
                for r in range(len(data)):

                    firstline = data[r].keys()

                    print len(firstline)
                    if len(firstline) == 5:
                        firstline[0] = "cm_name"
                        firstline[1] = "cm_ip"
                        firstline[2] = "cm_url"
                        firstline[3] = "cm_method"
                        firstline[4] = "cm_type"
                    else:
                        count = Case_model().cmquery_total(pid)
                        list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
                        return {"status": 1,"msg": "fail",'count': count, "list": list0}

                    d = {}
                    # 输出指定行
                    # line = s.row(r)
                    for i in range(len(firstline)):
                        d[firstline[i]] = data[r][firstline[i]]
                        d["cm_pid"] = ObjectId(pid)
                    Case_model().modeladd(d)
                return self.modeladd(pid)


            elif b.__eq__(".xls") or b.__eq__(".xlsx"):
                book = xlrd.open_workbook(Cupload().get_tmp_path() + file)
                for s in book.sheets():
                    firstline = []

                    for r in range(s.nrows):
                        if r == 0:
                            firstline = s.row(r)

                            if len(firstline) == 5:
                                firstline[0] = "cm_name"
                                firstline[1] = "cm_ip"
                                firstline[2] = "cm_url"
                                firstline[3] = "cm_method"
                                firstline[4] = "cm_type"
                            else:
                                count = Case_model().cmquery_total(pid)
                                list0 = Case_model().cmquery_page(pid=pid, skip_num=0, limit_num=8)
                                return {"status": 1, "msg": "fail", 'count': count, "list": list0}
                            if len(firstline) != 4:
                                print 0
                        else:
                            d = {}
                            # 输出指定行
                            line = s.row(r)
                            for i in range(len(firstline)):
                                d[firstline[i]] = line[i].value
                                d["cm_pid"] = ObjectId(pid)
                            Case_model().modeladd(d)
                    return self.modeladd(pid)
        elif typ == 1:
            a, b = os.path.splitext(file)
            if b.__eq__(".yaml"):
                fn = open(Cupload().get_tmp_path() + file)
                data = yaml.load(fn)
                for r in range(len(data)):

                    firstline = data[r].keys()

                    print len(firstline)
                    if len(firstline) == 10:
                        firstline[0] = "c_name"
                        firstline[1] = "c_rank"
                        firstline[2] = "c_data"
                        firstline[3] = "c_check"
                        firstline[4] = "c_desc"
                        firstline[5] = "c_timing"
                        firstline[6] = "c_ip"
                        firstline[7] = "c_url"
                        firstline[8] = "c_method"
                        firstline[9] = "c_type"
                    else:
                        count = Case().casequery_total(pid, pmodel)
                        list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                        return {"status": 1, "msg": "fail", 'count': count, "list": list0}

                    d = {}
                    # 输出指定行
                    # line = s.row(r)
                    for i in range(len(firstline)):
                        d[firstline[i]] = data[r][firstline[i]]
                        d["c_pid"] = ObjectId(pid)
                        d["c_pmodel"] = pmodel
                        d["c_user"] = user
                        d["c_encrypt"] = "no"
                        d["c_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    Case().readoneadd(d)
                    return self.caseadd(pid, pmodel)

            elif b.__eq__(".xls") or b.__eq__(".xlsx"):
                book = xlrd.open_workbook(Cupload().get_tmp_path() + file)
                for s in book.sheets():
                    firstline = []

                    for r in range(s.nrows):
                        if r == 0:
                            firstline = s.row(r)

                            if len(firstline) == 10:
                                firstline[0] = "c_name"
                                firstline[1] = "c_rank"
                                firstline[2] = "c_data"
                                firstline[3] = "c_check"
                                firstline[4] = "c_desc"
                                firstline[5] = "c_timing"
                                firstline[6] = "c_ip"
                                firstline[7] = "c_url"
                                firstline[8] = "c_method"
                                firstline[9] = "c_type"
                            else:
                                count = Case().casequery_total(pid, pmodel)
                                list0 = Case().casequery_page(pid=pid, pmodel=pmodel, skip_num=0, limit_num=8)
                                return {"status": 1, "msg": "fail", 'count': count, "list": list0}
                            if len(firstline) != 4:
                                print 0
                        else:
                            d = {}
                            # 输出指定行
                            line = s.row(r)
                            for i in range(len(firstline)):
                                d[firstline[i]] = line[i].value
                                d["c_pid"] = ObjectId(pid)
                                d["c_pmodel"] = pmodel
                                d["c_user"] = user
                                d["c_encrypt"] = "no"
                                d["c_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                # return self.caseadd(d,pid,pmodel)
                            Case().readoneadd(d)
                    return self.caseadd(pid, pmodel)


if __name__ == "__main__":
    pass
