Title: 使用wordpress搭建个人站点
Date: 2013-01-27 21:25
Category: 杂项

## 1. 安装mysql

1. 从mysql官网下载源码[5.5.24源码地址](http://downloads.mysql.com/archives/mysql-5.5/mysql-5.5.24.tar.gz)
2. 下载并安装cmake，用来生成makefile。[2.8.9地址](http://www.kitware.com/news/home/browse/CMake?2012_08_09&CMake+2.8.9+is+Now+Available%21)
3. 解压mysql-5.5.24.tar.gz，进入解压后的目录
4. 运行`cmake -i`，设置三个变量：`CMAKE_INSTALL_PREFIX`,`MYSQL_DATADIR`,`SYSCONFDIR`，其他默认即可。
5. `运行make && make install`
6. 进入mysql安装目录，即`CMAKE_INSTALL_PREFIX`指定地址，运行`nohup ./bin/mysqld &启动mysql`


## 2. 安装apache

1. 从apache官网[下载地址](http://www.apache.org/dyn/closer.cgi)找一个合适镜像下载源码。我选择的是[北交大的镜像](http://mirror.bjtu.edu.cn/apache/httpd/)
2. 选择需要的版本下载，然后`tar –zxvf`解压.tar.gz文件
3. 按INSTALL文件中的步骤安装即可: `./configure --prefix=\$TOOL\_ROOT/apache && make && make install`
4. 通过conf/httpd.conf中的"Listen 80"的配置可以修改apache监听的端口，如果需要的话
5. 运行`./bin/apachectl start/stop`可以开启和停止apache服务器（也可以`nohup ./bin/httpd –f conf/httpd.conf`启动）

## 3. 安装php

1. 从php官网下载源码，[下载地址](http://www.php.net/downloads.php)
2. 使用tar -jxvf解压.tar.bz2文件或者tar –zxvf解压.tar.gz文件 
3. 进入解压后的目录，运行./configure --prefix=\$TOOL\_ROOT/php --with-apxs2=\$TOOL\_ROOT/apache/bin/apxs --with-mysql
4. make && make install 
5. 进入apache目录，打开httpd.conf文件，添加如下内容：
   - 添加`"LoadModule php5\_module modules/libphp5.so"`，告诉apache启动时加载PHP模块：  
   - 添加`<FilesMatch \.php$> SetHandler application/x-httpd-php </FileMatch>`，告诉apache遇到.php结尾的文件时解析为PHP：

6. 测试apache是否可以正常解析php：
   - 新建test.php文件，放入apache/htdocs目录，内容如下：  
       ![image](http://images.cnitblog.com/blog/339471/201301/20200250-74e41e8c02e44b73b3aca2acfedcd5cc.png "image")
7.  启动apache服务器 
8.  打开浏览器访问IP:PORT/test.php（IP为apache所在服务器的地址，PORT为apache监听端口）
9.  官方安装文档[地址](http://php.net/manual/zh/install.unix.apache2.php)

## 4. 安装wordpress

1. 从[WordPress中文站](http://cn.wordpress.org/)下载wordpress源码
2. 通过tar -zxvf解压下载的.tar.gz文件
3. cp wordpress到apache/htdocs目录下（如果需要，可以重命名）
4. 在mysql中新建一个数据库供wordpress使用
5. 在mysql中新建一个用户，拥有上一步创建的数据库的读写权限
6. 进入apache/htdocs/wordpress目录，将wp-config-sample.php重命名为wp-config.php，打开该文件并将4、5两步新建的数据库和用户信息填入对应位置，如下：
    ![image](http://images.cnitblog.com/blog/339471/201301/20200251-25aceddc310d4bc6bff5f7b99b933e7b.png "image")
7. 打开浏览器访问IP:PORT/wordpress（IP为apache所在服务器的地址，PORT为apache监听端口，如果第3步重命名了wordpress目录，则PORT/后面需要修改为对应的名字）
8. 按照页面提示，填入所需信息，一步即可按照成功

本篇主要介绍的是如何安装wordpress环境和使用wordpress搭建个人站点，此个人站点暂时还是在本机或者局域网内的，下面一篇将介绍如何申请独立域名和虚拟空间，将自己的站点放到internet上去。

