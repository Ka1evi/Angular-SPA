#!/bin/bash

pidfile="/var/run/gunicorn.pid"
acc_log="/data/log/access.log"
err_log="/data/log/error.log"

dm_do() {
    port=$1
    cpu=$2
    mkdir -p /var/run/
    mkdir -p /data/log/
		mkdir -p /data/log/cgi/

    cd /data/cgi
    rm -f $pidfile
    gunicorn -w $cpu -b 127.0.0.1:${port} index:app  --access-logfile $acc_log -p $pidfile --error-logfile $err_log
}
rm /etc/localtime -f
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
cp /data/a.pth /usr/lib/python2.7/dist-packages/
if [ -f /data/requirements.txt ];then
    pip install -r /data/requirements.txt
fi
dm_do $1 $2
