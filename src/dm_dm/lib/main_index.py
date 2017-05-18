# _*_ coding: utf-8 _*_
from gevent import monkey
monkey.patch_all()
import gevent
import requests
import json
import time
import datetime
from threading import Timer
from bson.objectid import ObjectId
from pymongo import MongoClient
import click
import yaml
from bson.objectid import ObjectId

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

class alarm_schedule():
    """定义定时类，只是面向对象罢了，没什么大不同的"""

    def alarm_gogogo(self):
        """
        进入后其实当用户修改时间后是会停止的，而且会修改下次执行时间...
        如果用户不修改时间他就是一个永不停歇的函数
        24小时制的
        """
        dao = Dao()
        from main_index import Interface_Tasking
        inter_task = Interface_Tasking()
        testees = []  # 存储所有定时任务的结果，以列表的形式
        all_timings = dao.find_by_timing()  # 根据timing="YES"查处所有定时任务
        for all_timing in all_timings:
            # 循环将所有要执行的c_timing是"YES"的记录转换成协程
            # 并且放入列表内一次执行
            gev = gevent.spawn(inter_task.give_one_mongo_params, all_timing)
            testees.append(gev)
        gevent.joinall(testees)
        # 需要调度定时启动循环
        global timer
        delta_t = self.get_delta_t()
        timer = Timer(delta_t, self.alarm_gogogo)
        timer.start()

    def input_one_time(self):
        """
        给前端的接口，这样就可以做定时了
        不管是修改了定时时间还是触发定时任务，都可以用
        :return: NONE
        """
        global timer
        time.sleep(0)
        timer.cancel()
        delta_t = self.get_delta_t()
        timer = Timer(delta_t, self.alarm_gogogo)
        timer.start()

    def get_delta_t(self):
        """
        用于获取数据库中定时时间
        :return:从现在时间到执行时间之间的毫秒数
        """
        dao = Dao()
        timing = dao.get_running_time()

        now = datetime.datetime.now()  # 现在时间
        # 获取现在时间的String类型并只保留年月日部分，将时分秒部分剔除,保留一个空格
        str_now_ymd = now.strftime('%Y-%m-%d %H:%M:%S')[:11]

        str_next_t = str_now_ymd + timing + ":00"  # 欲下一次执行的时间

        # next_time是一个从1970到今天timing时间的秒数表示
        next_time = time.mktime(
            time.strptime(str_next_t, "%Y-%m-%d %H:%M:%S"))
        now_time = time.time()
        if next_time < now_time:
            # 如果next_time小于现在时间，就加一天
            delta = datetime.timedelta(days=1)  # 加一天时间
            _1_days = now + delta  # 一天后的现在时间
            # 取得一天后现在时间的String类型
            str_delta = _1_days.strftime('%Y-%m-%d %H:%M:%S')
            str_delta = str_delta[:11]  # 将该String类型的前十位（也就是年月日截留，其余舍弃）
            str_delta += (timing + ':00')  # 在截留的时间字符串后面添加日时秒
            # 得到明天的执行时间
            next_time = time.mktime(
                time.strptime(str_delta, "%Y-%m-%d %H:%M:%S"))
            delta_t = next_time - now_time
        else:
            delta_t = next_time - now_time
        return delta_t

global timer
timer = Timer(0, alarm_schedule().alarm_gogogo)

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



@click.command()
@click.option('-i', '--index', default=0, help='index of the case on the yaml')
@click.option('-f', '--function', type=click.Choice(['id','gevent', 'timing']),
              help='select a function you want to execute from the list:id=give_one_object_id;gevent=pid_and_model;timing=input_one_time')
def the_face(index, function):
	# click.echo('function is: %s' % function)
    f = open('case.yaml')
    s = yaml.load(f)
    if function == "id":
        str_id = s[index]['_id']
        id = ObjectId(str_id)  # 取出来的不是ObjectId型的
        print type(id)
        print id
    # f = open('case.yaml')
    # s = yaml.load(f)
    if function == "gevent":
        str_pid = s[index]['c_pid']
        pid = ObjectId(str_pid)  # 取出来的不是ObjectId型的
        model = s[index]['c_pmodel'].encode('utf-8')

    # if (function == 'give_one_objectid') or (function == 'pid_and_model'):
	 #    eval('Interface_Tasking().%s(%s)' % (function, index))
    # if function == 'input_one_time':
    #     eval('alarm_schedule().%s()' % function)
    if function == 'id':
        eval('Interface_Tasking().give_one_objectid(%r)' %  id)
    if function == 'gevent':
        eval('Interface_Tasking().pid_and_model(%r, %r)' % (pid, model))
    if function == 'timing':
        eval('alarm_schedule().input_one_time()')

if __name__ == '__main__':
    the_face()
    # Interface_Tasking().give_one_objectid(3)
    # alarm_schedule().input_one_time()