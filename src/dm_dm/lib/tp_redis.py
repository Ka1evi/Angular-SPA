#!/usr/bin/env python
# coding=utf-8

##
# @file    vpn_redis.py
# @brief   redis
# @author  zhanglong
# @date    2016-08-23
# @version 1.0

import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
g_redis = redis.Redis(connection_pool=pool)
