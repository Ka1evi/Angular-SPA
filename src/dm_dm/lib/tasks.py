#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
#导入celery相关模块、方法
from celery import Celery
from celery import platforms
#因为supervisord默认是用root运行的，必须设置以下参数为True才能允许celery用root运行
platforms.C_FORCE_ROOT = True
import task_fun
config = {}
config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/1'
config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/1'
#不需要返回任务状态，即设置以下参数为True
config['CELERY_IGNORE_RESULT'] = True
app = Celery("tasks", broker=config['CELERY_BROKER_URL'])
app.conf.update(config)


@app.task
def mytask(input):
    #{"delay":3, "fun":"test", "arg":{"a":"b"}}
    if input.has_key("delay"):
        time.sleep(int(input["delay"]))
    eval("task_fun.%s(input['arg'])"% input["fun"])
