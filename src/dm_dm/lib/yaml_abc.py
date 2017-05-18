# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import tablib
import random
import json

conn = pymongo.MongoClient('10.10.62.10', 27017)
db = conn.test
collection = db.case

# #查询单条记录
# headers=collection.find_one()
# #查询所有记录
# # for data in collection.find():
# data = tablib.Dataset(*(collection.find()),headers=headers)
# print data.yaml
# data.xlsx
# open('ss%s.xlsx'% random.uniform(1, 5),"wb").write(data.xlsx)



# 查询单条记录
# headers = ["用例编号", "请求参数", "用例名称", "检查点", "请求URL", "是否开始定时任务",
#            "主机IP", "用例所属模块", "请求类型", "用例最后编辑人员", "用例说明", "用例编辑时间",
#            "请求方法", "用例是否加密", "用例级别", "用例所属项目编号"]
# 查询所有记录
headers = ["index", "_id", "c_data", "c_name", "c_check", "c_url", "c_timing",
           "c_ip", "c_pmodel", "c_type", "c_user", "c_desc", "c_time",
           "c_method", "c_encrypt", "c_rank", "c_pid"]
print headers

list = []
index = 0
for data in collection.find():
    a = (index, str(data["_id"]), data["c_data"], data["c_name"], data["c_check"], data["c_url"],
         data["c_timing"], data["c_ip"], data["c_pmodel"], data["c_type"], data["c_user"],
         data["c_desc"], data["c_time"], data["c_method"], data["c_encrypt"], data["c_rank"],
         str(data["c_pid"]))
    list.append(a)
    index += 1
data = tablib.Dataset(*list, headers=headers)
print data.yaml
data.xlsx
ra = random.uniform(1, 5)
f = open('case.yaml', "wb")
f.write(data.yaml)
f.close
