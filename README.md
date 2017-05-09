#接口测试平台

#开发环境及使用

##后台的访问地址
  10.10.68.252，root/test123456
  
##开发环境和测试环境的使用
```shell
#启动容器
$ /data/sbin/startall.sh

#停止容器
$ /data/sbin/stopall.sh

#检查容器是否正常运行
$ docker ps -a
$ docker logs dm_dm

#具体操作一个容器
$ cd /data/dm_dm/
$ ./cmd.sh stop
$ ./cmd.sh start
$ ./cmd.sh shell
```

##日志查看
```shell
$ tail -f /data/log/cgi/login.do.log
```
