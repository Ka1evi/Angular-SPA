#!/bin/bash

cname="dm_dm"
port="8001"
cpu=2

start() {
	docker ps -a|grep -q $cname
    if [ $? -eq 0 ];then
        docker start $cname
    else
        docker run --name $cname -d --privileged --entrypoint /bin/sh --net="host" -v /data/g_nginx/www/:/www -v /data/$cname:/data docker.io/buildo/docker-python2.7-scikit-learn  /data/init.sh $port $cpu
    fi
    echo "start container:$cname success!"
    docker ps -a |grep $cname
}

stop() {
    docker ps -a|grep -q $cname
    if [ $? -eq 0 ];then
        docker stop $cname
        echo "stop container:$cname success!"
        docker ps -a |grep $cname
    else
        echo "container:$cname is not exist."
    fi
}

restart() {
    stop
    start
}

shell() {
    docker ps |grep -q $cname
    if [ $? -ne 0 ];then
        echo "container:$cname is not running."
    else
        docker exec -it $cname bash
    fi
}

case "$1" in
    start)
        $1
        ;;
    stop)
        $1
        ;;
    restart)
        $1
        ;;
    shell)
        $1
        ;;
    *)
        echo $"Usage: $0 {start|stop|shell|restart}"
        exit 2
esac
exit $?

