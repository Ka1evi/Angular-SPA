#!/bin/bash

redis_do() {
	port=$1
	mkdir -p /data/redis/pid/
	mkdir -p /data/redis/log/
	mkdir -p "/data/redis/dir/$port/"
  rm -rf /data/${port}.conf
	cp /data/redis.conf.bak /data/${port}.conf
	sed -i "s/bosspay_port/${port}/g" /data/${port}.conf
	redis-server "/data/${port}.conf"
}
rm /etc/localtime -f
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
redis_do $1
