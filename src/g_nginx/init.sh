#!/bin/bash

nginx_do() {
    mkdir -p /var/run/
    mkdir -p /data/log/
    mkdir -p /data/www/upload
    /usr/sbin/nginx -c /data/nginx.conf
}
rm /etc/localtime -f
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
nginx_do
