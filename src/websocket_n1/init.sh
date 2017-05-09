#!/bin/bash

websocket_do() {
	port=$1
	cd /data/cgi/
	python app.py
}
rm /etc/localtime -f
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
mkdir /data/cgi/
mkdir /data/lib/
cp /data/a.pth /usr/lib/python2.7/dist-packages/
if [ -f /data/requirements.txt ];then
    pip install -r /data/requirements.txt
fi
websocket_do $1
