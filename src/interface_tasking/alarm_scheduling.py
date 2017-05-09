# _*_ coding: utf-8 _*_
from gevent.monkey import patch_all
patch_all()
import gevent
import datetime
import time
from threading import Timer
from main_mongodb import Dao


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
        next_time = time.mktime(time.strptime(str_next_t, "%Y-%m-%d %H:%M:%S"))
        now_time = time.time()
        if next_time < now_time:
            #如果next_time小于现在时间，就加一天
            delta = datetime.timedelta(days=1)  # 加一天时间
            _1_days = now + delta  # 一天后的现在时间
            # 取得一天后现在时间的String类型
            str_delta = _1_days.strftime('%Y-%m-%d %H:%M:%S')
            str_delta = str_delta[:11]  # 将该String类型的前十位（也就是年月日截留，其余舍弃）
            str_delta += (timing + ':00')  # 在截留的时间字符串后面添加日时秒
            # 得到明天的执行时间
            next_time = time.mktime(time.strptime(str_delta, "%Y-%m-%d %H:%M:%S"))
            delta_t = next_time - now_time
        else:
            delta_t = next_time - now_time
        return delta_t

global timer
timer = Timer(0, alarm_schedule().alarm_gogogo)

if __name__ == '__main__':
    alarm_schedule().input_one_time()
