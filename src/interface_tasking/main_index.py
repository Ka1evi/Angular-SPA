# _*_ coding: utf-8 _*_
from gevent import monkey
monkey.patch_all()
import gevent
import requests
import json
from main_mongodb import Dao
from alarm_scheduling import alarm_schedule
import time
import datetime
from threading import Timer
from bson.objectid import ObjectId
from pymongo import MongoClient

global alarm  # 设置定时闹钟
alarm = 0


class Interface_Tasking():
    """接口测试的主要类"""
    def __init__(self):
        self.url = ''

    def give_one_objectid(self, id):
        """
        给我一个实例id,根据id去数据库查找该条记录
        并且使用该记录里面的信息完成接口测试
        """
        dao = Dao()
        testee = dao.find_by_id(id=id)
        # if "YES" == testee['c_timing'].upper():  # 该语句用于定时调度做准备
        #     global alarm
        #     if alarm == 0:
        #         alarm = 1  # 设置全局变量改变并且启动定时任务，这样以后有就不用判断了，也不会重复启动定时
        #         alarm_schedule().input_one_time()  # 启动定时任务

        # 将数据库取出来的数据解压一下放入对应的形参，做基本的格式检测
        response = self.request_in_(testee)
        # 将最终返回结果存入数据库
        dao.add(response)
        # 前台要我就给啊...
        return response

    def pid_and_model(self, pid, model):
        """
        根据pid和model做批量测试
        用到协程
        :param pid:
        :param model:
        :return:
        """
        dao = Dao()
        # 现在数据库根据条件查询到数据列表
        testees = dao.pid_and_model(pid=pid, model=model)
        # 定义一个空的列表来存放个个协程
        request = []
        # 遍历启动协程并将协程放入request内
        for testee in testees:
            request.append(gevent.spawn(self.give_one_mongo_params, testee))
        # 定义空的列表存放个个协程返回的值
        response = []
        # 遍历将协程返回的值放入response内
        for res in gevent.joinall(request):
            response.append(res.value)
        return response

    def give_one_mongo_params(self, request_params):
        """
        传入一条完整的case
        :param request_params:
        :return:
        """
        dao = Dao()
        # 将数据库取出来的数据解压一下放入对应的形参，做基本的格式检测
        response = self.request_in_(request_params)
        # 将最终返回结果存入数据库
        dao.add(response)
        return response

    def request_in_(self, request_params):
        """
        接收从数据库取出来的记录，
        根据记录做相应的操作
        """
        # 用来存储错误结果或是返回响应
        result = {}
        # 作为一个卡尺来看是否有无效参数
        bool_params = False
        # 在查询之前需要做基本的内容验证，确定请求参数是否有效
        if request_params['c_data']:
            for key, value in request_params['c_data'].items():
                if not value:
                    bool_params = True
                    result["Error" + str(len(result))] = "data['" + key + "'] is null"
                if not key:
                    bool_params = True
                    result["Error" + str(len(result))] = "data['" + key + "']'s key is null"

        # 判断检查点的数据类型并且判断其值是否规范
        if isinstance(request_params['c_check'], dict):
            for key, value in request_params['c_check'].items():
                if (value == 0) or (value == 0.0):
                    pass
                elif (value == True) or (value == False):
                    pass
                elif (not key) or (not value):  # 当键或值是空的时候，输出检查点不合法
                    bool_params = True
                    result["Error" + str(len(result))] = "check is not legal"
        elif isinstance(request_params['c_check'], str):
            check_key = request_params['c_check']  # 取得检查点的键
            # 当值是空的情况
            if not check_key:
                bool_params = True
                result["Error" + str(len(result))] = "check is not legal"
        else:
            pass

        # 当确实存在非法参数时，进入条件语句，并将错误信息存入数据库，不再考虑继续执行
        if bool_params:
            response = self.back_response(request_params=request_params,
                                          r_desc=result, r_result=101)
            return response

        # 将请求类型放到头部
        headers = {'Content-Type': request_params['c_type']}
        if 'https://' in request_params['c_ip']:
            self.url = request_params['c_ip'] + request_params['c_url']
        else:
            if 'http://'in request_params['c_ip']:
                self.url = request_params['c_ip'] + request_params['c_url']
            else:
                self.url = 'http://' + request_params['c_ip'] + request_params['c_url']
        # 根据method不同选择不同的函数调用
        if request_params['c_method'].upper() == "GET":
            result = self.main_get(url=self.url, data=request_params['c_data'],
                                   headers=headers)
        elif request_params['c_method'].upper() == "POST":
            result = self.main_post(url=self.url, data=request_params['c_data'],
                                    headers=headers)
        else:
            return  # 保留内容

        # 将异常的详细信息输出：
        if isinstance(result, dict):
            if "Error" in result.keys()[0]:
                response = self.back_response(request_params=request_params,
                                              r_desc=result, r_result=101)
                return response
        # 判断检查点是否匹配
        if isinstance(request_params['c_check'], dict):
            #定义bools为真，当最后还为真的话就正确存入数据库
            bools = True
            #当返回的也是字典
            if 'application/json' in result.headers['Content-Type'] :
                r_check = json.loads(result.content)  # 返回的字典
                str_result = str(result)
                for key, value in request_params['c_check'].items():
                    # 该方法用于比较key值是不是r_check的键
                    #如果不是字典的键，bools是False
                    if not r_check.__contains__(key):
                        bools = False
                        break
                    elif r_check[key] != value:
                        bools = False
                        break
                    else:
                        pass
            #当返回的不是字典
            else:
                str_result = str(result.content)
                for key, value in request_params['c_check'].items():
                    if (key not in str_result) or (str(value) not in str_result):
                        bools = False
                    else:
                        pass
            if bools:
                r_desc = {"Succeed": str_result}
                response = self.back_response(
                    request_params=request_params,
                    r_desc=r_desc, r_result=100)
            else:
                r_desc = {"Error": "检查点不匹配..."}
                response = self.back_response(
                    request_params=request_params,
                    r_desc=r_desc, r_result=101)
        elif isinstance(request_params['c_check'], str):
            if 'application/json' in result.headers['Content-Type']:
                str_result = str(result)
            else:
                str_result = str(result.content)
            if str(request_params['c_check']) in str_result:
                r_desc = {"Succeed": str_result}
                response = self.back_response(request_params=request_params,
                                              r_desc=r_desc, r_result=100)
            else:
                r_desc = {"Error": "检查点不匹配..."}
                response = self.back_response(request_params=request_params,
                                              r_desc=r_desc, r_result=101)
        else:
            if 'application/json' in result.headers['Content-Type']:
                str_result = str(result)
            else:
                str_result = str(result.content)
            if str(request_params['c_check']) in str_result:
                r_desc = {"Succeed": str_result}
                response = self.back_response(request_params=request_params,
                                              r_desc=r_desc, r_result=100)
            else:
                r_desc = {"Error": "检查点不匹配..."}
                response = self.back_response(request_params=request_params,
                                              r_desc=r_desc, r_result=101)
        return response

    def main_get(self, url, headers, data=''):
        """get方式传参"""
        try:
            if data != '':
                result = requests.get(url=url, params=data, headers=headers)
            else:
                result = requests.get(url=url, headers=headers)
            result.raise_for_status()
        # 抛出的异常
        except requests.RequestException as error:
            result = {}
            result["Error"] = str(error)
        finally:
            return result

    def main_post(self, url, headers, data=''):
        """method为post的时候使用的函数"""
        try:
            if data == '':
                result = requests.post(url=url, headers=headers)
            else:
                if 'application/json'.upper() in headers['Content-Type'].upper():
                    # 在请求类型是application/json的时候，会有一点不一样
                    result = requests.post(url=url, data=json.dumps(data),
                                           headers=headers)
                else:
                    result = requests.post(url=url, data=data,
                                           headers=headers)
            result.raise_for_status()
        except requests.RequestException as error:
            result = {}
            result["Error"] = str(error)
        finally:
            return result

    def back_response(self, request_params, r_desc, r_result):
        """
        专门用来返回结果，
        当然，只是把结果在这里规范而已
        """
        #这一部分只是做一个id转换成c_id
        response = request_params
        c_id = response['_id']
        del response['_id']
        response['c_id'] = c_id

        response['r_result'] = r_result  # 根据状态码可看出成功与否
        response['r_desc'] = r_desc  # 存储具体的成功失败内容
        r_time = time.strftime('%Y-%m-%d %H:%M:%S',
                               time.localtime())  # 返回当前时间
        response['r_time'] = r_time
        return response

if __name__ == '__main__':
    inter = Interface_Tasking()
    inter.pid_and_model(ObjectId("58e5a4ea94f9410cd82d655d"), '登录模块')
    # inter.give_one_objectid(ObjectId("58e84e4694f9411e0cf8a44d"))
    # inter.pid_and_model(ObjectId("58e5a4ea94f9410cd82d655d"), "login")



