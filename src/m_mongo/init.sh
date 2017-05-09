#!/bin/bash

mongo_do() {
	port=$1
    role=$2
    mkdir -p /data/log/
    mkdir -p /data/mydb/
    if [ -f /data/.auth ];then
        mongod --config /data/m_auth.conf
    else
        #use dc
        #db.createUser({user: "test",pwd: "test123456",roles:[{role: "readWrite",db: "test"}]});
        #touch /data/.auth
        mongod --config /data/m.conf
        sql="db.createUser({user: 'test',pwd: 'test123456',roles:[{role: 'readWrite',db: 'test'}]});"
        echo $sql | mongo test --shell
        touch /data/.auth
        #mongo -u test -p test123456 --authenticationDatabase test
        #ps axuf|grep mongod |grep -v grep |awk -F " " ' { print $2 } '|xargs kill -9
        #mongod --config /data/m_auth.conf
    fi
}
rm /etc/localtime -f
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
mongo_do $1 $2
