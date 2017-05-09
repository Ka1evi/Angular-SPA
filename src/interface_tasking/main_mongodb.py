# _*_ coding: utf-8 _*_
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

class Dao():
    """用于数据库操作的类"""
    def connection_db(self):
        """用于连接数据库的函数"""
        client = MongoClient("10.10.78.103", 27017)
        db = client['inter_tasking']
        return db
    def connection_liuzhen(self):
        client = MongoClient("10.10.62.10", 27017)
        db = client['test']
        return db

    def add(self, inter_add):
        """
        将测试结果放到数据库里面
        共10参，测试时间在函数里面
        result;desc  --测试结果；测试说明
        timing;  --定时调度
        inter_add['id'];inter_add['ip']  --用例编号；用例请求ip地址
        inter_add['url'];inter_add['method'] --请求URL，请求方法
        inter_add['type'];inter_add['data'] --请求类型，请求数据
        inter_add['check']  --检查点

        """
        db = self.connection_db()
        collection = db['inter_result']  # 联系数据库对应的集合
        # r_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) #返回当前时间
        # for key, value in inter_add.items():
        #     dict_add["c_"+key] = value
        # inter_add['r_time'] = r_time
        # dict_add['r_result'] = result
        # dict_add['r_desc'] = desc
        # dict_add['c_timing'] = timing
        collection.insert(inter_add)

    def find_by_id(self, id):
        """根据id查询单条数据"""
        db = self.connection_liuzhen()
        collection = db['case']
        testee = collection.find_one({"_id": id})
        return testee

    def find_by_timing(self):
        """
        根据定时调度查询所有符合要求的数据
        查询的是刘征的case表，非已执行的表
        """
        dao = Dao()
        db = dao.connection_liuzhen()
        collection = db['case']
        testees = collection.find({"c_timing": "YES"})
        return testees

    def pid_and_model(self, pid, model):
        """
        根据pid和model做协程，所有查询到的数据都要协程
        :param pid:
        :param model:
        :return:
        """
        dao = Dao()
        db = dao.connection_liuzhen()
        collection = db['case']
        testees = collection.find({"c_pid": pid, "c_pmodel": model})
        return testees

    def add_many(self, testees):
        """
        老版本的定时任务
        :param testees:
        :return:
        """
        db = self.connection_db()
        collection = db['inter_result']
        collection.insert_many(testees)
        pass

    def get_running_time(self):
        """从数据库获取定时时间"""
        db = self.connection_liuzhen()
        collection = db['timing']
        testee = collection.find()
        return testee[0]['time']


if __name__ == '__main__':
    dao = Dao()
#     dao.add({
#     "c_data" : {
#         "pwd" : "123456",
#         "name" : "liuz"
#     },
#     "c_name" : "登录测试1",
#     "c_check" : {
#         "status" : "login succeed"
#     },
#     "c_url" : "/cig-lib/login.do/login",
#     "c_timing" : "YES",
#     "c_ip" : "127.0.0.1",
#     "c_pmodel" : "login",
#     "c_type" : "application/json",
#     "c_user" : "liuz",
#     "c_desc" : "登录测试，可以成功登录，并返回{'status':'login succeed'}",
#     "c_time" : "2017-04-08 11:16:38",
#     "c_method" : "post",
#     "c_encrypt" : "no",
#     "c_rank" : "level1",
#     "c_pid" : ObjectId("58e5a4ea94f9410cd82d655d")
# })
    # print type(dao.find_by_id(ObjectId("58e84e4694f9411e0cf8a44d")))
    # dao.find_all_by_pid_and_model(ObjectId("58e5a4ea94f9410cd82d655d"), "login")
    # dao.get_running_time()
    # testees = dao.find_by_timing()
    # # print len(testees)
    # print type(testees)
    # for testee in testees:
    #     print type(testee), testee['_id']