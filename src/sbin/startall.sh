#!/bin/bash

sh /data/bz_redis/cmd.sh start
sh /data/m_mongo/cmd.sh start
sh /data/m_mongo/cmd.sh restart
sh /data/dm_dm/cmd.sh start
sh /data/g_nginx/cmd.sh start
