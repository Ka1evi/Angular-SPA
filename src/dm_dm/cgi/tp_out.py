# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from tp_global import *
from cgibase import cgibase
from tp_mongodb import *
import tablib

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
        # ad="C:/Users/Administrator/Desktop/eee/"
        ad = req["address"]

        file="The export file%s.xlsx"%  time.time()
        if os.path.exists(ad):
            ad=ad
        else:
            os.makedirs(ad)
        ids = req["id"]
        typ = req["typ"]
        try:
            f = open(ad + file, "wb")

        except IOError:
            self.out = {"status": 1,"address": "路径错误"}
        else:
            f.close()
            # os.makedirs(ad)
            # 用例列表
            if typ == 1:
                if isinstance(ids, list):
                    f = open(ad + file, "wb")
                    caselist = []
                    for id in ids:
                        data = Case().caseout(id)
                        caselist.append(data)
                        headers = ["用例编号", "请求参数", "用例名称", "检查点", "请求URL", "是否开始定时任务",
                                   "主机IP", "用例所属模块", "请求类型", "用例最后编辑人员", "用例说明", "用例编辑时间",
                                   "请求方法", "用例是否加密", "用例级别", "用例所属项目编号"]
                        data1 = tablib.Dataset(*caselist, headers=headers)
                        f.write(data1.xlsx)
                        f.close
                        self.out = {"status": 0,"address": ad,"filename":file}

                else:
                    data = Case().caseoneout(id=ids)
                    # data =Case_model().modelout(id=id)
                    f = open(ad+file, "wb")

                    f.write(data.xlsx)
                    self.out = {"status": 0,"address": ad,"filename":file}
                    f.close
            else:
                if isinstance(ids, list):
                    f = open(ad + file, "wb")
                    cmlist = []
                    for id in ids:
                        data = Case_model().modelout(id)
                        cmlist.append(data)
                    headers = ["模版编号", "模版名称", "主机IP", "请求URL", "请求方法", "请求类型"]
                    data1 = tablib.Dataset(*cmlist, headers=headers)
                    f.write(data1.xlsx)
                    f.close()

                    self.out = {"status": 0,"address": ad, "filename": file}
                else:
                    data = Case_model().modeloneout(id=ids)
                    f = open(ad+file, "wb")
                    f.write(data.xlsx)
                    self.out = {"status": 0,"address": ad,"filename":file}
                    f.close

if __name__ == "__main__":
    pass